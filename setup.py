#!/usr/bin/env python

from os.path import dirname, join
import plyer

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

curdir = dirname(__file__)
packages = [
    'plyer',
    'plyer.platforms',
    'plyer.platforms.linux',
    'plyer.platforms.android',
    'plyer.platforms.win',
    'plyer.platforms.win.libs',
    'plyer.platforms.ios',
    'plyer.platforms.macosx',
]


setup(
    name='plyer',
    version=plyer.__version__,
    description='Platform-independant wrapper for platform-dependant APIs',
    long_description=open(join(curdir, 'README.rst')).read(),
    author='Kivy team',
    author_email='mat@kivy.org',
    url='https://plyer.readthedocs.org/en/latest/',
    packages=packages,
    package_data={'': ['LICENSE', 'README.rst']},
    package_dir={'plyer': 'plyer'},
    include_package_data=True,
    license=open(join(curdir, 'LICENSE')).read(),
    zip_safe=False,
    classifiers=(
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',

    ),
)
