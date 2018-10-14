'''
Add a build section to the plyer.__version__ with standard .dev0 string.
Versions are fetched from PyPI according to the current version of plyer.

If there has been a release e.g. 1.2.3 and we bump the version on master
to 1.2.4.dev0, this fetches all versions that start with 1.2.4 i.e. right
after the release none and via cronjob there will be a 1.2.4.0.dev0 release.
Afterwards 1.2.4.1.dev0, etc until we bump to e.g. 1.2.5.dev0.
'''

import ssl
import json
from os.path import join
from urllib.request import urlopen
import plyer

# pylint: disable=protected-access
ssl._create_default_https_context = ssl._create_unverified_context


def get_build_section():
    '''
    Get all versions from PyPI that start with X.Y.Z of the current version.
    '''

    response = urlopen("https://pypi.org/pypi/plyer/json")
    versions = list(json.loads(response.read())["releases"].keys())
    print("Found these versions on PyPI: '{}'".format(versions))

    # ordinary release starts with X.Y.Z
    # scheduled increment adds the fourth section
    current = len([v for v in versions if v.startswith(plyer.__version__)])
    return current


def replace_version():
    '''
    Replace current version with X.Y.Z.b.dev0, where b is a build number.
    '''

    with open(join('plyer', '__init__.py')) as init:
        lines = init.readlines()

    build = get_build_section()
    print("New build section number is '{}'".format(build))

    # get original version
    curv = plyer.__version__.split('.')

    # assemble new one without "dev"/"dev0" thingy
    new = '.'.join(
        curv[:2] + [
            curv[2].strip('.dev0').strip('.dev').strip('dev0').strip('dev')
        ]
    )

    # create standardized new version
    new = '.'.join([new, str(build), 'dev0'])
    print("New build version is '{}'".format(new))

    with open(join('plyer', '__init__.py'), 'w') as init:
        for line in lines:
            if not line.startswith('__version__'):
                init.write(line)
                continue
            init.write("__version__ = '{}'".format(new))


if __name__ == '__main__':
    replace_version()
