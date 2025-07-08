from importlib import import_module
_registry = {}
def register(name):
    def _wrap(fn):
        _registry[name] = fn
        return fn
    return _wrap
def get_engine(name):
    return _registry.get(name)

from . import shopify, woocommerce  # auto-register 