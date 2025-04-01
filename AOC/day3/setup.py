from setuptools import setup, Extension

setup(
    ext_modules=[
        Extension(
            "aoc3cpp",
            ["aoc3cpp.cpp"],
            language="c++",
            extra_compile_args=["-O3"]
        )
    ]
)
