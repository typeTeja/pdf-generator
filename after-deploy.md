
-----

WeasyPrint could not import some external libraries. Please carefully follow the installation steps before reporting an issue:
https://doc.courtbouillon.org/weasyprint/stable/first_steps.html#installation
https://doc.courtbouillon.org/weasyprint/stable/first_steps.html#troubleshooting 

-----

2026-05-27 17:34:27,110 [ERROR] pdf_microservice: Failed to import WeasyPrint. This usually means system libraries (libpango, libcairo, etc.) are missing. Error: OSError: cannot load library 'libgobject-2.0-0': libgobject-2.0-0: cannot open shared object file: No such file or directory.  Additionally, ctypes.util.find_library() did not manage to locate a library called 'libgobject-2.0-0'
2026-05-27 17:34:27,116 [ERROR] pdf_microservice: Traceback (most recent call last):
  File "/app/app/main.py", line 38, in <module>
    import weasyprint
  File "/opt/venv/lib/python3.12/site-packages/weasyprint/__init__.py", line 372, in <module>
    from .css import preprocess_stylesheet  # noqa: I001, E402
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/venv/lib/python3.12/site-packages/weasyprint/css/__init__.py", line 29, in <module>
    from ..text.fonts import FontConfiguration
  File "/opt/venv/lib/python3.12/site-packages/weasyprint/text/fonts.py", line 17, in <module>
    from .constants import (  # isort:skip
  File "/opt/venv/lib/python3.12/site-packages/weasyprint/text/constants.py", line 5, in <module>
    from .ffi import pango
  File "/opt/venv/lib/python3.12/site-packages/weasyprint/text/ffi.py", line 476, in <module>
    gobject = _dlopen(
              ^^^^^^^^
  File "/opt/venv/lib/python3.12/site-packages/weasyprint/text/ffi.py", line 464, in _dlopen
    return ffi.dlopen(names[0], flags)  # pragma: no cover
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/venv/lib/python3.12/site-packages/cffi/api.py", line 150, in dlopen
    lib, function_cache = _make_ffi_library(self, name, flags)
                          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/venv/lib/python3.12/site-packages/cffi/api.py", line 834, in _make_ffi_library
    backendlib = _load_backend_lib(backend, libname, flags)
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/venv/lib/python3.12/site-packages/cffi/api.py", line 829, in _load_backend_lib
    raise OSError(msg)
OSError: cannot load library 'libgobject-2.0-0': libgobject-2.0-0: cannot open shared object file: No such file or directory.  Additionally, ctypes.util.find_library() did not manage to locate a library called 'libgobject-2.0-0'

INFO:     Started server process [1]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
