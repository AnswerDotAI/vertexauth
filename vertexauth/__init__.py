from .core import foo, bar
from importlib.util import find_spec as _find_spec

__all__ = ["foo","bar"]

if _find_spec("claudette") is not None:
    from .optional import baz
    __all__.append("baz")

if _find_spec("anthropic") is not None:
    from .optional import qux
    __all__.append("qux")



    
