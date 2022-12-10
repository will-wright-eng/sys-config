# type: ignore[attr-defined]
"""Awesome `sys-config` is a Python cli/package created with https://github.com/TezRomacH/python-package-template"""

__author__ = """Will Wright"""
__email__ = "hello@sys-config.com"
__version__ = "0.1.2"

from importlib import metadata as importlib_metadata

from sys_config.main import ConfigHandler


def get_version() -> str:
    try:
        return importlib_metadata.version(__name__)
    except importlib_metadata.PackageNotFoundError:  # pragma: no cover
        return "unknown"


version: str = get_version()
