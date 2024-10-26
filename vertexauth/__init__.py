from .core import foo, bar
from importlib.util import find_spec

if find_spec("claudette") is not None:
    from .optional import baz
    __all__ = ["foo","bar"]
else:
    __all__ = ["foo","bar","baz"]


    
