from setuptools import setup, Extension

setup(
    ext_modules=[Extension(
        name="aoc6cpp",
        sources=["aoc6.cpp"],
        language="c++",
        extra_compile_args=["-O3"],
    )]
)