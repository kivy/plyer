from qrtools import QR
import subprocess

import re
from plyer.facades import QRCode


class LinuxQRCode(QRCode):
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
        qr_code = QR()
        qr_code.decode_webcam()

        data_list = self.data_decode[qr_code.data_type](qr_code.data)
        qr_data = data_list
        if qr_code.data_type in ('bookmark', 'emailmessage'):
            qr_data = dict(zip(data_list[::2], data_list[1::2]))

        return {
            'data_string': qr_code.data,
            'data_type': qr_code.data_type,
            'qr_data': qr_data
        }

    def _scan_file(self, filelocation):
        qr_code = QR()

        if not filelocation:
            return

        qr_code.filename = filelocation
        qr_code.decode()

        data_list = self.data_decode[qr_code.data_type](qr_code.data)
        qr_data = data_list
        if qr_code.data_type in ('bookmark', 'emailmessage'):
            qr_data = dict(zip(data_list[::2], data_list[1::2]))

        return {
            'data_string': qr_code.data,
            'data_type': qr_code.data_type,
            'qr_data': qr_data
        }

    def _encode_qr(self, data, data_type, filename):
        qr_code = QR()

        if not data:
            return

        qr_code.data = data
        qr_code.data_type = data_type

        qr_code.filename = filename or qr_code.get_tmp_file()
        if not qr_code.filename.endswith('.png'):
            qr_code.filename += '.png'

        try:
            subprocess.Popen([
                '/usr/bin/qrencode',
                '-o', qr_code.filename,
                '-s', unicode(qr_code.pixel_size),
                '-m', unicode(qr_code.margin_size),
                '-l', qr_code.level,
                qr_code.data_to_string()
            ]).wait()
        except subprocess.CalledProcessError as e:
            return None

        return qr_code.filename


def instance():
    return LinuxQRCode()
