
import sys
import os

import qrcode
import qrcode.image.svg
from io import BytesIO

import hashlib
import hmac

def _get_hmac_signature(data):
    s = os.environ.get('DJANGO_SECRET')
    bs = bytes(s, 'utf-8')
    h = hmac.new(bs, bytes(data,'utf-8'), hashlib.sha1).hexdigest()
    return h


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
    qr.add_data(";")
    qr.add_data(_get_hmac_signature(data))    
    image = qr.make_image()
    return image

if __name__ == '__main__':
    url = sys.argv[1]
    f = sys.argv[2]
    qr = generate_qr(url)

    # stream = BytesIO()
    # image.save(stream)
    # data = stream.getvalue().decode()
    with open(f"{f}.svg",'wb') as qrfile:
        qr.save(qrfile)
