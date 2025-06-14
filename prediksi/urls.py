from django.contrib import admin
from django.urls import path
from prediksi import views  # asumsikan apps kamu bernama prediksi

urlpatterns = [
    path('', views.index, name='index'),  # hanya bisa diakses jika login
    path('data-latih/', views.tambah_data_latih, name='tambah_data_latih'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
]
