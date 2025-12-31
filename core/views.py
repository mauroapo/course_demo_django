from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from courses.models import Course, Enrollment


@login_required
def home_view(request):
    """Home page with two carousels."""
    # Get user's enrolled courses
    my_enrollments = Enrollment.objects.filter(user=request.user).select_related('course')[:10]
    my_courses = [enrollment.course for enrollment in my_enrollments]
    
    # Get recent active courses
    recent_courses = Course.objects.filter(is_active=True).order_by('-created_at')[:10]
    
    return render(request, 'core/home.html', {
        'my_courses': my_courses,
        'recent_courses': recent_courses
    })


def healthcheck(request):
    """Simple healthcheck endpoint."""
    return JsonResponse({'status': 'healthy'})
