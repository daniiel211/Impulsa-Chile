from serial_app import views
from django.urls import path

urlpatterns = [
    path('students/', views.student_list),
    path('students/<int:pk>/', views.student_detail),
]
    