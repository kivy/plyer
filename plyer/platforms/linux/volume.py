from subprocess import Popen, PIPE
from plyer.facades import Volume
from plyer.utils import whereis_exe

from os import environ


class VolumeSet(Volume):
    def _get_state(self):
        old_lang = environ.get('LANG')
        environ['LANG'] = 'C'

        status = {"Volume_Set": False}
  
        print("Set Volume(%) : ")
        dev = input()
        dev = str(dev)
        dev = "pactl set-sink-volume 0 " + dev + "%"
        try : 
              pactl_process = Popen(dev, shell=True)
        except :
                return status
        environ['LANG'] = old_lang

        status['Volume_Set'] = True

        return status

def instance():
    import sys
    if whereis_exe('pactl'):
        return VolumeSet()
    sys.stderr.write("pactl not found.")
    return Volume()
