"""Import hook for Gentrace auto-tracing."""

from __future__ import annotations

import ast
import sys
from types import ModuleType
from typing import TYPE_CHECKING, Any, Dict, Callable, Iterator, Optional, Sequence, cast
from dataclasses import dataclass
from importlib.abc import Loader, MetaPathFinder
from importlib.util import spec_from_loader
from importlib.machinery import ModuleSpec

from .types import AutoTraceModule
from .rewrite_ast import compile_source

if TYPE_CHECKING:
    from opentelemetry.trace import Tracer


@dataclass
class GentraceFinder(MetaPathFinder):
    """The import hook entry point, inserted into `sys.meta_path` to apply AST rewriting to matching modules."""
    
    modules_filter: Callable[[AutoTraceModule], bool]
    min_duration: int
    tracer: Optional['Tracer']
    pipeline_id: Optional[str] = None
    
    def find_spec(
        self, fullname: str, path: Optional[Sequence[str]], target: Optional[ModuleType] = None
    ) -> Optional[ModuleSpec]:
        """This is the method that is called by the import system."""
        for plain_spec in self._find_plain_specs(fullname, path, target):
            # Not all loaders have get_source, but it's an abstract method of the standard ABC InspectLoader.
            # In particular it's implemented by `importlib.machinery.SourceFileLoader`
            # which is provided by default.
            get_source = getattr(plain_spec.loader, 'get_source', None)
            if not callable(get_source):
                continue
                
            try:
                source = cast(str, get_source(fullname))
            except Exception:
                continue
                
            if not source:
                continue
                
            # We fully expect plain_spec.origin and self.get_filename(...)
            # to be the same thing (a valid filename), but they're optional.
            filename = plain_spec.origin
            if not filename:
                try:
                    filename = cast('Optional[str]', plain_spec.loader.get_filename(fullname))  # type: ignore
                except Exception:
                    pass
                    
            if not self.modules_filter(AutoTraceModule(fullname, filename)):
                return None  # tell the import system to try the next meta path finder
                
            try:
                tree = ast.parse(source)
            except Exception:
                # The plain finder gave us invalid source code. Try another one.
                continue
                
            filename = filename or f'<{fullname}>'
            
            try:
                execute = compile_source(tree, filename, fullname, self.min_duration, self.tracer, self.pipeline_id)
            except Exception:
                # Auto-tracing failed with an unexpected error. Ensure that this doesn't crash the whole application.
                return None  # tell the import system to try the next meta path finder
                
            loader = GentraceLoader(plain_spec, execute)
            return spec_from_loader(fullname, loader)
            
    def _find_plain_specs(
        self, fullname: str, path: Optional[Sequence[str]], target: Optional[ModuleType]
    ) -> Iterator[ModuleSpec]:
        """Yield module specs returned by other finders on `sys.meta_path`."""
        for finder in sys.meta_path:
            # Skip this finder or any like it to avoid infinite recursion.
            if isinstance(finder, GentraceFinder):
                continue
                
            try:
                plain_spec = finder.find_spec(fullname, path, target)
            except Exception:
                continue
                
            if plain_spec:
                yield plain_spec
                

@dataclass
class GentraceLoader(Loader):
    """An import loader produced by GentraceFinder which executes a modified AST of the module's source code."""
    
    plain_spec: ModuleSpec
    """A spec for the module that was returned by another meta path finder."""
    
    execute: Callable[[Dict[str, Any]], None]
    """A function which accepts module globals and executes the compiled code."""
    
    def exec_module(self, module: ModuleType):
        """Execute a modified AST of the module's source code in the module's namespace."""
        self.execute(module.__dict__)
        
    # This is required when `exec_module` is defined.
    # It returns None to indicate that the usual module creation process should be used.
    def create_module(self, spec: ModuleSpec):
        return None
        
    def get_code(self, _name: str):
        # `python -m` uses the `runpy` module which calls this method instead of going through the normal protocol.
        # So return some code which can be executed with the module namespace.
        # Here `__loader__` will be this object, i.e. `self`.
        source = '__loader__.execute(globals())'
        return compile(source, '<string>', 'exec', dont_inherit=True)
        
    def __getattr__(self, item: str):
        """Forward some methods to the plain spec's loader (likely a `SourceFileLoader`) if they exist."""
        if item in {'get_filename', 'is_package'}:
            return getattr(self.plain_spec.loader, item)
        raise AttributeError(item)