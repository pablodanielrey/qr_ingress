
import sys
import os

from qr.qr import QRCode, Message

import qrcode
import qrcode.image.svg
from io import BytesIO

def generate_qr(data):
    factory = qrcode.image.svg.SvgImage
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=20,
        border=4,
        image_factory=factory
    )
    qr.add_data(data)
    image = qr.make_image()
    return image

if __name__ == '__main__':
    url = sys.argv[1]
    f = sys.argv[2]


    print('QR de acceso permitido')
    qr = QRCode('Pablo', 'Rey', 10.0)
    m = Message(qr.to_message())
    print(m.to_string())
    qr = generate_qr(m.to_string())

    # stream = BytesIO()
    # image.save(stream)
    # data = stream.getvalue().decode()
    with open(f"{f}_permitido.svg",'wb') as qrfile:
        qr.save(qrfile)


    print('QR de acceso denegado')
    qr = QRCode('Pablo', 'Rey', 1.1)
    m = Message(qr.to_message())
    print(m.to_string())
    qr = generate_qr(m.to_string())

    # stream = BytesIO()
    # image.save(stream)
    # data = stream.getvalue().decode()
    with open(f"{f}_denegado.svg",'wb') as qrfile:
        qr.save(qrfile)
