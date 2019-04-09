from django.contrib.auth.models import User 
from .models import *
from rest_framework import serializers

'''
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','groups','password',]
'''


class ScrumGoalSerializer(serializers.ModelSerializer):

    class Meta:
        model = ScrumyGoals
        fields = ['visible','goal_id','goal_name','goal_status','id']


class ScrumUserSerializer(serializers.ModelSerializer):
    scrumygoals_set = ScrumGoalSerializer(many=True)
    class Meta:
        model = ScrumUser
        fields = ['id','nickname','scrumygoals_set']


class ScrumProjectRoleSerializer(serializers.ModelSerializer):
 
    
    class Meta:
        model = ScrumProjectRole
        fields = ['role', 'user', 'id']   