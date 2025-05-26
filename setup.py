from setuptools import setup, find_packages

setup(
    name="lattice-crypto",
    version="0.1",
    packages=find_packages(include=["lattice_methods", "tests"]),
    install_requires=[
        "numpy",
        "sympy",
        "nbval",
    ],
)