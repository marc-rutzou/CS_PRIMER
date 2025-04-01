from setuptools import setup, Extension

setup(ext_modules=[
    Extension(
        "aoc4cpp",
        ["aoc4cpp.cpp"],
        language="c++",
        extra_compile_args=["-O3"]
    )]
)
