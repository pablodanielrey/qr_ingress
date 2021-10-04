import logging
import hashlib
import hmac
import os
logging.getLogger().setLevel(logging.DEBUG)

from django.shortcuts import render, redirect
from django.http import HttpRequest

# Create your views here.

def _get_hmac_signature(data):
    s = os.environ.get('DJANGO_SECRET')
    bs = bytes(s, 'utf-8')
    h = hmac.new(bs, bytes(data,'utf-8'), hashlib.sha1).hexdigest()
    return h

def _decode_qr(data):
    sdata = data.split(';')
    h = sdata[-1]
    original_data = data.replace(f"{h}",'')
    newh = _get_hmac_signature(original_data)
    
    decoded = {
        'data': data,
        'original_hash': h,
        'computed_hash': newh
    }
    for field in sdata:
        field_data = field.split(':')
        try:
            decoded[field_data[0]] = field_data[1]
        except IndexError as e:
            logging.warn(data, e)

    logging.debug(decoded)
    return decoded

def _verify_hmac(decoded):
    decoded['original_hash'] == decoded['computed_hash']




def index(request:HttpRequest):
    if request.method == 'GET':
        return render(request, 'reader.html')
    
    if request.method == 'POST':
        qrcode = request.POST['qrcode']
        logging.debug(f'QRCODE: {qrcode}')
        decoded = _decode_qr(qrcode)
        if not _verify_hmac(decoded):
            return redirect('reader:invalid_qr')
        


    return redirect('reader:access_denied') 

def authorized(request):
    return render(request, 'authorized.html', {'timer':2})

def denied(request):
    return render(request, 'denied.html', {'timer':2})

def invalid(request):
    return render(request, 'invalid.html', {'timer':2})