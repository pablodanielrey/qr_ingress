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
        except exceptions.InvalidMessage as e:
            logging.exception(e)
            return redirect('reader:invalid_qr')


        logging.debug(qrc.to_dict())
        for k,v in qrc.to_dict().items():
            request.session[k] = v

        if qrc._has_access():
            return redirect('reader:access_authorized')

        return redirect('reader:access_denied') 
    

def authorized(request):
    context = {
        'timer': 12
    }
    for k,v in request.session.items():
        context[k] = v
    return render(request, 'authorized.html', context)

def denied(request):
    context = {
        'timer': 12
    }
    for k,v in request.session.items():
        context[k] = v

    return render(request, 'denied.html', context)

def invalid(request):
    context = {
        'timer': 12
    }
    for k,v in request.session.items():
        context[k] = v

    return render(request, 'invalid.html', context)