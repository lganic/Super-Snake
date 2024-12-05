# setup.py
from setuptools import setup, Extension
import sys
import pybind11

from pybind11.setup_helpers import Pybind11Extension, build_ext

ext_modules = [
    Pybind11Extension(
        "hamilton_cycle_module",
        ["src/cpp/bindings.cpp"],
        # Example: passing in the version to the compiled code
        define_macros=[('VERSION_INFO', "0.0.1")],
    ),
]

setup(
    name="hamilton_cycle_module",
    version="0.0.1",
    author="Your Name",
    author_email="your.email@example.com",
    description="A Python module to find Hamiltonian cycles using C++",
    ext_modules=ext_modules,
    cmdclass={"build_ext": build_ext},
    zip_safe=False,
)
