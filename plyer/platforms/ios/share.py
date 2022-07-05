# coding=utf-8
"""
Share
-----
"""

from plyer.facades import Share
from plyer import storagepath
from pyobjus import autoclass
from pyobjus.objc_py_types import NSSize, NSRect, NSPoint
from typing import Tuple

NSURL = autoclass('NSURL')
UIApplication = autoclass('UIApplication')
UIDevice = autoclass('UIDevice')
currentDevice = UIDevice.currentDevice()
iPhone = currentDevice.userInterfaceIdiom == 0
iPad = currentDevice.userInterfaceIdiom == 1
sharedApplication = UIApplication.sharedApplication()

class IosShare(Share):

    def _write_data_to_file(self, data, out_file):
        with open(out_file, 'w') as ofile:
            ofile.write(data)


    def _share_text(self, text: str, title: str,
        size: Tuple[int, int]=(32, 32),
        pos:Tuple[int, int]=(200, 200),
        arrow_direction:int=0):
        self._share_file(text, None, title,
            size=size, pos=pos, arrow_direction=arrow_direction)

    def _share_file(
        self, data: str, filename: str, title: str,
        size: Tuple[int, int]=(32, 32),
        pos:Tuple[int, int]=(200, 200),
        arrow_direction:int=0):

        if not data:
            return

        if filename:
            out_file = storagepath.get_home_dir() + '/Documents/' + filename
            self._write_data_to_file(data, out_file)
            URL = NSURL.fileURLWithPath_(out_file)
            data = URL

        import gc 
        gc.collect()

        UIActivityViewController = autoclass('UIActivityViewController')
        UIActivityViewController_instance = UIActivityViewController.alloc().init()
        activityViewController = UIActivityViewController_instance.initWithActivityItems_applicationActivities_([data], None)
        UIcontroller = sharedApplication.keyWindow.rootViewController()
            

        if iPad:
            UIView = UIcontroller.view()
            UIActivityViewController_instance.modalPresentationStyle = 9# 9  is popover
            UIActivityViewController_instance.preferredContentSize = NSSize(0,0)
            pc = UIActivityViewController_instance.popoverPresentationController()
            pc.permittedArrowDirections = arrow_direction # 0 means no direction
            pc.sourceView = UIView
            val = NSRect()
            val.size = NSSize(*size)# Apsect ration?
            val.origin = NSPoint(*pos)
            pc.sourceRect = val
        
        UIcontroller.presentViewController_animated_completion_(activityViewController, True, None)
        gc.collect()
        


def instance():
    return IosShare()
