# dummy files to test Proxy + facades
dummy_facade = ('''\
class Dummy(object):
    def show(self):
        raise NotImplementedError()
''')


dummy = ('''
from plyer.facades import Dummy


class {plat}Dummy(Dummy):
    def show(self):
        return self

    def __str__(self, *args):
        return '{plat}'.lower()


def instance():
    return {plat}Dummy()
''')

from os import mkdir
from os.path import abspath, dirname, join
fac_path = join(
    dirname(dirname(abspath(__file__))),
    'facades'
)
plat_path = join(
    dirname(dirname(abspath(__file__))),
    'platforms'
)

# create Dummy facade
with open(join(fac_path, 'dummy.py'), 'w') as f:
    f.write(dummy_facade)

# create Dummy platform modules
for plat in {'android', 'ios', 'win', 'macosx', 'linux'}:
    with open(join(plat_path, plat, 'dummy.py'), 'w') as f:
        f.write(dummy.format(
            **{'plat': plat.title()}
        ))

# make Dummy facade available in plyer
injected = False
with open(join(fac_path, '__init__.py'), 'r+') as f:

    # make a backup of original file
    facades_old = f.readlines()

    # return to the beginning of a file and inject
    f.seek(0)
    for line in facades_old:
        # inject before the first importing (necessary for __all__)
        if line.startswith('from ') or line.startswith('import '):
            # if injected and on an import line,
            # proceed with default
            if injected:
                f.write(line)
                continue

            # injecting Dummy facade to plyer
            f.write(
                '\nfrom plyer.facades.dummy import Dummy\n'
                '__all__ += ("Dummy", )\n'
            )
            injected = True

        # write line by default
        f.write(line)
    f.truncate()

with open(join(fac_path, '__old_init__.py'), 'w') as f:
    f.write(''.join(facades_old))
