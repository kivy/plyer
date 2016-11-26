from jnius import autoclass
from plyer.facades import Sysinfo
from plyer.platforms.android import activity

Build = autoclass('android.os.Build')
BuildVersion = autoclass('android.os.Build$VERSION')
BuildVersionCodes = autoclass('android.os.Build$VERSION_CODES')
System = autoclass('java.lang.System')
Environment = autoclass('android.os.Environment')
StatFs = autoclass('android.os.StatFs')
DisplayMetrics = autoclass('android.util.DisplayMetrics')
Context = autoclass('android.content.Context')
MemoryInfo = autoclass('android.app.ActivityManager$MemoryInfo')


class AndroidSysinfo(Sysinfo):

    def _model_info(self, alias=False):
        '''
        Returns the model info for example: ASUS_Z00ED
        Examples are given for Asus Zenphone 2 laser 5"
        * alias is ignored on android platform
        '''
        return Build.MODEL

    def _system_name(self):
        '''
        Returns the system's OS name.
        Since Android would show 'Linux' as system OS name usually,
        return "Android (Linux)" to avoid confusion with pure Linux platforms
        for example: Android (Linux)
        '''
        name = System.getProperty("os.name")
        if name.lower() == 'linux':
            name = "Android (Linux)"
        return name

    def _platform_info(self):
        '''
        Returns platform's name for example: ASUS_Z00E_2
        '''
        return Build.DEVICE

    def _processor_info(self):
        """Returns the information of processor as tuple-like object of
        * **model** *(str)*: CPU model name or '' (not implemented)
        * **manufacturer** *(str)*: manufacturer name
        * **arch** *(str)*: architecture info
        * **cores** *(int)*: number of physical cores or None (not implemented)
        for example:
        cpu_namedtuple(model='', manufacturer='qcom',
                       cores=None, arch='armeabi-v7a')
        """
        return self.CpuNamedTuple(model='', manufacturer=Build.HARDWARE,
                                  cores=None, arch=Build.CPU_ABI)

    def _version_info(self):
        '''
        Returns the version of OS in a tuple,
        for example: ('Android', '21', 'LOLLIPOP')

        There are multiple codenames for some SDK values
        e.g (21 L, 21 LOLLIPOP), so we will try to check
        for longer value, and break loop only then
        '''
        sdkint = BuildVersion.SDK_INT
        version = BuildVersion.RELEASE
        codename = ''
        try:
            codes = BuildVersionCodes()
            for field_name in dir(codes):
                field_value = getattr(BuildVersionCodes, field_name, '')
                # following type check may except on some fields
                # (codename is already aquired in tests on this point)
                # may consider using try-except here too
                if (type(field_value) == int) and (field_value == sdkint):
                    codename = field_name
                    if len(codename) > 2:
                        break
        except Exception as ex:
            if not codename:
                codename = "UNKNOWN"
        return ('Android', str(sdkint), codename)

    def _architecture_info(self):
        '''
        Returns the architecture in a tuple,
        for example: ('armeabi-v7a', 'armeabi')
        '''
        return (Build.CPU_ABI, Build.CPU_ABI2)

    def _device_name(self):
        '''
        Returns the device name, for example: asus ASUS_Z00ED
        '''
        return "{0} {1}".format(Build.MANUFACTURER, Build.MODEL)

    def _manufacturer_name(self, alias=False):
        '''
        Returns the manufacturer's name, for example: asus
        * alias is ignored on android platform
        '''
        return Build.MANUFACTURER

    def _kernel_version(self):
        '''
        Returns the kernel version, for example: 3.10.49-perf-g4186cc1
        '''
        return System.getProperty("os.version")

    def _storage_info(self, path=None):
        '''
        Returns the amount of available disk storage in bytes (int)
        * **path** is not implemented on this platform
        '''

        stat = StatFs(Environment.getDataDirectory().getPath())
        bytes_vailable = stat.getBlockSize() * stat.getBlockCount()

        return int(bytes_vailable)

    def _memory_info(self):
        '''
        Return total system memory (RAM) in bytes (int)
        '''
        context = activity.getApplicationContext()
        activity_manager = context.getSystemService(Context.ACTIVITY_SERVICE)
        mem_info = MemoryInfo()
        activity_manager.getMemoryInfo(mem_info)
        return int(mem_info.totalMem)

    def _screen_resolution(self):
        '''
        Returns the screen resolution as 2-tuple, for example: (720,1280)
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
