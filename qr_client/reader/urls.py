
from django.urls import path
from . import views

app_name = 'reader'
urlpatterns = [
    path('', views.index, name='index'),
    path('authorized', views.authorized, name='access_authorized'),
    path('denied', views.denied, name='access_denied'),
    path('invalid', views.invalid, name='invalid_qr'),
    path('access', views.access, name='access_records')
]