from qrtools import QR
import subprocess

import re
from plyer.facades import QRCode


class OSXQRCode(QRCode):
    qrCode = QR()
    data_decode = {
        'text': lambda data: data,
        'url': lambda data: data,
        'email': lambda data: data.replace(u"mailto:", u"")
            .replace(u"MAILTO:", u""),
        'emailmessage': lambda data: re.findall(
            u"MATMSG:(TO):(.*);(SUB):(.*);(BODY):(.*);;",
            data, re.IGNORECASE)[0],
        'telephone': lambda data: data.replace(u"tel:", u"")
            .replace(u"TEL:", u""),
        'geo': lambda data: re.findall(
            u"GEO:(.*),(.*)", data, re.IGNORECASE)[0],
        'bookmark': lambda data: re.findall(
            u"MEBKM:(TITLE):(.*);(URL):(.*);;", data, re.IGNORECASE)[0],
    }

    def _get_qr_data_type(self):
        return self.data_decode.keys()

    def _scan_code(self):
        raise NotImplementedError()

    def _scan_file(self, filelocation):
        if not filelocation:
            return

        self.qrCode.filename = filelocation
        self.qrCode.decode()

        data_list = self.data_decode[self.qrCode.data_type](self.qrCode.data)
        qr_data = data_list
        if self.qrCode.data_type in ('bookmark', 'emailmessage'):
            qr_data = dict(zip(data_list[::2], data_list[1::2]))

        return {
            'data_string': self.qrCode.data,
            'data_type': self.qrCode.data_type,
            'qr_data': qr_data
        }

    def _encode_qr(self, data, data_type, filename):
        if not data:
            return

        self.qrCode.data = data
        self.qrCode.data_type = data_type

        self.qrCode.filename = filename or self.qrCode.get_tmp_file()
        if not self.qrCode.filename.endswith('.png'):
            self.qrCode.filename += '.png'

        try:
            subprocess.Popen([
                '/usr/local/bin/qrencode',
                '-o', self.qrCode.filename,
                '-s', unicode(self.qrCode.pixel_size),
                '-m', unicode(self.qrCode.margin_size),
                '-l', self.qrCode.level,
                self.qrCode.data_to_string()
            ]).wait()
        except subprocess.CalledProcessError as e:
            return None

        return self.qrCode.filename


def instance():
    return OSXQRCode()
