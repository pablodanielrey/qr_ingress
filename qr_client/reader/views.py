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

def _verify_hmac(data):
    sdata = data.split(';')
    h = sdata[-1]
    original_data = data.replace(f"{h}",'')
    newh = _get_hmac_signature(original_data)
    
    logging.debug(f"data:{data}\nhash:{h}\noriginal:{original_data}\nnew h:{newh}")
    return h == newh


def index(request:HttpRequest):
    if request.method == 'GET':
        return render(request, 'reader.html')
    
    if request.method == 'POST':
        qrcode = request.POST['qrcode']
        logging.debug(f'QRCODE: {qrcode}')
        if _verify_hmac(qrcode):
            return redirect('reader:access_authorized')

    return redirect('reader:access_denied') 

def authorized(request):
    return render(request, 'authorized.html')

def denied(request):
    return render(request, 'denied.html')