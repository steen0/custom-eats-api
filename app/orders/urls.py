"""
URL mappings for the user API
"""

from django.urls import path

from . import views

urlpatterns = [
    path('datetime/', views.current_datetime),
]
