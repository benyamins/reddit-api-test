"""
    Can't do `python -m reddit.api`. This will trigger runtime warning.
    In case of needing to import in __init__, one must run the package
    as a module with `python -m reddit`. So the logic must be placed
    in __main__.py.

    See: https://stackoverflow.com/questions/43393764/
"""
# from .db import DBConnection
