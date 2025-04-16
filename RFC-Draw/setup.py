from setuptools import setup

setup(
    name='RFC-Draw',
    description="A python3 program to draw images for SVG-RFC-1.2 diagrams",
    version='1.0',
    author='Nevil Brownlee',
    author_email="nevil.brownlee@gmail.com",
    packages=['RFC-Draw'],  #same as name
    install_requires=['setuptools','wheel'], #external packages as dependencies
   )
