from setuptools import setup, find_packages

setup(
    name="api",
    version="0.1",
    packages=find_packages(),
    install_requires=['Django>=2.1'],
    zip_safe=False
)