import re

import kivy
from kivy.properties import StringProperty, ObjectProperty, ListProperty

kivy.require('1.8.0')

from kivy.app import App
from kivy.garden.xpopup.file import XFileOpen

from kivy.uix.boxlayout import BoxLayout

from plyer import qrcode


class QRCodeDemo(BoxLayout):
    file_location = StringProperty()
    manager = ObjectProperty(None)
    qr_data_type = ListProperty()

    def __init__(self, **kwargs):
        super(QRCodeDemo, self).__init__(**kwargs)
        self.ids.qr_type_select = [{'text': str(x)} for x in range(100)]
        self.qr_data_type = qrcode.get_qr_data_type()

    def open_filepopup(self):
        from os.path import expanduser
        XFileOpen(on_dismiss=self._filepopup_callback,
                  path=expanduser(u'~/'))

    def open_webcam(self):
        print qrcode.scan_code()

    def encode(self):
        data = {
            'text': lambda: self.ids.qr_text.text,
            'url': lambda: self.ids.qr_url.text,
            'email': lambda: self.ids.qr_email.text,
            'emailmessage': lambda: [self.ids.qr_email_to.text,
                                     self.ids.qr_email_sub.text,
                                     self.ids.qr_email_body.text],
            'bookmark': lambda: [self.ids.qr_bookmark_title.text,
                                 self.ids.qr_bookmark_url.text],
            'geo': lambda: [self.ids.qr_get_lat.text,
                            self.ids.qr_get_lon.text],
        }[self.manager.current]()
        file_location = qrcode.encode_qr(data, self.manager.current)
        self.file_location = file_location

    def update_qr_type(self, text):
        self.manager.current = text

    def _filepopup_callback(self, instance):
        if instance.is_canceled():
            return

        self.file_location = str(instance.selection[0])
        print qrcode.scan_file(instance.selection[0])


class QRCodeDemoApp(App):
    def build(self):
        return QRCodeDemo()


if __name__ == '__main__':
    QRCodeDemoApp().run()
