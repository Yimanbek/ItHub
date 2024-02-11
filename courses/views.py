from rest_framework.permissions import IsAuthenticated 
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .serializers import CoursesSerializer
from .models import Courses
from drf_yasg.utils import swagger_auto_schema


class CoursesCreateView(APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(request_body=CoursesSerializer)
    def post(self, request):
        try:
            serializer = CoursesSerializer(data=request.data)
            if serializer.is_valid():
                serializer.validated_data['owner'] = request.user
                serializer.save()
                return Response({'success': True, 'message': 'Courses created successfully'})
            else:
                return Response({'success': False, 'message': 'Invalid data', 'errors': serializer.errors})
        except Exception as e:
            return Response({'success': False, 'message': f'An error occurred: {str(e)}'})

class CoursesDetailView(APIView):
    def get(self, request, id):
        try:
            courses = get_object_or_404(Courses, id=id)
            serializer = CoursesSerializer(courses)
            return Response({'success': True, 'courses': serializer.data})
        except Exception as e:
            return Response({'success': False, 'message': f'An error occurred: {str(e)}'})
        

class CoursesListView(APIView):
    def get(self, request):
        try:
            courses = Courses.objects.all()
            serializer = CoursesSerializer(courses, many=True)
            return Response({'success': True, 'courses': serializer.data})
        except Exception as e:
            return Response({'success': False, 'message': f'An error occurred: {str(e)}'})