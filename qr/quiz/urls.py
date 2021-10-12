from django.urls import path

from . import views

app_name='quiz'
urlpatterns = [
    path('', views.qr_code_view, name='qr'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('authorize', views.authorize, name='authorize')
    # path('qr/<str:user_id>', views.qr_code_view, name='qr')

]