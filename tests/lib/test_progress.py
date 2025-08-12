"""Tests for progress reporting functionality."""

import logging
from typing import Any
from unittest.mock import Mock, patch

import pytest

from gentrace.lib.utils import is_ci
from gentrace.lib.progress import (
    ProgressReporter,
    RichProgressReporter,
    SimpleProgressReporter,
)


class TestCIDetection:
    """Tests for the is_ci() function."""

    def test_is_ci_with_ci_env_true(self, monkeypatch: Any) -> None:
        """Test CI detection when CI env var is 'true'."""
        monkeypatch.setenv("CI", "true")
        assert is_ci() is True

    def test_is_ci_with_ci_env_uppercase_true(self, monkeypatch: Any) -> None:
        """Test CI detection when CI env var is 'TRUE'."""
        monkeypatch.setenv("CI", "TRUE")
        assert is_ci() is True

    def test_is_ci_with_ci_env_1(self, monkeypatch: Any) -> None:
        """Test CI detection when CI env var is '1'."""
        monkeypatch.setenv("CI", "1")
        assert is_ci() is True

    def test_is_ci_with_ci_env_yes(self, monkeypatch: Any) -> None:
        """Test CI detection when CI env var is 'yes'."""
        monkeypatch.setenv("CI", "yes")
        assert is_ci() is True

    def test_is_ci_with_continuous_integration(self, monkeypatch: Any) -> None:
        """Test CI detection with CONTINUOUS_INTEGRATION env var."""
        monkeypatch.setenv("CONTINUOUS_INTEGRATION", "true")
        assert is_ci() is True

    def test_is_ci_with_github_actions(self, monkeypatch: Any) -> None:
        """Test CI detection in GitHub Actions environment."""
        monkeypatch.setenv("GITHUB_ACTIONS", "true")
        assert is_ci() is True

    def test_is_ci_with_gitlab_ci(self, monkeypatch: Any) -> None:
        """Test CI detection in GitLab CI environment."""
        monkeypatch.setenv("GITLAB_CI", "1")
        assert is_ci() is True

    def test_is_ci_with_circleci(self, monkeypatch: Any) -> None:
        """Test CI detection in CircleCI environment."""
        monkeypatch.setenv("CIRCLECI", "true")
        assert is_ci() is True

    def test_is_ci_with_jenkins(self, monkeypatch: Any) -> None:
        """Test CI detection in Jenkins environment."""
        monkeypatch.setenv("JENKINS_URL", "http://jenkins.example.com")
        assert is_ci() is True

    def test_is_ci_with_azure_pipelines(self, monkeypatch: Any) -> None:
        """Test CI detection in Azure Pipelines environment."""
        monkeypatch.setenv("TF_BUILD", "True")
        assert is_ci() is True

    def test_is_ci_false_when_no_ci_vars(self, monkeypatch: Any) -> None:
        """Test CI detection returns False when no CI variables are set."""
        # Clear all potential CI environment variables
        ci_vars = [
            "CI",
            "CONTINUOUS_INTEGRATION",
            "GITHUB_ACTIONS",
            "GITLAB_CI",
            "CIRCLECI",
            "TRAVIS",
            "JENKINS_URL",
            "JENKINS_HOME",
            "BUILDKITE",
            "DRONE",
            "BAMBOO_BUILD_NUMBER",
            "TF_BUILD",
            "TEAMCITY_VERSION",
            "BITBUCKET_BUILD_NUMBER",
            "SEMAPHORE",
            "APPVEYOR",
            "CODEBUILD_BUILD_ID",
            "NETLIFY",
            "VERCEL",
            "RENDER",
        ]
        for var in ci_vars:
            monkeypatch.delenv(var, raising=False)

        assert is_ci() is False

    def test_is_ci_false_with_ci_false(self, monkeypatch: Any) -> None:
        """Test CI detection when CI is explicitly 'false'."""
        # Clear all potential CI environment variables first
        ci_vars = [
            "CI",
            "CONTINUOUS_INTEGRATION",
            "GITHUB_ACTIONS",
            "GITLAB_CI",
            "CIRCLECI",
            "TRAVIS",
            "JENKINS_URL",
            "JENKINS_HOME",
            "BUILDKITE",
            "DRONE",
            "BAMBOO_BUILD_NUMBER",
            "TF_BUILD",
            "TEAMCITY_VERSION",
            "BITBUCKET_BUILD_NUMBER",
            "SEMAPHORE",
            "APPVEYOR",
            "CODEBUILD_BUILD_ID",
            "NETLIFY",
            "VERCEL",
            "RENDER",
        ]
        for var in ci_vars:
            monkeypatch.delenv(var, raising=False)

        # Now set CI to false
        monkeypatch.setenv("CI", "false")
        assert is_ci() is False

    def test_is_ci_false_with_ci_empty(self, monkeypatch: Any) -> None:
        """Test CI detection when CI is empty string."""
        # Clear all potential CI environment variables first
        ci_vars = [
            "CI",
            "CONTINUOUS_INTEGRATION",
            "GITHUB_ACTIONS",
            "GITLAB_CI",
            "CIRCLECI",
            "TRAVIS",
            "JENKINS_URL",
            "JENKINS_HOME",
            "BUILDKITE",
            "DRONE",
            "BAMBOO_BUILD_NUMBER",
            "TF_BUILD",
            "TEAMCITY_VERSION",
            "BITBUCKET_BUILD_NUMBER",
            "SEMAPHORE",
            "APPVEYOR",
            "CODEBUILD_BUILD_ID",
            "NETLIFY",
            "VERCEL",
            "RENDER",
        ]
        for var in ci_vars:
            monkeypatch.delenv(var, raising=False)

        # Now set CI to empty string
        monkeypatch.setenv("CI", "")
        assert is_ci() is False


class TestSimpleProgressReporter:
    """Tests for SimpleProgressReporter."""

    def test_init_with_custom_logger(self) -> None:
        """Test initialization with a custom logger."""
        mock_logger = Mock(spec=logging.Logger)
        reporter = SimpleProgressReporter(logger=mock_logger)
        assert reporter.logger is mock_logger
        assert reporter.total == 0
        assert reporter.current == 0
        assert reporter.pipeline_id == ""

    def test_init_without_logger(self) -> None:
        """Test initialization without a logger (uses default)."""
        reporter = SimpleProgressReporter()
        assert reporter.logger is not None
        assert reporter.logger.name == "gentrace"

    def test_start(self) -> None:
        """Test starting a new evaluation run."""
        mock_logger = Mock(spec=logging.Logger)
        reporter = SimpleProgressReporter(logger=mock_logger)

        reporter.start("pipeline-123", 10)

        assert reporter.pipeline_id == "pipeline-123"
        assert reporter.total == 10
        assert reporter.current == 0
        mock_logger.info.assert_called_once_with("\nRunning experiment with 10 test cases...")

    def test_start_single_case(self) -> None:
        """Test starting with a single test case (singular form)."""
        mock_logger = Mock(spec=logging.Logger)
        reporter = SimpleProgressReporter(logger=mock_logger)

        reporter.start("pipeline-123", 1)

        mock_logger.info.assert_called_once_with("\nRunning experiment with 1 test case...")

    def test_increment(self) -> None:
        """Test incrementing progress."""
        mock_logger = Mock(spec=logging.Logger)
        reporter = SimpleProgressReporter(logger=mock_logger)

        reporter.start("pipeline-123", 3)
        mock_logger.reset_mock()

        reporter.increment("Test Case 1")
        assert reporter.current == 1
        mock_logger.info.assert_called_with('[1/3] Running test case: "Test Case 1"')

        reporter.increment("Test Case 2")
        assert reporter.current == 2
        mock_logger.info.assert_called_with('[2/3] Running test case: "Test Case 2"')

    def test_stop(self) -> None:
        """Test stopping the reporter."""
        mock_logger = Mock(spec=logging.Logger)
        reporter = SimpleProgressReporter(logger=mock_logger)

        reporter.stop()

        mock_logger.info.assert_called_once_with("Evaluation complete.")

    def test_start_with_url(self) -> None:
        """Test starting with an experiment URL."""
        mock_logger = Mock(spec=logging.Logger)
        reporter = SimpleProgressReporter(logger=mock_logger)
        
        test_url = "https://gentrace.ai/t/org/pipeline/123/experiments/abc"
        reporter.start("pipeline-123", 5, test_url)
        
        # Verify both the start message and URL were logged
        assert mock_logger.info.call_count == 2
        calls = mock_logger.info.call_args_list
        assert "Running experiment with 5 test cases..." in calls[0][0][0]
        assert f"Experiment URL: {test_url}" in calls[1][0][0]

    def test_full_lifecycle(self) -> None:
        """Test complete lifecycle of progress reporting."""
        mock_logger = Mock(spec=logging.Logger)
        reporter = SimpleProgressReporter(logger=mock_logger)

        # Start
        reporter.start("pipeline-123", 2)

        # Process test cases
        reporter.increment("Login Test")
        reporter.increment("Logout Test")

        # Stop
        reporter.stop()

        # Verify all calls
        assert mock_logger.info.call_count == 4
        calls = [call[0][0] for call in mock_logger.info.call_args_list]
        assert calls[0] == "\nRunning experiment with 2 test cases..."
        assert calls[1] == '[1/2] Running test case: "Login Test"'
        assert calls[2] == '[2/2] Running test case: "Logout Test"'
        assert calls[3] == "Evaluation complete."


class TestRichProgressReporter:
    """Tests for RichProgressReporter."""

    @patch("gentrace.lib.progress.Console")
    @patch("gentrace.lib.progress.Progress")
    def test_init(self, _mock_progress_class: Any, mock_console_class: Any) -> None:
        """Test initialization of RichProgressReporter."""
        reporter = RichProgressReporter()

        assert reporter.console is not None
        assert reporter.progress is None
        assert reporter.task_id is None
        assert reporter.current_test_name == ""
        assert reporter.completed_count == 0
        mock_console_class.assert_called_once_with(stderr=True)

    @patch("gentrace.lib.progress.Live")
    @patch("gentrace.lib.progress.Console")
    @patch("gentrace.lib.progress.Progress")
    def test_start(self, mock_progress_class: Any, _mock_console_class: Any, mock_live_class: Any) -> None:
        """Test starting a new evaluation run with progress bar."""
        mock_progress = Mock()
        mock_task_id = 123
        mock_progress.add_task.return_value = mock_task_id
        mock_progress_class.return_value = mock_progress
        
        mock_live = Mock()
        mock_live_class.return_value = mock_live

        reporter = RichProgressReporter()
        
        # Mock _create_display to avoid rendering issues with mocked objects
        with patch.object(reporter, '_create_display', return_value=Mock()):
            reporter.start("pipeline-123", 50)

        assert reporter.progress is mock_progress
        assert reporter.task_id == mock_task_id
        assert reporter.completed_count == 0
        assert reporter.total_count == 50

        mock_progress.add_task.assert_called_once()
        mock_live.start.assert_called_once()

        # Check that the task was created with the right parameters
        call_args = mock_progress.add_task.call_args
        assert call_args[1]["total"] == 50
        assert call_args[1]["description"] == ""  # No description in the bar itself

    @patch("gentrace.lib.progress.Live")
    @patch("gentrace.lib.progress.Console")
    @patch("gentrace.lib.progress.Progress")
    def test_update_current_test(self, mock_progress_class: Any, mock_console_class: Any, mock_live_class: Any) -> None:
        """Test updating the current test display."""
        mock_progress = Mock()
        mock_progress_class.return_value = mock_progress
        mock_console = Mock()
        mock_console_class.return_value = mock_console
        mock_live = Mock()
        mock_live_class.return_value = mock_live

        reporter = RichProgressReporter()
        
        # Mock _create_display to avoid rendering issues with mocked objects
        with patch.object(reporter, '_create_display', return_value=Mock()):
            reporter.start("pipeline-123", 10)
            reporter.update_current_test("Login Test")

        assert reporter.current_test_name == "Login Test"
        
        # Verify live.update was called
        assert mock_live.update.called

    @patch("gentrace.lib.progress.Live")
    @patch("gentrace.lib.progress.Console")
    @patch("gentrace.lib.progress.Progress")
    def test_increment(self, mock_progress_class: Any, mock_console_class: Any, mock_live_class: Any) -> None:
        """Test incrementing the progress bar."""
        mock_progress = Mock()
        mock_progress_class.return_value = mock_progress
        mock_console = Mock()
        mock_console_class.return_value = mock_console
        mock_live = Mock()
        mock_live_class.return_value = mock_live

        reporter = RichProgressReporter()
        
        # Mock _create_display to avoid rendering issues with mocked objects
        with patch.object(reporter, '_create_display', return_value=Mock()):
            reporter.start("pipeline-123", 10)
            reporter.increment("Test 1")

        assert reporter.completed_count == 1
        assert reporter.last_completed_test == "Test 1"
        assert reporter.current_test_name == ""

        # Verify update was called with advance=1
        update_calls = mock_progress.update.call_args_list
        last_call = update_calls[-1]
        assert last_call[1]["advance"] == 1
        
        # Verify live.update was called
        assert mock_live.update.called

    @patch("gentrace.lib.progress.Live")
    @patch("gentrace.lib.progress.Console")
    @patch("gentrace.lib.progress.Progress")
    def test_stop(self, mock_progress_class: Any, mock_console_class: Any, mock_live_class: Any) -> None:
        """Test stopping the progress bar."""
        mock_progress = Mock()
        mock_progress_class.return_value = mock_progress
        mock_console = Mock()
        mock_console_class.return_value = mock_console
        mock_live = Mock()
        mock_live_class.return_value = mock_live

        reporter = RichProgressReporter()
        
        # Mock _create_display to avoid rendering issues with mocked objects
        with patch.object(reporter, '_create_display', return_value=Mock()):
            reporter.start("pipeline-123", 10)
            reporter.stop()

        assert reporter.progress is None
        assert reporter.task_id is None
        assert reporter.live is None

        mock_live.stop.assert_called_once()

        # Verify console.print was called with completion message
        print_calls = mock_console.print.call_args_list
        found_complete_msg = False
        for call in print_calls:
            if call[0] and "Evaluation complete" in str(call[0][0]):
                found_complete_msg = True
                break
        assert found_complete_msg

    @patch("gentrace.lib.progress.Live")
    @patch("gentrace.lib.progress.Console")
    @patch("gentrace.lib.progress.Progress")
    def test_start_with_url(self, mock_progress_class: Any, _mock_console_class: Any, mock_live_class: Any) -> None:
        """Test starting with an experiment URL."""
        mock_progress = Mock()
        mock_task_id = 999
        mock_progress.add_task.return_value = mock_task_id
        mock_progress_class.return_value = mock_progress
        
        mock_live = Mock()
        mock_live_class.return_value = mock_live

        reporter = RichProgressReporter()
        test_url = "https://gentrace.ai/t/org/pipeline/456/experiments/def"
        
        # Mock _create_display to avoid rendering issues with mocked objects
        with patch.object(reporter, '_create_display', return_value=Mock()):
            reporter.start("pipeline-456", 10, test_url)

        assert reporter.experiment_url == test_url
        assert reporter.total_count == 10
        mock_live.start.assert_called_once()

    @patch("gentrace.lib.progress.Live")
    @patch("gentrace.lib.progress.Console")
    @patch("gentrace.lib.progress.Progress")
    def test_full_lifecycle(self, mock_progress_class: Any, _mock_console_class: Any, mock_live_class: Any) -> None:
        """Test complete lifecycle of rich progress reporting."""
        mock_progress = Mock()
        mock_task_id = 456
        mock_progress.add_task.return_value = mock_task_id
        mock_progress_class.return_value = mock_progress
        mock_live = Mock()
        mock_live_class.return_value = mock_live

        reporter = RichProgressReporter()

        # Mock _create_display to avoid rendering issues with mocked objects
        with patch.object(reporter, '_create_display', return_value=Mock()):
            # Start evaluation
            reporter.start("pipeline-123", 3)

            # Process test cases
            reporter.update_current_test("Test 1")
            reporter.increment("Test 1")

            reporter.update_current_test("Test 2")
            reporter.increment("Test 2")

            reporter.update_current_test("Test 3")
            reporter.increment("Test 3")

            # Stop
            reporter.stop()

        # Verify lifecycle
        assert reporter.completed_count == 3
        assert reporter.progress is None
        assert reporter.task_id is None
        assert reporter.live is None

        mock_live.start.assert_called_once()
        mock_live.stop.assert_called_once()


class TestProgressReporterInterface:
    """Tests for the ProgressReporter abstract base class."""

    def test_interface_methods_exist(self) -> None:
        """Test that the interface defines all required methods."""
        assert hasattr(ProgressReporter, "start")
        assert hasattr(ProgressReporter, "increment")
        assert hasattr(ProgressReporter, "stop")

    def test_cannot_instantiate_abstract_class(self) -> None:
        """Test that ProgressReporter cannot be instantiated directly."""
        with pytest.raises(TypeError, match="Can't instantiate abstract class"):
            ProgressReporter()  # type: ignore

    def test_concrete_classes_implement_interface(self) -> None:
        """Test that concrete classes implement the required interface."""
        # SimpleProgressReporter
        simple_reporter = SimpleProgressReporter()
        assert callable(simple_reporter.start)
        assert callable(simple_reporter.increment)
        assert callable(simple_reporter.stop)
        assert callable(simple_reporter.update_current_test)

        # RichProgressReporter
        rich_reporter = RichProgressReporter()
        assert callable(rich_reporter.start)
        assert callable(rich_reporter.increment)
        assert callable(rich_reporter.stop)
        assert callable(rich_reporter.update_current_test)
