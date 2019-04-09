from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms


# Create your models here.

class ScrumUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=30)

    def __str__(self):
        return (self.nickname)

    class Meta:
        verbose_name_plural = 'Scrum Users'
        ordering = ['nickname']

class GoalStatus(models.Model):
    status_name = models.CharField(max_length=200)

    def __str__(self):
        return self.status_name



class ScrumyGoals(models.Model):
    visible = models.BooleanField(default=True)
    moveable = models.BooleanField(default=True)
    goal_name= models.CharField(max_length=200)
    goal_id= models.CharField(max_length=100)
    created_by = models.CharField(max_length=200)
    moved_by = models.CharField(max_length=200)
    owner = models.CharField(max_length=200)
    goal_status = models.ForeignKey(GoalStatus, on_delete=models.PROTECT)
    user=models.ForeignKey(ScrumUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.goal_id

    class Meta:
        ordering = ['-goal_id']
        verbose_name_plural = "Scrumy Goals"




class ScrumProjectRole(models.Model):
    role = models.CharField(max_length=20)
    user = models.ForeignKey(ScrumUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.role






class SignUpForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password']


class CreateGoalForm(ModelForm):
    class Meta:
        model = ScrumyGoals
        fields = ['goal_name', 'goal_id']


class AddGoalForm(ModelForm):
    class Meta:
        model = ScrumyGoals
        fields = ['goal_name', 'goal_status']


class WeekOnlyAddGoalForm(ModelForm):
    class Meta:
        model = ScrumyGoals
        fields = ['goal_name']


class DevMoveGoalForm(forms.ModelForm):
    queryset = GoalStatus.objects.all()
    goal_status = forms.ChoiceField(choices=[(choice.pk, choice) for choice in queryset[:3]])

    class Meta:
        model = GoalStatus
        fields = ['goal_status']


class AdminChangeGoalForm(forms.ModelForm):
    queryset = GoalStatus.objects.all()
    goal_status = forms.ChoiceField(choices=[(choice.pk, choice) for choice in queryset[:3]])

    class Meta:
        model = GoalStatus
        fields = ['goal_status']


class AdminChangeForm(forms.ModelForm):
    queryset = GoalStatus.objects.all()
    goal_status = forms.ChoiceField(choices=[(choice.pk, choice) for choice in queryset[1:3]])

    class Meta:
        model = GoalStatus
        fields = ['goal_status']


class OwnerChangeForm(forms.ModelForm):
    class Meta:
        model = ScrumyGoals
        fields = ['goal_status']


class QAChangegoal(forms.ModelForm):
    queryset = GoalStatus.objects.all()
    goal_status = forms.ChoiceField(choices=[(choice.pk, choice) for choice in queryset[::1][:3]])

    class Meta:
        model = GoalStatus
        fields = ['goal_status']


class QAChangeGoalForm(forms.ModelForm):
    queryset = GoalStatus.objects.all()
    goal_status = forms.ChoiceField(choices=[(choice.pk, choice) for choice in queryset.order_by('-id')[:4][::4]])

    class Meta:
        model = GoalStatus
        fields = ['goal_status']


class QAMoveForm(forms.ModelForm):
    queryset = GoalStatus.objects.all()
    goal_status = forms.ChoiceField(choices=[(choice.pk, choice) for choice in queryset[1:3]])

    class Meta:
        model = GoalStatus
        fields = ['goal_status']

