from django.contrib.auth.models import User, Group
from rest_framework import serializers
from . import models


class userSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password',]

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.student      
        fields = '__all__'

class StudentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.studentDetails
        fields = '__all__'

class bookSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Book
        fields = '__all__'
