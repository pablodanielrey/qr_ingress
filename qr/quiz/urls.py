from django.urls import path

from . import views

app_name='quiz'
urlpatterns = [
    path('', views.index),
    path('qr/<str:user_id>', views.qr_code_view, name='qr')
]