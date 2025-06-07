"""Automatic tracing functionality for Gentrace using AST transformation."""

from __future__ import annotations

import sys
import uuid
import warnings
from typing import TYPE_CHECKING, Union, Literal, Callable, Optional, Sequence

from .types import AutoTraceModule
from .import_hook import GentraceFinder

if TYPE_CHECKING:
    from opentelemetry.trace import Tracer


def install_auto_tracing(
    modules: Union[Sequence[str], Callable[[AutoTraceModule], bool]],
    *,
    min_duration: float = 0,
    check_imported_modules: Literal['error', 'warn', 'ignore'] = 'error',
    tracer: Optional['Tracer'] = None,
    pipeline_id: Optional[str] = None,
) -> None:
    """Install automatic tracing for specified modules.
    
    Args:
        modules: Either a list of module name prefixes to trace, or a callable
                that returns True for modules that should be traced
        min_duration: Minimum duration in seconds for a function to be traced
        check_imported_modules: How to handle modules that have already been imported
        tracer: OpenTelemetry tracer to use (defaults to gentrace tracer)
        pipeline_id: Optional Gentrace pipeline ID to associate all auto-traced spans with.
                    Must be a valid UUID string if provided.
    """
    if isinstance(modules, Sequence):
        modules = modules_func_from_sequence(modules)  # type: ignore

    if not callable(modules):
        raise TypeError('modules must be a list of strings or a callable')

    if check_imported_modules not in ('error', 'warn', 'ignore'):
        raise ValueError('check_imported_modules must be one of "error", "warn", or "ignore"')
    
    # Validate pipeline_id if provided
    if pipeline_id is not None:
        try:
            uuid.UUID(pipeline_id)
        except ValueError as e:
            raise ValueError(
                f"pipeline_id must be a valid UUID string. Received: '{pipeline_id}'"
            ) from e

    if check_imported_modules != 'ignore':
        for module in list(sys.modules.values()):
            try:
                auto_trace_module = AutoTraceModule(module.__name__, module.__file__)
            except Exception:
                continue

            if modules(auto_trace_module):
                if check_imported_modules == 'error':
                    raise AutoTraceModuleAlreadyImportedException(
                        f'The module {module.__name__!r} matches modules to trace, but it has already been imported. '
                        f'Either call `install_auto_tracing` earlier, '
                        f"or set `check_imported_modules` to 'warn' or 'ignore'."
                    )
                else:
                    warnings.warn(
                        f'The module {module.__name__!r} matches modules to trace, but it has already been imported. '
                        f'Either call `install_auto_tracing` earlier, '
                        f"or set `check_imported_modules` to 'ignore'.",
                        AutoTraceModuleAlreadyImportedWarning,
                        stacklevel=2,
                    )

    min_duration_ns = int(min_duration * 1_000_000_000)
    finder = GentraceFinder(modules, min_duration_ns, tracer, pipeline_id)
    sys.meta_path.insert(0, finder)


def modules_func_from_sequence(modules: Sequence[str]) -> Callable[[AutoTraceModule], bool]:
    return lambda module: module.parts_start_with(list(modules))


class AutoTraceModuleAlreadyImportedException(Exception):
    pass


class AutoTraceModuleAlreadyImportedWarning(Warning):
    pass