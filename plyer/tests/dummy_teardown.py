from os import remove
from os.path import abspath, dirname, join
fac_path = join(
    dirname(dirname(abspath(__file__))),
    'facades'
)
plat_path = join(
    dirname(dirname(abspath(__file__))),
    'platforms'
)

# remove Dummy facade
remove(join(fac_path, 'dummy.py'))

# remove Dummy platform modules
for plat in {'android', 'ios', 'win', 'macosx', 'linux'}:
    remove(join(plat_path, plat, 'dummy.py'))

with open(join(fac_path, '__old_init__.py')) as f:
    facades_old = f.read()
remove(join(fac_path, '__old_init__.py'))

# restore the original facades __init__.py
with open(join(fac_path, '__init__.py'), 'w') as f:
    f.write(''.join(facades_old))
