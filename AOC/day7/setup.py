from setuptools import setup, Extension

setup(
    ext_modules=[Extension(
        name="aoc7cpp",
        sources=["aoc7.cpp"],
        language="c++",
        extra_compile_args=["-O3"]
    )]
)