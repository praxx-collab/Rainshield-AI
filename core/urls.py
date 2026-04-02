from django.urls import path
from . import views

urlpatterns = [
    path('', views.register, name='register'),
    path('dashboard/<int:worker_id>/', views.dashboard, name='dashboard'),
    path('claim/', views.claim, name='claim'),
]