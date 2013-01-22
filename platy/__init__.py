from os import plateform

if plateform == 'android':
    from android import *
elif plateform == 'ios':
    from ios import *
else:
    from desktop import *
