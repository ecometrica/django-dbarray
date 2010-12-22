import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()
    
setup(
    name = "django-dbarray",
    version = "0.0.1",
    packages = find_packages(),
)