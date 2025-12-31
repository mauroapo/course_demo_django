from rest_framework import serializers
from .models import Course, Enrollment


class CourseSerializer(serializers.ModelSerializer):
    """Serializer for Course model."""
    
    class Meta:
        model = Course
        fields = ['id', 'name', 'description', 'price', 'image_url', 'created_at']


class EnrollmentSerializer(serializers.ModelSerializer):
    """Serializer for Enrollment model."""
    
    course = CourseSerializer(read_only=True)
    
    class Meta:
        model = Enrollment
        fields = ['id', 'course', 'acquired_at', 'source']
