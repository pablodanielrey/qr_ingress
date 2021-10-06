import logging
import hashlib
import hmac
import os
logging.getLogger().setLevel(logging.DEBUG)

from django.shortcuts import render, redirect
from django.http import HttpRequest

from qr import qr, exceptions

# Create your views here.

def index(request:HttpRequest):
    if request.method == 'GET':
        return render(request, 'reader.html')
    
    if request.method == 'POST':
        qrcode = request.POST['qrcode']
        logging.debug(f'QRCODE: {qrcode}')

        try:
            m = qr.Message.from_string(qrcode)
            qrc = qr.QRCode.from_message(m.message)
        except exceptions.InvalidHash as e:
            logging.exception(e)
            return redirect('reader:invalid_qr')

        logging.debug(qrc.to_dict())
        if qrc._has_access():
            return redirect('reader:access_authorized')

        return redirect('reader:access_denied') 
    

def authorized(request):
    return render(request, 'authorized.html', {'timer':2})

def denied(request):
    return render(request, 'denied.html', {'timer':2})

def invalid(request):
    return render(request, 'invalid.html', {'timer':2})