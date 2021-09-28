from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.db import models

# from django.core import serializers

from datetime import datetime, timezone
import uuid

from .models import QuizGrade, User

#https://medium.com/geekculture/how-to-generate-a-qr-code-in-django-e32179d7fdf2
import qrcode
import qrcode.image.svg
from io import BytesIO

# Create your views here.

def accepted(request):

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
            'timemodified': d.timemodified
        } for d in data
    ]
    print(r)
    return JsonResponse({'status':200,'data':r}, json_dumps_params={"ensure_ascii": False})


def _get_enabled_quiz(user_id):
    """
        retorna las respuestas que cumplen los parámetros para considerarse permitidas.
    """
    dt = datetime.now()
    nowt = dt.timestamp()

    week_seconds = 60 * 60 * 24 * 7
    week_before_t = nowt - week_seconds

    """
    attempts = QuizAttempt.objects.filter(timefinish__gt=week_before_t, userid__id=user_id)
    attempt = attempts.first()
    if not attempt:
        return None
    """

    try:
        user = User.objects.get(id=user_id)
        grades = user.grades.filter(quiz=7168, grade=10.0)
        return user, grades
    except User.DoesNotExist as e:
        return None, None
    #return QuizGrade.objects.filter(timemodified__gt=week_before_t, userid__id=user_id, grade=10.0)
    #return QuizGrade.objects.filter(quiz=7168, user__id=user_id, grade=10.0)

def qr_code_view(request, user_id):

    factory = qrcode.image.svg.SvgImage
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=20,
        border=4,
        image_factory=factory
    )


    user, quizs = _get_enabled_quiz(user_id)

    
    if not user:
        data = f"Inválido;{uuid.uuid4()}"
    else:
        quiz = quizs.first()
        if not quiz:
            data = f"Persona: {user.firstname} {user.lastname};Inválido;{uuid.uuid4()}"
        else:
            data = f"Persona: {quiz.user.firstname} {quiz.user.lastname};Calificación: {quiz.grade};{uuid.uuid4()}"

    #qr.add_data(f"MECARD:N:{user.firstname} {user.lastname};TEL:+54 9 221 3033138;;")
    #qr.add_data('https://youtu.be/YqsdmQsjQds')
    #qr.add_data(f"WIFI:T:WPA;S:mynetwork;P:mypass;;")
    # qr.add_data('http://localhost:8000/quiz/')
    # qr.add_data('MECARD:N:Mariano Visentin;TEL:+54 9 11 6767-0165;;')
    # qr.add_data('mailto:mariano.visentin@econo.unlp.edu.ar')
    qr.add_data(data)

    image = qr.make_image()
    stream = BytesIO()
    image.save(stream)
    data = stream.getvalue().decode()
    return HttpResponse(data, content_type='image/svg+xml')