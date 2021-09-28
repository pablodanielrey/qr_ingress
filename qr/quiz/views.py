from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
# from django.core import serializers

from .models import QuizAttempt, QuizGrade, User

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