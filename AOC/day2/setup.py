from Cython.Build import cythonize
from setuptools import setup, Extension

setup(ext_modules = cythonize("aoc2cy.pyx", annotate=True))

setup(
    ext_modules=[
        Extension(
            "aoc2cpp", 
            ["aoc2cpp.cpp"], 
            language="c++",
            extra_compile_args=["-O3"]
        )
    ],
)

