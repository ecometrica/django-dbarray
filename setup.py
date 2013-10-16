import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()
    
setup(
    name = "django-dbarray",
    version = "0.1",
    packages = find_packages(),
    description = "Django ORM field for Postgres array types.",
    author = "Ecometrica",
    author_email = "info@ecometrica.ca",
    maintainer = "Michael Mulley",
    maintainer_email = "michael@michaelmulley.com",
    url = "http://github.com/ecometrica/django-vinaigrette/",
    keywords = ["django", "model", "field", 
        "postgres", "postgresql", "database", "array", "list"],
    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: BSD License",
        "Operating System :: POSIX",
        "Topic :: Database",
        "Framework :: Django",
        ],
    long_description = read('README.rst'),
)
