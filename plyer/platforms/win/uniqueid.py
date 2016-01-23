try:
    import _winreg as regedit
except:
    try:
        import winreg as regedit
    except:
        raise NotImplemented()

from plyer.facades import UniqueID


class WinUniqueID(UniqueID):
    def _get_uid(self):
        hKey = regedit.OpenKey(regedit.HKEY_LOCAL_MACHINE,
            r"SOFTWARE\\Microsoft\\Cryptography", 0,
            regedit.KEY_READ | regedit.KEY_WOW64_64KEY)
        value, _ = regedit.QueryValueEx(hKey, "MachineGuid")
        return value


def instance():
    return WinUniqueID()
