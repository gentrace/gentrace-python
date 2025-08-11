"""
Python compatibility tests for Gentrace SDK.

This module tests basic functionality of the Gentrace SDK across different Python versions
to ensure compatibility. It focuses on the happy path of importing and initializing the SDK.
"""

import os
import sys
from typing import cast

import pytest

from gentrace.lib.types import OtelConfigOptions


class TestPythonCompatibility:
    """Test suite for Python version compatibility."""

    def test_basic_import(self) -> None:
        """Test that we can import gentrace without errors."""
        import gentrace
        
        # Check that version is accessible
        assert hasattr(gentrace, '__version__') or hasattr(gentrace, 'version')
        
    def test_import_submodules(self) -> None:
        """Test that we can import key submodules."""
        submodules = [
            "gentrace.lib.init",
            "gentrace.lib.utils",
            "gentrace.lib.traced",
            "gentrace.lib.eval",
            "gentrace.types",
        ]
        
        for module in submodules:
            __import__(module)
            assert module in sys.modules
            
    def test_init_default(self) -> None:
        """Test initializing with default settings."""
        import gentrace
        
        # Set a dummy API key to avoid warnings
        os.environ["GENTRACE_API_KEY"] = "test-key-for-compatibility-check"
        
        # This should not raise any exceptions
        gentrace.init()
        
    def test_init_with_api_key(self) -> None:
        """Test initializing with an API key."""
        import gentrace
        
        # This should not raise any exceptions
        gentrace.init(api_key="test-api-key")
        
    def test_init_without_otel(self) -> None:
        """Test initializing without OpenTelemetry."""
        import gentrace
        
        # This should not raise any exceptions
        gentrace.init(api_key="test-api-key", otel_setup=False)
        
    def test_init_with_custom_otel_config(self) -> None:
        """Test initializing with custom OpenTelemetry configuration."""
        import gentrace
        
        otel_config = cast(OtelConfigOptions, {
            "service_name": "compatibility-test",
            "debug": False
        })
        
        # This should not raise any exceptions
        gentrace.init(api_key="test-api-key", otel_setup=otel_config)
        
    def test_basic_functionality(self) -> None:
        """Test basic SDK functionality after initialization."""
        from gentrace.lib.traced import traced
        
        # Test that we can use the @traced decorator
        @traced()
        def sample_function(x: int) -> int:
            return x * 2
        
        # Verify the function is wrapped
        assert hasattr(sample_function, '__wrapped__')
        
        # Test that we can import types
        from gentrace.types import Dataset, Pipeline, TestCase, Experiment
        
        # Verify types are importable (they exist in the namespace)
        assert Dataset is not None
        assert Pipeline is not None
        assert TestCase is not None
        assert Experiment is not None
        
    def test_type_annotations_compatibility(self) -> None:
        """Test that type annotations don't cause import errors."""
        # This specifically tests for issues like the Sequence import problem
        # that was fixed for Python 3.8 compatibility
        
        from gentrace.lib import utils
        
        # Check that the module loaded successfully
        assert hasattr(utils, 'display_table')
        assert hasattr(utils, 'print_function_call_summary')
        
        # These functions use type annotations that were problematic
        # in Python 3.8 (Sequence, Tuple, Dict)
        import inspect
        
        # Get the function signatures to ensure they're properly annotated
        display_table_sig = inspect.signature(utils.display_table)
        assert 'columns' in display_table_sig.parameters
        assert 'rows' in display_table_sig.parameters
        
        print_func_sig = inspect.signature(utils.print_function_call_summary)
        assert 'args' in print_func_sig.parameters
        assert 'kwargs' in print_func_sig.parameters


@pytest.fixture(autouse=True)
def reset_gentrace_state():
    """Reset Gentrace state between tests to avoid initialization warnings."""
    # Clear any existing initialization state
    import sys
    if hasattr(sys.modules.get("gentrace", None), "__gentrace_initialized"):
        delattr(sys.modules["gentrace"], "__gentrace_initialized")
    if hasattr(sys.modules.get("gentrace", None), "__gentrace_otel_setup_config"):
        delattr(sys.modules["gentrace"], "__gentrace_otel_setup_config")
    
    # Clear init history
    from gentrace.lib.init import _init_history
    _init_history.clear()
    # Reset call count by accessing the module's global
    import gentrace.lib.init
    gentrace.lib.init._init_call_count = 0
    
    yield
    
    # Cleanup after test
    if hasattr(sys.modules.get("gentrace", None), "__gentrace_initialized"):
        delattr(sys.modules["gentrace"], "__gentrace_initialized")
    if hasattr(sys.modules.get("gentrace", None), "__gentrace_otel_setup_config"):
        delattr(sys.modules["gentrace"], "__gentrace_otel_setup_config")