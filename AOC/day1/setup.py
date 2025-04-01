from setuptools import setup, Extension
from Cython.Build import cythonize

cpp_extension = Extension(
    name="extension",            # The module name: import extension
    sources=["cpp_extension.cpp"],
    language="c++",
)

setup(
    name="my_combined_package",
    version="1.0",
    ext_modules = cythonize("cy1.pyx", annotate=True) + [cpp_extension],
)

