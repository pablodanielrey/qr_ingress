import logging
import datetime
from zoneinfo import ZoneInfo

from django.shortcuts import render, redirect
from django.http import HttpRequest, JsonResponse

from qr_common import qr, exceptions

from .models import Access, SyncModel

# Create your views here.

TIMER = 1

def registrar_acceso(qrc:qr.QRCode):
    logging.debug(qrc.to_dict())
    a = Access(
        access=datetime.datetime.now(tz=ZoneInfo("America/Argentina/Buenos_Aires")),
        firstname=qrc.firstname,
        lastname=qrc.lastname,
        username=qrc.username,
        email=qrc.email,
        number=qrc.id_number,
        grade=qrc.grade,
        timestamp=qrc.timestamp
    )
    a.save()

def index(request:HttpRequest):
    if request.method == 'GET':
        return render(request, 'reader.html')
    
    if request.method == 'POST':
        qrcode = request.POST['qrcode']
        logging.debug(f'QRCODE: {qrcode}')

        try:
            m = qr.Message.from_string(qrcode)
            qrc = qr.QRCode.from_message(m.message)

            registrar_acceso(qrc)

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
        'timer': TIMER
    }
    for k,v in request.session.items():
        context[k] = v
    return render(request, 'authorized.html', context)

def denied(request):
    context = {
        'timer': TIMER
    }
    for k,v in request.session.items():
        context[k] = v

    return render(request, 'denied.html', context)

def invalid(request):
    context = {
        'timer': TIMER
    }
    for k,v in request.session.items():
        context[k] = v

    return render(request, 'invalid.html', context)


def access(request):
    access = Access.objects.all()
    data = []
    for a in access:
        data.append(
            {
                'firstname': a.firstname,
                'lastname': a.lastname,
                'username': a.username,
                'email': a.email,
                'number': a.number,
                'grade': a.grade,
                'timestamp': a.timestamp,
                'access': a.access
            }
        )
    return JsonResponse(data, safe=False)


def sync(request):
    s = SyncModel()
    s.sync()