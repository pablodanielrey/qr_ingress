
import os
import hashlib
import hmac

def _get_hmac_signature(data):
    s = os.environ.get('DJANGO_SECRET')
    bs = bytes(s, 'utf-8')
    h = hmac.new(bs, bytes(data,'utf-8'), hashlib.sha1).hexdigest()
    return h

def _verify_hmac(data):
    sdata = data.split(';')
    h = sdata[-1]
    original_data = data.replace(f";{h}",'')
    newh = _get_hmac_signature(original_data)
    return h == newh

if __name__ == '__main__':
    while True:
        print('Por favor ingrese su qr')
        qrdata = input()
        print(f"QR: {qrdata}")
        if _verify_hmac(qrdata):
            print('Código valido')
        else:
            print('Codigo Inválido')
