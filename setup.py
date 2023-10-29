"""Bootstrap setup script."""

import os
from setuptools import setup, find_packages

# Get the current version number from inside the module
with open(os.path.join('bootstrap', 'version.py')) as version_file:
    exec(version_file.read())

# Load the required dependencies from the requirements file
with open("requirements.txt") as requirements_file:
    install_requires = requirements_file.read().splitlines()

setup(
    name = 'bootstrap',
    version = __version__,
    description = 'Basic bootstraps for statistics.',
    long_description = 'Basic bootstraps for statistics.',
    python_requires = '>=3.6',
    author = 'Thomas Donoghue',
    author_email = 'tdonoghue.research@gmail.com',
    url = 'https://github.com/TomDonoghue/bootstrap',
    packages = find_packages(),
    license = 'MIT License',
    install_requires = install_requires,
    tests_require = ['pytest'],
    platforms = 'any',
)
