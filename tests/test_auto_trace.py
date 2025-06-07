"""Tests for the auto-trace functionality."""

import ast
import sys
from typing import Any
from unittest.mock import Mock

import pytest

# pyright: reportUnknownMemberType=false, reportUnknownParameterType=false, reportUnknownArgumentType=false


class TestAutoTrace:
    """Test the auto-trace AST transformation functionality."""
    
    @pytest.fixture
    def mock_tracer(self) -> Mock:
        """Create a mock tracer for testing."""
        tracer = Mock()
        span = Mock()
        span.__enter__ = Mock(return_value=span)
        span.__exit__ = Mock(return_value=None)
        tracer.start_as_current_span.return_value = span
        return tracer
    
    def test_compile_source_basic(self, mock_tracer: Mock) -> None:
        """Test basic AST compilation with auto-tracing."""
        from gentrace.lib.auto_trace.rewrite_ast import compile_source
        
        # Simple test code
        code = """
def add(a, b):
    return a + b

result = add(1, 2)
"""
        
        # Parse and compile
        tree = ast.parse(code)
        execute = compile_source(tree, '<test>', 'test_module', min_duration=0, tracer=mock_tracer)
        
        # Execute
        globs: dict[str, Any] = {}
        execute(globs)
        
        # Check that the function was defined and works
        assert 'add' in globs
        assert globs['result'] == 3
        
        # Check that tracer was called
        mock_tracer.start_as_current_span.assert_called()
    
    def test_no_auto_trace_decorator(self, mock_tracer: Mock) -> None:
        """Test that @no_auto_trace decorator prevents tracing."""
        from gentrace.lib.auto_trace.rewrite_ast import no_auto_trace, compile_source
        
        # Code with no_auto_trace decorator
        code = """
from gentrace.lib.auto_trace.rewrite_ast import no_auto_trace

@no_auto_trace
def skipped():
    return "not traced"

def traced():
    return "traced"

r1 = skipped()
r2 = traced()
"""
        
        # Parse and compile
        tree = ast.parse(code)
        execute = compile_source(tree, '<test>', 'test_module', min_duration=0, tracer=mock_tracer)
        
        # Execute with the decorator available
        globs = {'no_auto_trace': no_auto_trace}
        execute(globs)
        
        # Check results
        assert globs['r1'] == "not traced"
        assert globs['r2'] == "traced"
        
        # Check that only one function was traced
        assert mock_tracer.start_as_current_span.call_count == 1
    
    def test_class_methods_traced(self, mock_tracer: Mock) -> None:
        """Test that class methods are traced."""
        from gentrace.lib.auto_trace.rewrite_ast import compile_source
        
        code = """
class Calculator:
    def add(self, a, b):
        return a + b
    
    @classmethod
    def multiply(cls, a, b):
        return a * b

calc = Calculator()
r1 = calc.add(2, 3)
r2 = Calculator.multiply(4, 5)
"""
        
        # Parse and compile
        tree = ast.parse(code)
        execute = compile_source(tree, '<test>', 'test_module', min_duration=0, tracer=mock_tracer)
        
        # Execute
        globs: dict[str, Any] = {}
        execute(globs)
        
        # Check results
        assert globs['r1'] == 5
        assert globs['r2'] == 20
        
        # Check that methods were traced
        assert mock_tracer.start_as_current_span.call_count >= 2
    
    def test_generator_functions_not_traced(self, mock_tracer: Mock) -> None:
        """Test that generator functions are not traced (they have yield)."""
        from gentrace.lib.auto_trace.rewrite_ast import compile_source
        
        code = """
def generator():
    yield 1
    yield 2

def regular():
    return list(generator())

result = regular()
"""
        
        # Parse and compile
        tree = ast.parse(code)
        execute = compile_source(tree, '<test>', 'test_module', min_duration=0, tracer=mock_tracer)
        
        # Execute
        globs: dict[str, Any] = {}
        execute(globs)
        
        # Check results
        assert globs['result'] == [1, 2]
        
        # Only regular() should be traced, not generator()
        assert mock_tracer.start_as_current_span.call_count == 1
    
    def test_install_auto_tracing(self) -> None:
        """Test the install_auto_tracing function."""
        from gentrace.lib.auto_trace import GentraceFinder, install_auto_tracing
        
        # Install auto-tracing for a test module pattern
        install_auto_tracing(['test_dummy_module'], check_imported_modules='ignore')
        
        # Check that the finder was added to sys.meta_path
        finder = None
        for item in sys.meta_path:
            if isinstance(item, GentraceFinder):
                finder = item
                break
        
        assert finder is not None
        
        # Clean up
        sys.meta_path.remove(finder)
    
    def test_install_auto_tracing_with_pipeline_id(self) -> None:
        """Test install_auto_tracing with pipeline_id."""
        import uuid

        from gentrace.lib.auto_trace import GentraceFinder, install_auto_tracing
        
        pipeline_id = str(uuid.uuid4())
        
        # Install auto-tracing with pipeline_id
        install_auto_tracing(
            ['test_dummy_module'], 
            check_imported_modules='ignore',
            pipeline_id=pipeline_id
        )
        
        # Check that the finder was added with pipeline_id
        finder = None
        for item in sys.meta_path:
            if isinstance(item, GentraceFinder):
                finder = item
                break
        
        assert finder is not None
        assert finder.pipeline_id == pipeline_id
        
        # Clean up
        sys.meta_path.remove(finder)
    
    def test_install_auto_tracing_invalid_pipeline_id(self) -> None:
        """Test that invalid pipeline_id raises ValueError."""
        from gentrace.lib.auto_trace import install_auto_tracing
        
        with pytest.raises(ValueError, match="pipeline_id must be a valid UUID"):
            install_auto_tracing(
                ['test_dummy_module'],
                check_imported_modules='ignore',
                pipeline_id="not-a-uuid"
            )
    
    def test_compile_source_with_pipeline_id(self, mock_tracer: Mock) -> None:
        """Test that pipeline_id is handled correctly for auto-traced functions."""
        import uuid

        from gentrace.lib.auto_trace.rewrite_ast import compile_source
        
        pipeline_id = str(uuid.uuid4())
        
        # Simple test code
        code = """
def test_func():
    return "hello"

result = test_func()
"""
        
        # Parse and compile with pipeline_id
        tree = ast.parse(code)
        execute = compile_source(
            tree, '<test>', 'test_module', 
            min_duration=0, 
            tracer=mock_tracer,
            pipeline_id=pipeline_id
        )
        
        # Execute
        globs: dict[str, Any] = {}
        execute(globs)
        
        # The function should have been called to create a span
        mock_tracer.start_as_current_span.assert_called()
        
        # Note: The actual pipeline_id attribute is added dynamically at runtime
        # based on whether it's a root span or not, so we can't test it directly
        # without mocking the OpenTelemetry context
    
    def test_ast_transformation_preserves_docstrings(self, mock_tracer: Mock) -> None:
        """Test that docstrings are preserved during AST transformation."""
        from gentrace.lib.auto_trace.rewrite_ast import compile_source
        
        code = '''
def documented():
    """This is a docstring."""
    return 42
'''
        
        # Parse and compile
        tree = ast.parse(code)
        execute = compile_source(tree, '<test>', 'test_module', min_duration=0, tracer=mock_tracer)
        
        # Execute
        globs: dict[str, Any] = {}
        execute(globs)
        
        # Check that docstring is preserved
        assert globs['documented'].__doc__ == "This is a docstring."