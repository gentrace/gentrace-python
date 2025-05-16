import sys
from unittest.mock import MagicMock, patch

from gentrace.lib.init import init as function_under_test

# Get a direct reference to the module where init() is defined and its dependencies are looked up
init_module_object = sys.modules["gentrace.lib.init"]

# Test functions will now be pytest-style
# The order of mock arguments corresponds to the patch decorators from bottom to top (applied inside-out)


def test_init_with_all_args_and_kwargs() -> None:
    with patch.object(init_module_object, "Gentrace") as mock_gentrace_cls, patch.object(
        init_module_object, "AsyncGentrace"
    ) as mock_async_gentrace_cls, patch.object(init_module_object, "_set_client_instances") as mock_set_instances:
        mock_sync_client_instance = MagicMock()
        mock_async_client_instance = MagicMock()
        mock_gentrace_cls.return_value = mock_sync_client_instance
        mock_async_gentrace_cls.return_value = mock_async_client_instance

        function_under_test(api_key="test_token_val", base_url="http://testserver", timeout=60)

        mock_gentrace_cls.assert_called_once_with(api_key="test_token_val", base_url="http://testserver", timeout=60)
        mock_async_gentrace_cls.assert_called_once_with(
            api_key="test_token_val", base_url="http://testserver", timeout=60
        )
        mock_set_instances.assert_called_once_with(mock_sync_client_instance, mock_async_client_instance)


def test_init_with_api_key_only() -> None:
    with patch.object(init_module_object, "Gentrace") as mock_gentrace_cls, patch.object(
        init_module_object, "AsyncGentrace"
    ) as mock_async_gentrace_cls, patch.object(init_module_object, "_set_client_instances") as mock_set_instances:
        mock_sync_client_instance = MagicMock()
        mock_async_client_instance = MagicMock()
        mock_gentrace_cls.return_value = mock_sync_client_instance
        mock_async_gentrace_cls.return_value = mock_async_client_instance

        function_under_test(api_key="test_token_val")

        mock_gentrace_cls.assert_called_once_with(api_key="test_token_val")
        mock_async_gentrace_cls.assert_called_once_with(api_key="test_token_val")
        mock_set_instances.assert_called_once_with(mock_sync_client_instance, mock_async_client_instance)


def test_init_with_base_url_only() -> None:
    with patch.object(init_module_object, "Gentrace") as mock_gentrace_cls, patch.object(
        init_module_object, "AsyncGentrace"
    ) as mock_async_gentrace_cls, patch.object(init_module_object, "_set_client_instances") as mock_set_instances:
        mock_sync_client_instance = MagicMock()
        mock_async_client_instance = MagicMock()
        mock_gentrace_cls.return_value = mock_sync_client_instance
        mock_async_gentrace_cls.return_value = mock_async_client_instance

        function_under_test(base_url="http://testserver")

        mock_gentrace_cls.assert_called_once_with(base_url="http://testserver")
        mock_async_gentrace_cls.assert_called_once_with(base_url="http://testserver")
        mock_set_instances.assert_called_once_with(mock_sync_client_instance, mock_async_client_instance)


def test_init_with_no_explicit_args() -> None:
    with patch.object(init_module_object, "Gentrace") as mock_gentrace_cls, patch.object(
        init_module_object, "AsyncGentrace"
    ) as mock_async_gentrace_cls, patch.object(init_module_object, "_set_client_instances") as mock_set_instances:
        mock_sync_client_instance = MagicMock()
        mock_async_client_instance = MagicMock()
        mock_gentrace_cls.return_value = mock_sync_client_instance
        mock_async_gentrace_cls.return_value = mock_async_client_instance

        function_under_test()

        mock_gentrace_cls.assert_called_once_with()
        mock_async_gentrace_cls.assert_called_once_with()
        mock_set_instances.assert_called_once_with(mock_sync_client_instance, mock_async_client_instance)


def test_init_with_additional_kwargs() -> None:
    with patch.object(init_module_object, "Gentrace") as mock_gentrace_cls, patch.object(
        init_module_object, "AsyncGentrace"
    ) as mock_async_gentrace_cls, patch.object(init_module_object, "_set_client_instances") as mock_set_instances:
        mock_sync_client_instance = MagicMock()
        mock_async_client_instance = MagicMock()
        mock_gentrace_cls.return_value = mock_sync_client_instance
        mock_async_gentrace_cls.return_value = mock_async_client_instance

        function_under_test(max_retries=5, custom_option="test_custom")

        mock_gentrace_cls.assert_called_once_with(max_retries=5, custom_option="test_custom")
        mock_async_gentrace_cls.assert_called_once_with(max_retries=5, custom_option="test_custom")
        mock_set_instances.assert_called_once_with(mock_sync_client_instance, mock_async_client_instance)
