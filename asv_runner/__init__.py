# Version fallback for source-tree imports. Built artifacts do not
# execute this: pdm-backend (tool.pdm.version.write_to) replaces this
# file with a static ``__version__ = '<tag>'`` at build time.
try:
    from importlib.metadata import PackageNotFoundError, version
except ImportError:  # Python < 3.8
    from importlib_metadata import PackageNotFoundError, version

try:
    __version__ = version("asv_runner")
except PackageNotFoundError:
    # Source tree without installed distribution metadata.
    __version__ = "0.0.0.dev0"

del PackageNotFoundError, version
