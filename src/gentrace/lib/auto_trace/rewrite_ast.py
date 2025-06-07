"""AST rewriting for Gentrace auto-tracing."""

from __future__ import annotations

import ast
import time
import uuid
from typing import TYPE_CHECKING, Any, Dict, List, Union, TypeVar, Callable, Optional, ContextManager
from collections import deque
from dataclasses import dataclass

from opentelemetry import trace

from .ast_utils import BaseTransformer

if TYPE_CHECKING:
    from opentelemetry.trace import Tracer


def compile_source(
    tree: ast.AST, 
    filename: str, 
    module_name: str, 
    min_duration: int,
    tracer: Optional['Tracer'] = None,
    pipeline_id: Optional[str] = None,
) -> Callable[[Dict[str, Any]], None]:
    """Compile a modified AST of the module's source code.
    
    Returns a function which accepts module globals and executes the compiled code.
    """
    gentrace_name = f'gentrace_{uuid.uuid4().hex}'
    context_factories: List[Callable[[], ContextManager[Any]]] = []
    tree = rewrite_ast(tree, filename, gentrace_name, module_name, context_factories, min_duration, tracer, pipeline_id)
    assert isinstance(tree, ast.Module)  # for type checking
    # dont_inherit=True is necessary to prevent the module from inheriting the __future__ import from this module.
    code = compile(tree, filename, 'exec', dont_inherit=True)
    
    def execute(globs: Dict[str, Any]):
        globs[gentrace_name] = context_factories
        exec(code, globs, globs)
        
    return execute


def rewrite_ast(
    tree: ast.AST,
    filename: str,
    gentrace_name: str,
    module_name: str,
    context_factories: List[Callable[[], ContextManager[Any]]],
    min_duration: int,
    tracer: Optional['Tracer'] = None,
    pipeline_id: Optional[str] = None,
) -> ast.AST:
    transformer = AutoTraceTransformer(
        gentrace_name, filename, module_name, context_factories, min_duration, tracer, pipeline_id
    )
    return transformer.visit(tree)


@dataclass
class AutoTraceTransformer(BaseTransformer):
    """Trace all encountered functions except those explicitly marked with `@no_auto_trace`."""
    
    context_factories: List[Callable[[], ContextManager[Any]]]
    min_duration: int
    tracer: Optional['Tracer']
    pipeline_id: Optional[str] = None
    
    def check_no_auto_trace(self, node: Union[ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef]) -> bool:
        """Return true if the node has a `@no_auto_trace` decorator."""
        return any(
            (
                isinstance(node, ast.Name)
                and node.id == 'no_auto_trace'
                or (
                    isinstance(node, ast.Attribute)
                    and node.attr == 'no_auto_trace'
                    and isinstance(node.value, ast.Name)
                    and node.value.id == 'gentrace'
                )
            )
            for node in node.decorator_list
        )
        
    def visit_ClassDef(self, node: ast.ClassDef):
        if self.check_no_auto_trace(node):
            return node
            
        return super().visit_ClassDef(node)
        
    def visit_FunctionDef(self, node: Union[ast.FunctionDef, ast.AsyncFunctionDef]):
        if self.check_no_auto_trace(node):
            return node
            
        return super().visit_FunctionDef(node)
        
    def rewrite_function(self, node: Union[ast.FunctionDef, ast.AsyncFunctionDef], qualname: str) -> ast.AST:
        if has_yield(node):
            return node
            
        return super().rewrite_function(node, qualname)
        
    def get_span_attributes(self, qualname: str, lineno: int) -> Dict[str, Any]:
        """Get the attributes to set on the span."""
        # Note: pipeline_id will be added dynamically only to root spans
        return super().get_span_attributes(qualname, lineno)
    
    def create_span_call_node(self, node: Union[ast.FunctionDef, ast.AsyncFunctionDef], qualname: str) -> ast.Call:
        # See the compile_source docstring
        index = len(self.context_factories)
        
        # Get or create tracer  
        tracer = self.tracer or trace.get_tracer("gentrace")
        
        # Create span factory
        span_name = f'{self.module_name}.{qualname}'
        attributes = self.get_span_attributes(qualname, node.lineno)
        
        # When pipeline_id is set, we need special handling
        if self.pipeline_id is not None:
            from opentelemetry import trace as otel_trace, baggage as otel_baggage, context as otel_context

            from ..constants import ATTR_GENTRACE_SAMPLE_KEY, ATTR_GENTRACE_PIPELINE_ID
            
            def create_span_with_pipeline_support():
                """Create span with pipeline_id support."""
                current_context = otel_context.get_current()
                
                # Check if this is a root span (no active span in context)
                current_span = otel_trace.get_current_span(current_context)
                is_root_span = current_span is None or not current_span.is_recording()
                
                # Prepare attributes - only add pipeline_id to root spans
                span_attributes = attributes.copy()
                if is_root_span:
                    span_attributes[ATTR_GENTRACE_PIPELINE_ID] = self.pipeline_id
                
                # For root spans, set baggage context
                if is_root_span:
                    # Check if baggage is already set
                    existing_baggage = otel_baggage.get_baggage(ATTR_GENTRACE_SAMPLE_KEY, context=current_context)
                    if existing_baggage is None:
                        # Set baggage context (similar to @interaction decorator)
                        context_with_baggage = otel_baggage.set_baggage(
                            ATTR_GENTRACE_SAMPLE_KEY, "true", context=current_context
                        )
                        token = otel_context.attach(context_with_baggage)
                        
                        # Create span with the appropriate attributes
                        span = tracer.start_as_current_span(span_name, attributes=span_attributes)
                        
                        # Wrap to ensure we detach the baggage context
                        class SpanWithBaggageCleanup:
                            def __init__(self, span, token):
                                self.span = span
                                self.token = token
                                
                            def __enter__(self):
                                return self.span.__enter__()
                                
                            def __exit__(self, exc_type, exc_val, exc_tb):
                                try:
                                    return self.span.__exit__(exc_type, exc_val, exc_tb)
                                finally:
                                    otel_context.detach(self.token)
                        
                        return SpanWithBaggageCleanup(span, token)
                
                # For non-root spans or if baggage already set, create normal span
                return tracer.start_as_current_span(span_name, attributes=span_attributes)
            
            span_factory = create_span_with_pipeline_support
        else:
            # No pipeline_id, use standard span creation
            span_factory = lambda: tracer.start_as_current_span(span_name, attributes=attributes)
        
        if self.min_duration > 0:
            # This needs to be as fast as possible since it's the cost of auto-tracing a function
            # that never actually gets instrumented because its calls are all faster than `min_duration`.
            class MeasureTime:
                __slots__ = 'start'
                
                def __enter__(_self):
                    _self.start = time.perf_counter_ns()
                    
                def __exit__(_self, *_):
                    if time.perf_counter_ns() - _self.start >= self.min_duration:
                        self.context_factories[index] = span_factory
                        
            self.context_factories.append(MeasureTime)
        else:
            self.context_factories.append(span_factory)
            
        # This node means:
        #   context_factories[index]()
        # where `context_factories` is a global variable with the name `self.span_name_prefix`
        # pointing to the `self.context_factories` list.
        return ast.Call(
            func=ast.Subscript(
                value=ast.Name(id=self.span_name_prefix, ctx=ast.Load()),
                slice=ast.Index(value=ast.Constant(value=index)),  # type: ignore
                ctx=ast.Load(),
            ),
            args=[],
            keywords=[],
        )


T = TypeVar('T')


def no_auto_trace(x: T) -> T:
    """Decorator to prevent a function/class from being traced by `gentrace.install_auto_tracing`.
    
    This is useful for small functions that are called very frequently and would generate too much noise.
    
    The decorator is detected at import time.
    Only `@no_auto_trace` or `@gentrace.no_auto_trace` are supported.
    
    Any decorated function, or any function defined anywhere inside a decorated function/class,
    will be completely ignored by auto-tracing.
    
    This decorator simply returns the argument unchanged, so there is zero runtime overhead.
    """
    return x


def has_yield(node: ast.AST):
    queue = deque([node])
    while queue:
        node = queue.popleft()
        for child in ast.iter_child_nodes(node):
            if isinstance(child, (ast.Yield, ast.YieldFrom)):
                return True
            if not isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda)):
                queue.append(child)