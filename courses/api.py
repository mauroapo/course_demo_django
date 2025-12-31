from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Course, Enrollment
from .serializers import CourseSerializer, EnrollmentSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_courses_api(request):
    """API endpoint for user's enrolled courses."""
    enrollments = Enrollment.objects.filter(user=request.user).select_related('course')
    serializer = EnrollmentSerializer(enrollments, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def available_courses_api(request):
    """API endpoint for available courses."""
    search_query = request.GET.get('search', '')
    sort_by = request.GET.get('sort', '')
    
    # Get user's enrolled course IDs
    enrolled_course_ids = Enrollment.objects.filter(
        user=request.user
    ).values_list('course_id', flat=True)
    
    # Get available courses
    courses = Course.objects.filter(is_active=True).exclude(id__in=enrolled_course_ids)
    
    # Apply search filter
    if search_query:
        courses = courses.filter(name__icontains=search_query)
    
    # Apply sorting
    if sort_by == 'price_asc':
        courses = courses.order_by('price')
    elif sort_by == 'price_desc':
        courses = courses.order_by('-price')
    else:
        courses = courses.order_by('-created_at')
    
    serializer = CourseSerializer(courses, many=True)
    return Response(serializer.data)
