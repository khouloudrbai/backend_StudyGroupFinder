from django.contrib import admin
from django.urls import path 
from . import views 
from django.conf import settings  # Import settings
from django.conf.urls.static import static 


urlpatterns = [
 path('login',views.login),
 path('signup',views.signup),
 path('getuserinfo', views.get_user_info),
 path('profile/<int:user_id>/', views.ProfileAPI.as_view(), name='profile'),
 path('profile/update/', views.UpdateProfileView.as_view()),
 path('profile/delete/', views.DeleteProfileView.as_view()),
 path('upload-photo/', views.UploadProfilePhotoView.as_view(), name='upload-photo'),
 path('courses/', views.list_courses, name='list_courses'),
 path('profile/add_course/<int:course_id>/', views.add_course_to_profile, name='add_course_to_profile'),
path('courses/serach', views.CourseSearchView.as_view(), name='course_search'),

] +static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)