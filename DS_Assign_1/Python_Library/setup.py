from setuptools import find_packages, setup
setup(
    name='myQueue',
    packages=find_packages(include=['myQueue']),
    version='0.1.0',
    description='Library for Queue implementation- DS assignment 1',
    install_requires=['requests'],
    author='Rupinder Goyal',
)