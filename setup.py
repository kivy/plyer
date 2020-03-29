#!/usr/bin/env python
'''
Setup.py
========

For MacOS or iOS install additional dependency PyOBJus::

    pip install https://github.com/kivy/pyobjus/zipball/master

For Android install additional dependency PyJNIus::

    pip install https://github.com/kivy/pyjnius/zipball/master
'''

from os.path import dirname, join
import plyer
import io

EXTRA_OPTIONS = {}

try:
    from setuptools import setup
    EXTRA_OPTIONS = dict(
        EXTRA_OPTIONS, **{
            'extras_require': {
                'ios': ['pyobjus'],
                'macosx': ['pyobjus'],
                'android': ['pyjnius'],
                'dev': ['mock', 'flake8']
            }
        }
    )

except ImportError:
    from distutils.core import setup

CURDIR = dirname(__file__)
PACKAGES = [
    'plyer',
    'plyer.facades',
    'plyer.platforms',
    'plyer.platforms.linux',
    'plyer.platforms.android',
    'plyer.platforms.win',
    'plyer.platforms.win.libs',
    'plyer.platforms.ios',
    'plyer.platforms.macosx',
    'plyer.platforms.macosx.libs',
]

with io.open(join(CURDIR, "README.md"), encoding="utf8") as fd:
    README = fd.read()
with io.open(join(CURDIR, "CHANGELOG.md"), encoding="utf8") as fd:
    CHANGELOG = fd.read()

setup(
    name='plyer',
    version=plyer.__version__,
    description='Platform-independent wrapper for platform-dependent APIs',
    long_description=README + u"\n\n" + CHANGELOG + u"\n\n",
    long_description_content_type='text/markdown',
    author='Kivy team',
    author_email='mat@kivy.org',
    url='https://plyer.readthedocs.org/en/latest/',
    packages=PACKAGES,
    package_data={'': ['LICENSE', 'README.md']},
    package_dir={'plyer': 'plyer'},
    include_package_data=True,
    license=open(join(CURDIR, 'LICENSE')).read(),
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    **EXTRA_OPTIONS
)
