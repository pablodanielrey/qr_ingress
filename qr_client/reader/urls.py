
from django.urls import path
from . import views

app_label = 'reader'
urlpatterns = [
    path('', views.index)
]