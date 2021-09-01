from django.urls import path
from . import views

app_name = 'users'
urlpatterns = [
    path('login/', views.Login, name='userlogin'),
    path('logout/', views.Logout, name='userlogout'),
    path('register/', views.Register, name='userregister'),
    path('profile/', views.ProfileEdit, name='userprofile'),
    path('profile/pdchange', views.PasswordEdit, name='userpdchange'),
]
