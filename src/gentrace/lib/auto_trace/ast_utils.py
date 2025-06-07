"""AST transformation utilities for Gentrace auto-tracing."""

from __future__ import annotations

import ast
from typing import Any, Dict, List, Union, cast
from dataclasses import dataclass
from typing_extensions import override


@dataclass
class BaseTransformer(ast.NodeTransformer):
    """Helper for rewriting ASTs to wrap function bodies in `with tracer.start_as_current_span(...):`."""
    
    span_name_prefix: str
    filename: str
    module_name: str
    
    def __post_init__(self):
        # Names of functions and classes that we're currently inside,
        # so we can construct the qualified name of the current function.
        self.qualname_stack: List[str] = []
        
    @override
    def visit_ClassDef(self, node: ast.ClassDef):
        self.qualname_stack.append(node.name)
        # We need to call generic_visit here to modify any functions defined inside the class.
        node = cast(ast.ClassDef, self.generic_visit(node))
        self.qualname_stack.pop()
        return node
        
    @override
    def visit_FunctionDef(self, node: Union[ast.FunctionDef, ast.AsyncFunctionDef]):
        self.qualname_stack.append(node.name)
        qualname = '.'.join(self.qualname_stack)
        self.qualname_stack.append('<locals>')
        # We need to call generic_visit here to modify any classes/functions nested inside.
        self.generic_visit(node)
        self.qualname_stack.pop()  # <locals>
        self.qualname_stack.pop()  # node.name
        
        return self.rewrite_function(node, qualname)
        
    @override
    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
        return self.visit_FunctionDef(node)
        
    def rewrite_function(self, node: Union[ast.FunctionDef, ast.AsyncFunctionDef], qualname: str) -> ast.AST:
        # Replace the body of the function with:
        #     with <span_call_node>:
        #         <original body>
        body = node.body.copy()
        new_body: List[ast.stmt] = []
        if (
            body
            and isinstance(body[0], ast.Expr)
            and isinstance(body[0].value, ast.Constant)
            and isinstance(body[0].value.value, str)
        ):
            # If the first statement is just a string literal, it's a docstring.
            # Keep it as the first statement in the new body, not wrapped in a span,
            # so it's still recognized as a docstring.
            new_body.append(body.pop(0))
            
        # Ignore functions with a trivial/empty body:
        # - If `body` is empty, that means it originally was just a docstring that got popped above.
        # - If `body` is just a single `pass` statement
        # - If `body` is just a constant expression, particularly an ellipsis (`...`)
        if not body or (
            len(body) == 1
            and (
                isinstance(body[0], ast.Pass)
                or (isinstance(body[0], ast.Expr) and isinstance(body[0].value, ast.Constant))
            )
        ):
            return node
            
        span = ast.With(
            items=[
                ast.withitem(
                    context_expr=self.create_span_call_node(node, qualname),
                )
            ],
            body=body,
            type_comment=node.type_comment,
        )
        new_body.append(span)
        
        return ast.fix_missing_locations(
            ast.copy_location(
                type(node)(  # type: ignore
                    name=node.name,
                    args=node.args,
                    body=new_body,
                    decorator_list=node.decorator_list,
                    returns=node.returns,
                    type_comment=node.type_comment,
                ),
                node,
            )
        )
        
    def create_span_call_node(self, node: Union[ast.FunctionDef, ast.AsyncFunctionDef], qualname: str) -> ast.Call:
        raise NotImplementedError()
        
    def get_span_attributes(self, qualname: str, lineno: int) -> Dict[str, Any]:
        """Get the attributes to set on the span."""
        return {
            'code.filepath': self.filename,
            'code.lineno': lineno,
            'code.function': qualname,
        }