
from django.urls import path
from . import views

app_name = 'reader'
urlpatterns = [
    path('', views.index, name='index'),
    path('authorized', views.authorized, name='access_authorized'),
    path('denied', views.denied, name='access_denied'),
]