from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views
# app_name = 'trips'
urlpatterns = [
    path('', views.Mainpage, name='Mainpage'),
    path('daily<int:num>/', views.Daily_detail, name='Daily'),
    path('Test/', views.Test, name='Test'),
    path('AddNew/', views.Add_New, name='Add_New'),
    path('Update<int:num>', views.Update, name='Update'),
    path('Delete<int:num>', views.Delete, name='Delete'),
    path('ImgCtl/', views.ImageView, name='ImgCtl'),
]
