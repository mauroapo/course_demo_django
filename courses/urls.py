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

    # Turma / Presence Control
    path('turmas/', views.turma_list_view, name='turma_list'),
    path('turmas/<int:turma_id>/', views.turma_detail_view, name='turma_detail'),
    path('turmas/<int:turma_id>/session/create/', views.presence_session_create_view, name='presence_session_create'),
    path('turmas/session/<int:session_id>/', views.presence_session_detail_view, name='presence_session_detail'),
    path('turmas/session/<int:session_id>/toggle/', views.presence_session_toggle_view, name='presence_session_toggle'),
    path('turmas/session/<int:session_id>/checkin/', views.presence_checkin_view, name='presence_checkin'),
    path('turmas/session/<int:session_id>/remove/<int:student_id>/', views.presence_remove_view, name='presence_remove'),
]
