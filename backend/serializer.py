from django.contrib.auth.models import User
from rest_framework import serializers
from django.core.validators import MinLengthValidator
from .models import Course, StudentProfile
from django.db import models

class UserSerializer(serializers.ModelSerializer):
    studyinterest = serializers.CharField(source='profile.studyinterest', required=False)
    github = serializers.CharField(source='profile.github', required=False)
    linkedin = serializers.CharField(source='profile.linkedin', required=False)
    photo = serializers.CharField(source='profile.photo', required=False)
    phonenumber = serializers.CharField(source='profile.phonenumber', required=False)
    jobdescription = serializers.CharField(source='profile.jobdescription', required=False)

    password = serializers.CharField(
        max_length=128,
        write_only=True,
        validators=[MinLengthValidator(8)]
    )
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2', 'studyinterest', 'photo', 'phonenumber', 'jobdescription', 'github', 'linkedin')

    def validate(self, attrs):
        # Ensure that password and password2 match
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match"})
        return attrs

    def create(self, validated_data):
  
        validated_data.pop('password2')
        profile_data = validated_data.pop('profile', {})
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()



        # Create the StudentProfile instance
        student_profile = StudentProfile.objects.create(user=user, **profile_data)

        return user


class CourseSerializer(serializers.ModelSerializer):
    photo = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = '__all__'

    def get_photo(self, obj):
        # Ensure that obj.photo is a valid URL
        return obj.photo


class StudentProfileSerializer(serializers.ModelSerializer):
    courses = CourseSerializer(many=True, read_only=True)

    class Meta:
        model = StudentProfile
        fields = "__all__"
