from setuptools import setup, Extension

setup(
    ext_modules=[Extension(
        "aoc5cpp",
        ["aoc5cpp.cpp"],
        language="c++",
        extra_compile_args=["-O3"],
        # extra_compile_args=["-O0", "-g", "-fno-omit-frame-pointer", "-fno-inline"],
    )]
)