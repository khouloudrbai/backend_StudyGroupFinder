from django.conf import settings
from django.http import JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from backend.models import Course, StudentProfile
from .serializer import CourseSerializer, StudentProfileSerializer, UserSerializer
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from django.core.files.storage import FileSystemStorage



@api_view(['POST'])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token = Token.objects.create(user=user)
        return Response({"token": token.key, "user": serializer.data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login(request):
    try:
        user = get_object_or_404(User, username=request.data.get('username'))
        if not user.check_password(request.data.get('password')):
            return Response({"detail": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
        token, created = Token.objects.get_or_create(user=user)
        serializer = UserSerializer(instance=user)
        return Response({"token": token.key, "user": serializer.data}, status=status.HTTP_200_OK)
    except KeyError:
        return Response({"detail": "Username and password are required."}, status=status.HTTP_400_BAD_REQUEST)


class UpdateProfileView(generics.UpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]   
    serializer_class = StudentProfileSerializer

    def get_object(self):
        try:
            return self.request.user.profile
        except StudentProfile.DoesNotExist:
            raise get_object_or_404(StudentProfile, user=self.request.user)
        

class ProfileAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id, *args, **kwargs):
        user = get_object_or_404(User, pk=user_id)
        try:
            profile = user.studentprofile
        except StudentProfile.DoesNotExist:
            return Response({"detail": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)
        
        profile_serializer = StudentProfileSerializer(profile)
        return Response(profile_serializer.data, status=status.HTTP_200_OK)


class DeleteProfileView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = StudentProfileSerializer

    def get_object(self):
        try:
            return self.request.user.studentprofile
        except StudentProfile.DoesNotExist:
            raise get_object_or_404(StudentProfile, user=self.request.user)


class UploadProfilePhotoView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self,request):
        if request.method == 'POST' and request.FILES['photo']:
            photo = request.FILES['photo']
            fs = FileSystemStorage(location=settings.MEDIA_ROOT)
            filename = fs.save('profile_photos/' + photo.name, photo)
            photo_url = settings.MEDIA_URL + filename
            profile = request.user.profile  
            profile.photo =  filename  
            profile.save() 
            return JsonResponse({'photoUrl': photo_url})
        return JsonResponse({'error': 'No file uploaded'}, status=400)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_user_info(request):
    serializer = UserSerializer(instance=request.user)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def list_courses(request):
    courses = Course.objects.all()
    serializer = CourseSerializer(courses, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def add_course_to_profile(request, course_id):
    try:
        profile = request.user.studentprofile  # Adjusted for StudentProfile, assuming user has StudentProfile
        course = Course.objects.get(id=course_id)
        profile.courses.add(course)
        return Response({"message": "Course added successfully"}, status=status.HTTP_200_OK)
    except Course.DoesNotExist:
        return Response({"error": "Course not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def add_courses(request, course_id):
    serializer = CourseSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token = Token.objects.create(user=user)
        return Response({"token": token.key, "user": serializer.data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CourseSearchView(APIView):
    def get(self, request):
        search_query = request.GET.get('q', '')  # Get the search query parameter
        if search_query:
            # Filter courses by title or description using a case-insensitive search
            courses = Course.objects.filter(
                Q(title__icontains=search_query) | Q(description__icontains=search_query)
            )
        else:
            # If no query, return all courses
            courses = Course.objects.all()

        # Serialize the filtered courses
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)