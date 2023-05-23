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
    #groups = GroupPrimaryKeySerializer(many=True, required=False)
    groups = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all(), many=True, required=False)
    classrooms = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all(), many=True, required=False)    
    points = serializers.IntegerField(required=False)
    teacher = serializers.PrimaryKeyRelatedField(queryset=Teacher.objects.all(), required=False)
    subject = serializers.PrimaryKeyRelatedField(queryset=Subject.objects.all(), required=False)
    max_lessons = serializers.IntegerField(required=False)

    def update(self, instance, validated_data):
        groups_data = validated_data.pop('groups', [])
        classrooms_data = validated_data.pop('classrooms', [])
        instance = super(ClassSerializer, self).update(instance, validated_data)

        for group_data in groups_data:
            group_qs = Group.objects.filter(name__iexact=group_data.name)

            if group_qs.exists():
                group = group_qs.first()
            else:
                group = Group.objects.create(**group_data)

            instance.groups.add(group)


        for classroom_data in classrooms_data:
            classroom_qs = Classroom.objects.filter(name__iexact=classroom_data.name)

            if classroom_qs.exists():
                classroom = classroom_qs.first()
            else:
                classroom = Classroom.objects.create(**classroom_data)

            instance.classrooms.add(classroom)

        return instance

    class Meta:
        model = Class
        fields = '__all__'
    
    


class ScheduleClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScheduleClass
        fields = '__all__'