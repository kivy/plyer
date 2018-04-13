'''
    Note::
        This facade depends on:
        - nmcli (Network Manager command line tool)
            It is found in most of the popular distros. Support for other
            managers is not provided yet.
    One more thing: Betalistish!!
'''
#from __future__ import print_function
from plyer.facades import Wifi
from subprocess import Popen, PIPE, call, STDOUT
import glob, re

class LinuxWifi(Wifi):
    names = {}
    interface = glob.glob('/sys/class/net/*/wireless')[0][15:-9]
    def enable(self):
        return call(['nmcli', 'r', 'wifi', 'on'])

    def disable(self):
        return call(['nmcli', 'r', 'wifi', 'off'])

    def keys(self):
        return ('None' if len(self.names) is 0 else self.names)

    def _is_enabled(self):
        '''
        Returns `True` if wifi is enabled else `False`.
        '''
        enbl = Popen(["nmcli", "radio", "wifi"], stdout=PIPE, stderr=PIPE)
        if enbl.communicate()[0].split()[0].decode("utf-8") == "enabled":
            return True
        else:
            self.enable()
            return True
        return False
    def get_wifi(self):
        r = Popen(["iwlist", self.interface, "scan"], stdout=PIPE, stderr=PIPE)
        r = r.communicate()[0].decode("utf-8")
        r = [e.strip().split('\n')[0] for e in r.splitlines()]
        if len(r) is 1:
            self.get_wifi()
        del r[0] #getting rid of scan complete
        return r
    def _start_scanning(self):
        error = "{'error', 'Your WiFi is being busy at the moment. Try again in a little while.'}"
        r = self.get_wifi()
        b = {}
        c = {}
        i = 0
        for v in r:
            if not re.search(r"Cell %s" % v[5:7], ''.join(v)):
                if v.count(':') is 1:
                    """ If only one colon found for splitting"""
                    if v.count('=') > 0:
                        if v.count('=') < 2:
                            """ Splitting Extra:tsf=000001a1166da2f4 into: 'Extra': '000001a1166da2f4' """
                            b[v.split(':')[0].strip(' ').lower().replace(' ','_')] = v.split('=')[1].replace('"','').strip(' ')
                    else:
                        b[v.split(':',1)[0].strip(' ').lower().replace(' ','_').replace('(','').replace(')','')] = v.split(':',1)[1].replace('"','').strip(' ') #Split of Mode:Master
                elif v.count('=') > 1:
                    # Chopping Quality=26/70  Signal level=-84 dBm
                    b['quality'] = v.split('=')[1].replace('"','').split(' ')[0].strip(' ')
                    b['signal'] = v.split('=',2)[2].strip(' ')
            else:
                i += 1 #Note: Had to play mind-games for getting it right
                if i > 1:
                    b.update({'address':v.replace(v[:len(v)-17],'').strip()})
                    c[i-1] = b.copy() if len(b) > 0 else error #Copying dict(b) to c[1..100]
                    b.clear()
        '''
        Returns all the network information.
        '''
        if self._is_enabled():
            for i in c:
                self.names[c[i]['essid']] = c[i]
        else:
            raise Exception('Wifi not enabled.')

    def _get_network_info(self, name):
        '''
        Starts scanning for available Wi-Fi networks and returns the available,
        devices.
        '''
        ret_list = {}
        ret_list['ssid'] = self.names[name]['essid']
        ret_list['signal'] = self.names[name]['signal']
        ret_list['quality'] = self.names[name]['quality']
        ret_list['frequency'] = self.names[name]['frequency']
        ret_list['bitrates'] = self.names[name]['bit_rates']
        ret_list['encrypted'] = self.names[name]['encryption_key']
        ret_list['channel'] = self.names[name]['channel']
        ret_list['address'] = self.names[name]['address']
        ret_list['mode'] = self.names[name]['mode']
        if not ret_list['encrypted']:
            return ret_list
        else:
            ret_list['encryption_type'] = self.names[name]['authentication_suites_1']
            return ret_list

    def _get_available_wifi(self):
        '''
        Returns the name of available networks.
        '''
        return ('None' if len(self.names) is 0 else self.names)

    def _connect(self, network, parameters):
        '''
        Expects 2 parameters:
            - name/ssid of the network.
            - parameters:
                - password: dict type
        '''
        try:
            self.enable()
        finally:
            password = parameters['password']
            cell = self.names[network]
            call(['nmcli', 'device', 'wifi', 'connect', network, 'password', password])
            return 'And we are connected'

    def _disconnect(self):
        '''
        Disconnect all the networks managed by Network manager.
        '''
        return self.disable()


def instance():
    import sys
    try:
        return LinuxWifi()
    except ImportError:
        sys.stderr.write("Oh look a penny..")
    return Wifi()