from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
# from django.core import serializers

from .models import QuizAttempt, QuizGrade, User

#https://medium.com/geekculture/how-to-generate-a-qr-code-in-django-e32179d7fdf2
import qrcode
import qrcode.image.svg
from io import BytesIO

# Create your views here.

def accepted(request):

    data = QuizGrade.objects.all()
    # jdata = serializers.serialize('json',data)
    r = [
        {
            'idnumber':d.userid.idnumber,
            'grade': d.grade
        } for d in data
    ]
    print(r)
    return JsonResponse({'status':200,'data':r}, json_dumps_params={"ensure_ascii": False})


def qr_code_view(request, user_id):
    factory = qrcode.image.svg.SvgImage
    image = qrcode.make('MECARD:N:Mariano Visentin;TEL:+54 9 11 6767-0165;;', image_factory=factory, box_size=20)
    stream = BytesIO()
    image.save(stream)
    data = stream.getvalue().decode()
    return HttpResponse(data, content_type='image/svg+xml')