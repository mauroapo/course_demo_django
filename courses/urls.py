from django.urls import path
from . import views

urlpatterns = [
    # Original course browsing
    path('my-courses/', views.my_courses_view, name='my_courses'),
    path('acquire/', views.acquire_courses_view, name='acquire_courses'),
    path('redirect/<int:course_id>/', views.course_redirect_view, name='course_redirect'),
    
    # Course content player
    path('<int:course_id>/', views.course_detail_view, name='course_detail'),
    path('lesson/<int:lesson_id>/', views.lesson_view, name='lesson_view'),
    path('quiz/<int:quiz_id>/', views.quiz_view, name='quiz_view'),
    path('quiz/<int:quiz_id>/take/', views.quiz_take_view, name='quiz_take'),
    path('quiz/result/<int:attempt_id>/', views.quiz_result_view, name='quiz_result'),
]
