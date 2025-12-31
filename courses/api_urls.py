from django.urls import path
from . import api

urlpatterns = [
    path('courses/my/', api.my_courses_api, name='api_my_courses'),
    path('courses/available/', api.available_courses_api, name='api_available_courses'),
]
