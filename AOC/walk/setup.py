from setuptools import setup, Extension

setup(ext_modules = [Extension("aoc_cpp", ["aoc.cpp"], extra_compile_args=["-O3"])])

