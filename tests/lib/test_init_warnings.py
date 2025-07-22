import sys
from unittest.mock import MagicMock, patch

import pytest

from gentrace.lib.init import init

# Get a direct reference to the module where init() is defined
init_module_object = sys.modules["gentrace.lib.init"]


@pytest.fixture(autouse=True)
def reset_init_state():
    """Reset the init state before each test"""
    # Clear the history
    if hasattr(init_module_object, '_init_history'):
        init_module_object._init_history.clear()  # type: ignore
    if hasattr(init_module_object, '_init_call_count'):
        init_module_object._init_call_count = 0  # type: ignore
    yield
    # Clean up after test
    if hasattr(init_module_object, '_init_history'):
        init_module_object._init_history.clear()  # type: ignore
    if hasattr(init_module_object, '_init_call_count'):
        init_module_object._init_call_count = 0  # type: ignore


def test_first_init_no_warning():
    """First init() call should not produce any warning"""
    with patch.object(init_module_object, "Gentrace") as mock_gentrace_cls, \
         patch.object(init_module_object, "AsyncGentrace") as mock_async_gentrace_cls, \
         patch.object(init_module_object, "_set_client_instances") as _mock_set_instances, \
         patch.object(init_module_object, "_setup_otel") as _mock_setup_otel, \
         patch.object(init_module_object.GentraceWarnings, "MultipleInitWarning") as mock_warning:
        
        mock_sync_client = MagicMock()
        mock_async_client = MagicMock()
        mock_gentrace_cls.return_value = mock_sync_client
        mock_async_gentrace_cls.return_value = mock_async_client
        
        init(api_key="test-key-1")
        
        # Should not create any warning
        mock_warning.assert_not_called()
        
        # Should have one entry in history
        history = init_module_object._get_init_history()
        assert len(history) == 1
        assert history[0].options["api_key"] == "test-key-1"


def test_multiple_init_same_config_no_warning():
    """Multiple init() calls with same config should not produce warning"""
    with patch.object(init_module_object, "Gentrace") as mock_gentrace_cls, \
         patch.object(init_module_object, "AsyncGentrace") as mock_async_gentrace_cls, \
         patch.object(init_module_object, "_set_client_instances") as _mock_set_instances, \
         patch.object(init_module_object, "_setup_otel") as _mock_setup_otel, \
         patch.object(init_module_object.GentraceWarnings, "MultipleInitWarning") as mock_warning:
        
        mock_sync_client = MagicMock()
        mock_async_client = MagicMock()
        mock_gentrace_cls.return_value = mock_sync_client
        mock_async_gentrace_cls.return_value = mock_async_client
        
        # Call init twice with same config
        init(api_key="test-key-1", base_url="https://gentrace.ai/api")
        init(api_key="test-key-1", base_url="https://gentrace.ai/api")
        
        # Should not create any warning since config is the same
        mock_warning.assert_not_called()
        
        # Should have two entries in history
        history = init_module_object._get_init_history()
        assert len(history) == 2


def test_multiple_init_different_config_shows_warning():
    """Multiple init() calls with different config should produce warning"""
    with patch.object(init_module_object, "Gentrace") as mock_gentrace_cls, \
         patch.object(init_module_object, "AsyncGentrace") as mock_async_gentrace_cls, \
         patch.object(init_module_object, "_set_client_instances") as _mock_set_instances, \
         patch.object(init_module_object, "_setup_otel") as _mock_setup_otel:
        
        mock_sync_client = MagicMock()
        mock_async_client = MagicMock()
        mock_gentrace_cls.return_value = mock_sync_client
        mock_async_gentrace_cls.return_value = mock_async_client
        
        # Mock the warning display
        mock_warning_instance = MagicMock()
        with patch.object(init_module_object.GentraceWarnings, "MultipleInitWarning", return_value=mock_warning_instance):
            # First init
            init(api_key="test-key-1", base_url="https://gentrace.ai/api")
            
            # Second init with different config
            init(api_key="test-key-2", base_url="https://gentrace.ai/api", timeout=30)
            
            # Should create and display warning
            init_module_object.GentraceWarnings.MultipleInitWarning.assert_called_once()
            mock_warning_instance.display.assert_called_once()
            
            # Check the warning was called with correct parameters
            call_args = init_module_object.GentraceWarnings.MultipleInitWarning.call_args
            assert call_args[1]["call_number"] == 2
            assert len(call_args[1]["diff_lines"]) > 0
            assert len(call_args[1]["init_history"]) == 1


def test_warning_masks_sensitive_values():
    """Warning should mask sensitive values like API keys"""
    with patch.object(init_module_object, "Gentrace") as mock_gentrace_cls, \
         patch.object(init_module_object, "AsyncGentrace") as mock_async_gentrace_cls, \
         patch.object(init_module_object, "_set_client_instances") as _mock_set_instances, \
         patch.object(init_module_object, "_setup_otel") as _mock_setup_otel:
        
        mock_sync_client = MagicMock()
        mock_async_client = MagicMock()
        mock_gentrace_cls.return_value = mock_sync_client
        mock_async_gentrace_cls.return_value = mock_async_client
        
        # Mock the warning
        mock_warning_instance = MagicMock()
        with patch.object(init_module_object.GentraceWarnings, "MultipleInitWarning", return_value=mock_warning_instance):
            # First init
            init(api_key="sk-1234567890abcdef")
            
            # Second init with different API key
            init(api_key="sk-abcdef1234567890")
            
            # Check that diff lines contain masked values
            call_args = init_module_object.GentraceWarnings.MultipleInitWarning.call_args
            diff_lines = call_args[1]["diff_lines"]
            
            # Check that API key is masked in diff
            diff_text = " ".join(diff_lines)
            assert "sk-123***" in diff_text or "sk-abc***" in diff_text
            assert "sk-1234567890abcdef" not in diff_text
            assert "sk-abcdef1234567890" not in diff_text


def test_multiple_init_tracks_history():
    """Multiple init calls should properly track history"""
    with patch.object(init_module_object, "Gentrace") as mock_gentrace_cls, \
         patch.object(init_module_object, "AsyncGentrace") as mock_async_gentrace_cls, \
         patch.object(init_module_object, "_set_client_instances") as _mock_set_instances, \
         patch.object(init_module_object, "_setup_otel") as _mock_setup_otel:
        
        mock_sync_client = MagicMock()
        mock_async_client = MagicMock()
        mock_gentrace_cls.return_value = mock_sync_client
        mock_async_gentrace_cls.return_value = mock_async_client
        
        # Call init multiple times
        init(api_key="key-1")
        init(api_key="key-2", base_url="https://gentrace.ai/api")
        init(api_key="key-3", timeout=60)
        
        # Check history
        history = init_module_object._get_init_history()
        assert len(history) == 3
        assert history[0].options["api_key"] == "key-1"
        assert history[1].options["api_key"] == "key-2"
        assert history[1].options["base_url"] == "https://gentrace.ai/api"
        assert history[2].options["api_key"] == "key-3"
        assert history[2].options["timeout"] == 60


def test_otel_setup_changes_trigger_warning():
    """Changes to otel_setup should trigger warning"""
    with patch.object(init_module_object, "Gentrace") as mock_gentrace_cls, \
         patch.object(init_module_object, "AsyncGentrace") as mock_async_gentrace_cls, \
         patch.object(init_module_object, "_set_client_instances") as _mock_set_instances, \
         patch.object(init_module_object, "_setup_otel") as _mock_setup_otel:
        
        mock_sync_client = MagicMock()
        mock_async_client = MagicMock()
        mock_gentrace_cls.return_value = mock_sync_client
        mock_async_gentrace_cls.return_value = mock_async_client
        
        # Mock the warning
        mock_warning_instance = MagicMock()
        with patch.object(init_module_object.GentraceWarnings, "MultipleInitWarning", return_value=mock_warning_instance):
            # First init with otel_setup=True
            init(api_key="test-key", otel_setup=True)
            
            # Second init with otel_setup=False
            init(api_key="test-key", otel_setup=False)
            
            # Should show warning even though api_key is the same
            init_module_object.GentraceWarnings.MultipleInitWarning.assert_called_once()
            mock_warning_instance.display.assert_called_once()


def test_warning_shows_all_changed_fields():
    """Warning should show all fields that changed"""
    with patch.object(init_module_object, "Gentrace") as mock_gentrace_cls, \
         patch.object(init_module_object, "AsyncGentrace") as mock_async_gentrace_cls, \
         patch.object(init_module_object, "_set_client_instances") as _mock_set_instances, \
         patch.object(init_module_object, "_setup_otel") as _mock_setup_otel:
        
        mock_sync_client = MagicMock()
        mock_async_client = MagicMock()
        mock_gentrace_cls.return_value = mock_sync_client
        mock_async_gentrace_cls.return_value = mock_async_client
        
        # Mock the warning
        mock_warning_instance = MagicMock()
        with patch.object(init_module_object.GentraceWarnings, "MultipleInitWarning", return_value=mock_warning_instance):
            # First init
            init(api_key="key-1", base_url="https://gentrace.ai/api", timeout=30)
            
            # Second init with multiple changes
            init(api_key="key-2", base_url="https://custom.gentrace.ai/api", timeout=60, max_retries=5)
            
            # Check diff lines contain all changes
            call_args = init_module_object.GentraceWarnings.MultipleInitWarning.call_args
            diff_lines = call_args[1]["diff_lines"]
            diff_text = " ".join(diff_lines)
            
            # Should show changes for api_key, base_url, timeout, and addition of max_retries
            assert "api_key" in diff_text
            assert "base_url" in diff_text
            assert "timeout" in diff_text
            assert "max_retries" in diff_text


def test_complex_otel_config_diff():
    """Complex otel_setup configurations should be properly diffed"""
    with patch.object(init_module_object, "Gentrace") as mock_gentrace_cls, \
         patch.object(init_module_object, "AsyncGentrace") as mock_async_gentrace_cls, \
         patch.object(init_module_object, "_set_client_instances") as _mock_set_instances, \
         patch.object(init_module_object, "_setup_otel") as _mock_setup_otel:
        
        mock_sync_client = MagicMock()
        mock_async_client = MagicMock()
        mock_gentrace_cls.return_value = mock_sync_client
        mock_async_gentrace_cls.return_value = mock_async_client
        
        # Mock the warning
        mock_warning_instance = MagicMock()
        with patch.object(init_module_object.GentraceWarnings, "MultipleInitWarning", return_value=mock_warning_instance):
            # First init with dict otel_setup
            init(api_key="test-key", otel_setup={"service_name": "service-1", "debug": False})
            
            # Second init with different dict otel_setup
            init(api_key="test-key", otel_setup={"service_name": "service-2", "debug": True})
            
            # Should show warning
            init_module_object.GentraceWarnings.MultipleInitWarning.assert_called_once()
            
            # Check that diff shows the dict properly
            call_args = init_module_object.GentraceWarnings.MultipleInitWarning.call_args
            diff_lines = call_args[1]["diff_lines"]
            diff_text = " ".join(diff_lines)
            
            # Should show the otel_setup changed
            assert "otel_setup" in diff_text


def test_init_call_numbers_increment():
    """Init call numbers should increment properly"""
    with patch.object(init_module_object, "Gentrace") as mock_gentrace_cls, \
         patch.object(init_module_object, "AsyncGentrace") as mock_async_gentrace_cls, \
         patch.object(init_module_object, "_set_client_instances") as _mock_set_instances, \
         patch.object(init_module_object, "_setup_otel") as _mock_setup_otel:
        
        mock_sync_client = MagicMock()
        mock_async_client = MagicMock()
        mock_gentrace_cls.return_value = mock_sync_client
        mock_async_gentrace_cls.return_value = mock_async_client
        
        # Call init three times
        init(api_key="key-1")
        init(api_key="key-2")
        init(api_key="key-3")
        
        # Check call numbers
        history = init_module_object._get_init_history()
        assert history[0].call_number == 1
        assert history[1].call_number == 2
        assert history[2].call_number == 3


def test_warning_display_format():
    """Test the warning display format matches expected structure"""
    from gentrace.lib.warnings import GentraceWarnings
    
    # Create a warning instance directly
    warning = GentraceWarnings.MultipleInitWarning(
        call_number=2,
        diff_lines=[
            "  api_key:",
            '    - "sk-123***" → "sk-abc***"',
            "  timeout:",
            "    + 60",
        ],
        init_history=[
            {"timestamp": 1234567890, "callNumber": 1}
        ]
    )
    
    # Check the warning structure
    assert warning.warning_id == "GT_MultipleInitWarning"
    assert warning.title == "Multiple Initialization Detected"
    assert "Gentrace init() has been called 2 times." in warning.message
    assert "Configuration changes detected:" in warning.message
    assert warning.border_color == "yellow"