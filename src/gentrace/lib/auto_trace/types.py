"""Types for auto-tracing functionality."""

from __future__ import annotations

from typing import List, Tuple, Union, Optional


class AutoTraceModule:
    """Information about a module that might be auto-traced."""
    
    def __init__(self, name: str, filename: Optional[str]):
        self.name = name
        self.filename = filename
        
    def parts_start_with(self, prefixes: Union[Tuple[str, ...], List[str]]) -> bool:
        """Check if the module name starts with any of the given prefixes."""
        parts = self.name.split('.')
        for prefix in prefixes:
            prefix_parts = prefix.split('.')
            if len(parts) >= len(prefix_parts) and parts[:len(prefix_parts)] == prefix_parts:
                return True
        return False