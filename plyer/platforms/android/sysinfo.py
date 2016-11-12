from jnius import autoclass
from plyer.facades import Sysinfo
from plyer.platforms.android import activity

Build = autoclass('android.os.Build')
BuildVersion = autoclass('android.os.Build$VERSION')
BuildVersionCodes = autoclass('android.os.Build$VERSION_CODES')
System = autoclass('java.lang.System')
Environment = autoclass('android.os.Environment')
StatsFs = autoclass('android.os.StatFs')
DisplayMetrics = autoclass('android.util.DisplayMetrics')
Context = autoclass('android.content.Context')


class AndroidSysinfo(Sysinfo):

    def _model_info(self):
        '''
        Returns the model info for example: ASUS_Z00ED
        Examples are given for Asus Zenphone 2 laser 5"
        '''
        return Build.MODEL

    def _system_name(self):
        '''
        Returns the system's OS name for example: Linux
        '''
        return System.getProperty("os.name")

    def _platform_info(self):
        '''
        Returns platform's name for example: ASUS_Z00E_2
        '''
        return Build.DEVICE

    def _processor_info(self):
        '''
        Returns the type of processor for example: armeabi-v7a
        '''
        return Build.CPU_ABI

    def _version_info(self):
        '''
        Returns the version of OS in a tuple for example:
        '''
        sdkint = BuildVersion.SDK_INT
        version = BuildVersion.RELEASE
        try:
            fields = BuildVersionCodes.getClass().getFields()
            for field in fields:
                fieldName = field.getName()
                fieldValue = field.getInt()

                if (fieldValue == sdkint):
                    return ('Android', str(sdkint), fieldName)
        except Exception as ex:
            # WARNING TEST
            # from kivy.logger import Logger
            # Logger.error('plyer: could not get version code: {0}'.format(ex))
            return ('Android', str(sdkint), "UNKNOWN")

    def _architecture_info(self):
        '''
        Returns the architecture in a tuple,
        for example: ('armeabi-v7a', 'armeabi')
        '''
        return (Build.CPU_ABI, Build.CPU_ABI2)

    def _device_name(self):
        '''
        Returns the device name for example: asus ASUS_Z00ED
        '''
        return str(Build.MANUFACTURER) + " " + str(Build.MODEL)

    def _manufacturer_name(self):
        '''
        Returns the manufacturer's name for example: asus
        '''
        return Build.MANUFACTURER

    def _kernel_version(self):
        '''
        Returns the kernel version for example: 3.10.49-perf-g4186cc1
        '''
        return System.getProperty("os.version")

    def _storage_info(self):
        '''
        Returns the amount of storage (RAM) in GB. for example:
        NOTE WARNING this doesn't seem to return GBs of RAM.
        My phone reports 10610. Fuyou.
        '''
        stat = StatsFs(Environment.getDataDirectory().getPath())
        bytesAvailable = stat.getBlockSize() * stat.getBlockCount()
        megAvailable = bytesAvailable / 1048576
        return str(megAvailable)

    def _screen_resolution(self):
        '''
        Returns the screen resolution as list, for example: [720,1280]
        '''
        dm = DisplayMetrics()
        context = activity.getApplicationContext()
        wm = context.getSystemService(Context.WINDOW_SERVICE)
        wm.getDefaultDisplay().getMetrics(dm)
        wid = int(dm.widthPixels)
        hei = int(dm.heightPixels)
        return (wid, hei)


def instance():
    return AndroidSysinfo()
