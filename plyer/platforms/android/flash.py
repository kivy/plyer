# coding=utf-8
"""
Flash
-----
"""

from plyer.facades import Flash
from jnius import autoclass
from plyer.platforms.android import activity
from plyer.platforms.android import SDK_INT
if SDK_INT >= 23:
  Context = autoclass('android.content.Context')
  CameraManager = activity.getSystemService(Context.CAMERA_SERVICE)
  CameraCharacteristics = autoclass("android.hardware.camera2.CameraCharacteristics")
  CamId = CameraManager.getCameraIdList()[0] # First Camera
  flash_available = CameraManager.getCameraCharacteristics(CamId).get(CameraCharacteristics.FLASH_INFO_AVAILABLE)
else :
  Camera = autoclass("android.hardware.Camera")
  CameraParameters = autoclass("android.hardware.Camera$Parameters")
  SurfaceTexture = autoclass("android.graphics.SurfaceTexture")
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
        if SDK_INT >= 23:
          CameraManager.setTorchMode(self._camera, True)
        else:
          self._camera.setParameters(self._f_on)
           
    def _off(self):
        if not self._camera:
            return
        if SDK_INT >= 23:
          CameraManager.setTorchMode(self._camera, False)
        else:
          self._camera.setParameters(self._f_off)

    def _release(self):
        if not self._camera:
            return
        if SDK_INT < 23:
          self._camera.stopPreview()
          self._camera.release()
        self._camera = None

    def _camera_open(self):
        if not flash_available:
            return
        if SDK_INT  >= 23 :
          self._camera = CamId
        else:
          self._camera = Camera.open()
          self._f_on = Camera.getParameters()
          self._f_off = Camera.getParameters()
          self._f_on.setFlashMode(CameraParameters.FLASH_MODE_TORCH)
          self._f_off.setFlashMode(CameraParameters.FLASH_MODE_OFF)
          self._camera.startPreview()
          # Need this for Nexus 5
          self._camera.setPreviewTexture(SurfaceTexture(0))


def instance():
    return AndroidFlash()
