from django.urls import path

from . import views

urlpatterns = [
    path('', views.accepted),
    path('qr/<str:user_id>', views.qr_code_view)
]