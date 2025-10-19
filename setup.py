"""Setup script for bootstrap."""

import os
from setuptools import setup, find_packages

# Get the current version number from inside the module
with open(os.path.join('bootstrap', 'version.py')) as version_file:
    exec(version_file.read())

# Load the long description from the README
with open('README.rst') as readme_file:
    long_description = readme_file.read()

# Load the required dependencies from the requirements file
with open("requirements.txt") as requirements_file:
    install_requires = requirements_file.read().splitlines()

setup(
    name = 'bootstrap',
    version = __version__,
    description = 'Basic bootstraps for statistics.',
    long_description = long_description,
    long_description_content_type = 'text/x-rst',
    python_requires = '>=3.7',
    author = 'Thomas Donoghue',
    author_email = 'tdonoghue.research@gmail.com',
    url = 'https://github.com/TomDonoghue/bootstrap',
    packages = find_packages(),
    license = 'MIT License',
    download_url = 'https://github.com/TomDonoghue/bootstrap/releases',
    keywords = ['statistics'],
    install_requires = install_requires,
    tests_require = ['pytest'],
    classifiers = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: MacOS',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Programming Language :: Python :: 3.14',
        ],
    platforms = 'any',
    project_urls = {
        'Bug Reports' : 'https://github.com/TomDonoghue/bootstrap/issues',
        'Source' : 'https://github.com/TomDonoghue/bootstrap',
    },
)
