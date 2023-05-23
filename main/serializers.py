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

class ClassroomPrimaryKeySerializer(serializers.ModelSerializer):
    class Meta:
        model = Classroom
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
    groups = GroupPrimaryKeySerializer(many=True, required=False)
    classrooms = ClassroomPrimaryKeySerializer(many=True, required=False)
    points = serializers.IntegerField(required=False)
    teacher = serializers.PrimaryKeyRelatedField(queryset=Teacher.objects.all(), required=False)
    subject = serializers.PrimaryKeyRelatedField(queryset=Subject.objects.all(), required=False)
    max_lessons = serializers.IntegerField(required=False)

    def update(self, instance, validated_data):
        groups_data = validated_data.pop('groups', [])
        classrooms_data = validated_data.pop('classrooms', [])
        instance = super().update(instance, validated_data)

        # Обновляем связи с группами по идентификаторам
        if groups_data:
            instance.groups.set([group_data for group_data in groups_data])
        if classrooms_data:
            instance.classrooms.set([classroom_data for classroom_data in classrooms_data])

        return instance

    class Meta:
        model = Class
        fields = '__all__'
    
    


class ScheduleClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScheduleClass
        fields = '__all__'