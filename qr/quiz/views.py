from django.http.request import HttpRequest
from django.urls import reverse
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.db import models
from django.conf import settings
# from django.core import serializers

import logging
logging.getLogger().setLevel(logging.DEBUG)
import json


#####
### Vistas de la parte de oauth
#####
from authlib.integrations.django_client import OAuth
from authlib.integrations.base_client.errors import OAuthError

oauth = OAuth()
oauth.register(
    name='econo',
    server_metadata_url='https://oidc.econo.unlp.edu.ar/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'openid email profile'
    }
)


def login(request):
    if request.session.get('user', None):
        return redirect('/')

    econo = oauth.create_client('econo')
    redirect_uri = request.build_absolute_uri(reverse('quiz:authorize'))
    return econo.authorize_redirect(request, redirect_uri)


def authorize(request):
    try:
        token = oauth.econo.authorize_access_token(request)
        # resp = oauth.econo.get('user', token=token)
        # resp.raise_for_status()
        # profile = resp.json()
        # #userinfo = oauth.econo.userinfo(token=token)
        # user = {
        #     'email': userinfo.email,
        #     'username': userinfo.preferred_username
        # }
        # return HttpResponse(json.dumps(userinfo,ensure_ascii=False))
        userinfo = oauth.econo.parse_id_token(request, token)
        logging.debug(userinfo)
        request.session['user'] = userinfo
        return redirect('/')

    except OAuthError as e:
        context = {
            'error': e.description
        }
        return render(request, 'error_oauth.html', context)

def logout(request):
    request.session.pop('user', None)
    return redirect('/')


####
## Vistas de la sección de qr
#####

from datetime import datetime, timezone
import os
#https://medium.com/geekculture/how-to-generate-a-qr-code-in-django-e32179d7fdf2
import qrcode
import qrcode.image.svg
from io import BytesIO
import base64

from qr_common import qr

from .models import QuizGrade, User



def _get_enabled_quiz(user):
    grades = user.grades.filter(quiz=7168, grade=10.0)
    return grades

def _get_moodle_user(user):
    username = user['preferred_username']
    moodle_user = User.objects.get(username=username)
    return moodle_user


def qr_code_view(request):
    user = user = request.session.get('user', None)
    if not user:
        redirect_uri = request.build_absolute_uri(reverse('quiz:login'))
        return redirect(redirect_uri, permanent=False)

    logging.debug(json.dumps(user))

    try:
        
        moodle_user = _get_moodle_user(user)
    except User.DoesNotExist as e:
        return render(request, 'invalid_user.html', user)

    quizs = _get_enabled_quiz(moodle_user)
    quiz = quizs.first()
    if not quiz:
        return render(request, 'invalid_quiz.html', user)

    factory = qrcode.image.svg.SvgImage
    qr_c = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=20,
        border=4,
        image_factory=factory
    )

    qr_code = qr.QRCode(moodle_user.firstname, moodle_user.lastname,  moodle_user.username, moodle_user.email, moodle_user.idnumber, quiz.grade, quiz.timemodified)
    message = qr.Message(qr_code.to_message())

    qr_c.add_data(message.to_string())
    
    image = qr_c.make_image()
    stream = BytesIO()
    image.save(stream)
    data = stream.getvalue().decode()
    # return HttpResponse(data, content_type='image/svg+xml')

    bdata = base64.b64encode(bytes(data,'utf-8'))
    context = {
        'qr_image': bdata.decode('utf8'),
        'user': moodle_user
    }
    return render(request,'qr_code.html', context)



































def _get_accepted():
    data = QuizGrade.objects.filter(quiz=7168)
    # jdata = serializers.serialize('json',data)
    r = [
        {
            'user_id': d.user.id,
            'username': d.user.username,
            'firstname': d.user.firstname,
            'lastname': d.user.lastname,
            'idnumber':d.user.idnumber,
            'grade': d.grade,
            'timemodified': d.timemodified,
            'date': datetime.utcfromtimestamp(d.timemodified).strftime('%Y-%m-%d %H:%M:%S')
        } for d in data
    ]
    return r

def accepted(request):
    r = _get_accepted()
    print(r)
    return JsonResponse({'status':200,'data':r}, json_dumps_params={"ensure_ascii": False})

def index(request):
    context = {
        'quizes':_get_accepted()
    }
    return render(request, 'quiz_index.tmpl', context)

def login_example(request:HttpRequest):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    return HttpResponse(request.user.username)