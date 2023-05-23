from .models import *
from rest_framework import serializers
from django.core.serializers import serialize
from .modules.hashutils import make_pw_hash
from django.http import Http404, JsonResponse
import json

class GroupPrimaryKeySerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id']

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'

class ClassroomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classroom
        fields = '__all__'

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = '__all__'

class ClassSerializer(serializers.ModelSerializer):
    groups = GroupPrimaryKeySerializer(many=True)
    classrooms = ClassroomSerializer(many=True)

    class Meta:
        model = Class
        fields = '__all__'


class ScheduleClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScheduleClass
        fields = '__all__'