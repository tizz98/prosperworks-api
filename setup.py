#!/usr/bin/env python
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except (IOError, ImportError):
    with open('README.md') as f:
        long_description = f.read()

from prosperworks.constants import __version__


setup(
    name='prosperworks',
    version=__version__,
    description='A simple python wrapper for the ProsperWorks API',
    long_description=long_description,
    url='https://github.com/tizz98/prosperworks-api',
    download_url='https://github.com/tizz98/prosperworks-api/tarball/%s' % (
        __version__
    ),
    author='Elijah Wilson',
    author_email='elijah@elijahwilson.me',
    license='MIT',
    packages=['prosperworks'],
    keywords="prosperworks api",
    zip_safe=True,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],
    install_requires=[
        'requests',
    ]
)
