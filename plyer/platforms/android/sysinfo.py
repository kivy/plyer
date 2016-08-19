from jnius import autoclass
from plyer.facades import Sysinfo

Build = autoclass('android.os.Build')
BuildVersion = autoclass('android.os.Build$VERSION')
BuildVersionCodes = autoclass('android.os.Build$VERSION_CODES')
System = autoclass('java.lang.System')
Environment = autoclass('android.os.Environment')
StatsFs = autoclass('android.os.StatsFs')
DisplayMetrics = autoclass('android.util.DisplayMetrics')


class AndroidSysinfo(Sysinfo):

    def _model_info(self):
        '''
        Returns the model info for example:
        '''
        return Build.MODEL

    def _system_name(self):
        '''
        Returns the system's OS name for example:
        '''
        return System.getProperty("os.name")

    def _platform_info(self):
        '''
        Returns platform's name for example:
        '''
        return Build.DEVICE

    def _processor_info(self):
        '''
        Returns the type of processor for example:
        '''
        return Build.CPU_ABI

    def _version_info(self):
        '''
        Returns the version of OS in a tuple for example:
        '''
        sdkint = BuildVersion.SDK_INT
        version = BuildVersion.RELEASE
        try:
            fields = BuildVersionCodes.class.getFields()
            for field in fields:
                fieldName = field.getName()
                fieldValue = field.getInt()

                if (fieldValue == sdkint):
                    return ('Android', str(sdkint), fieldName)
        except:
            return ('Android', str(sdkint), "UNKNOWN")

    def _architecture_info(self):
        '''
        Returns the architecture in a tuple for example:
        '''
        return (Build.CPU_ABI, Build.CPU_ABI2)

    def _device_name(self):
        '''
        Returns the device name for example:
        '''
        return str(Build.MANUFACTURER) + " " + str(Build.MODEL)

    def _manufacturer_name(self):
        '''
        Returns the manufacturer's name for example:
        '''
        return Build.MANUFACTURER

    def _kernel_version(self):
        '''
        Returns the kernel version for example:
        '''
        return System.getProperty("os.version")

    def _storage_info(self):
        '''
        Returns the amount of storage (RAM) in GB. for example:
        '''
        stat = StatsFs(Environment.getDataDirectory().getPath())
        bytesAvailable = stat.getBlockSize() * stat.getBlockCount()
        megAvailable = bytesAvailable / 1048576
        return str(megAvailable)

    def _screen_resolution(self):
        '''
        Returns the screen resolution for example:
        '''
        dm = DisplayMetrics()
        getWindowManager.getDefaultDisplay().getMetrics(dm)
        wid = int(dm.widthPixels)
        hei = int(dm.heightPixels)
        return (wid, hei)


def instance():
    return AndroidSysinfo()
