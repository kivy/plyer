# coding=utf-8
"""
Flash
-----
"""

from plyer.facades import Flash
from jnius import autoclass, cast
from plyer.platforms.android import activity, SDK_INT

if SDK_INT < 23: #use the deprecated api
    Camera = autoclass("android.hardware.Camera")
    CameraParameters = autoclass("android.hardware.Camera$Parameters")
    SurfaceTexture = autoclass("android.graphics.SurfaceTexture")
else:
    Context = autoclass('android.content.Context')

PackageManager = autoclass('android.content.pm.PackageManager')
pm = activity.getPackageManager()
flash_available = pm.hasSystemFeature(PackageManager.FEATURE_CAMERA_FLASH)

class AndroidFlash(Flash):
    _camera = None

    def _on(self):
        
        if self._camera is None:
            self._camera_open()
            if not self._camera:
                return
        
        if SDK_INT < 23:
            self._camera.setParameters(self._f_on)
        else:
            self._camera.setTorchMode(self._cameraid, True)

    def _off(self):
        
        if not self._camera:
            return
            
        if SDK_INT < 23:
            self._camera.setParameters(self._f_off)
        else:
            self._camera.setTorchMode(self._cameraid, False)

    def _release(self):
        if SDK_INT < 23:
            if not self._camera:
                return
            self._camera.stopPreview()
            self._camera.release()
            self._camera = None

    def _camera_open(self):         
        if not flash_available:
            return
        
        if SDK_INT < 23:   
            self._camera = Camera.open()
            self._f_on = self._camera.getParameters()
            self._f_off = self._camera.getParameters()
            self._f_on.setFlashMode(CameraParameters.FLASH_MODE_TORCH)
            self._f_off.setFlashMode(CameraParameters.FLASH_MODE_OFF)
            self._camera.startPreview()
            # Need this for Nexus 5
            self._camera.setPreviewTexture(SurfaceTexture(0))
        else:
            service = activity.getSystemService(Context.CAMERA_SERVICE)
            self._camera = cast('android.hardware.camera2.CameraManager', service)
            self._cameraid = self._camera.getCameraIdList()[0]

def instance():
    return AndroidFlash()
