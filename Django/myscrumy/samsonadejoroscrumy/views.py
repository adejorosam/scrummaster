from samsonadejoroscrumy.models import GoalStatus, ScrumyGoals
from django.contrib.auth.models import User, Group, Permission
from .models import SignUpForm, CreateGoalForm, AddGoalForm, WeekOnlyAddGoalForm, QAChangegoal, DevMoveGoalForm, \
    AdminChangeGoalForm, QAChangeGoalForm, QAMoveForm, AdminChangeForm, OwnerChangeForm, ScrumUser, ScrumProjectRole
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import authenticate, login
from django.template import loader
from django.utils.datastructures import MultiValueDictKeyError
# from django.conf import settings
from django.shortcuts import render, redirect
# from django.contrib.auth.decorators import login_required
from random import *
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from rest_framework import viewsets, status, views, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

from .serializers import *
from .models import ScrumyGoals, GoalStatus

content_type_scrumygoals = ContentType.objects.get_for_model(ScrumyGoals)
content_type_goalstatus = ContentType.objects.get_for_model(GoalStatus)

developergroup = Group.objects.get(name='Developer')
admingroup = Group.objects.get(name='Admin')
qualityassurancegroup = Group.objects.get(name='Quality Assurance')
ownergroup = Group.objects.get(name='Owner')
verifygoal = GoalStatus.objects.get(status_name="Verify Goal")

def move_goal(request, goal_id, to_id):
    if request.user.is_authenticated:
        goal_item = ScrumyGoals.objects.get(id=goal_id)
        group_name = request.user.groups.all()[0].name
        from_allowed = []
        to_allowed = []

        if group_name == 'Developer':
            if request.user != goal_item.user.user:
                messages.error(request, 'Permission Denied: Unauthorized Moving of Goal')
                return HttpResponseRedirect(reverse('samsonadejoroscrumy:scrumboard'))
        if group_name == 'Owner':
            from_allowed = [0, 1, 2, 3]
            to_allowed = [0, 1, 2, 3]
        elif group_name == 'Admin':
            from_allowed = [1, 2]
            to_allowed = [1, 2]
        elif group_name == 'Developer':
            from_allowed = [0, 1]
            to_allowed = [0, 1]
        elif group_name == 'Quality Analyst':
            from_allowed = [2, 3]
            to_allowed = [2, 3]

        if (goal_item.status in from_allowed) and (to_id in to_allowed):
            goal_item.status = to_id
        elif group == 'Quality Analyst' and goal_item.status == 2 and to_id == 0:
            goal_item.status = to_id
        else:
            messages.error(request, 'Permission Denied: Unauthorized Moving of Goal')
            return HttpResponseRedirect(reverse('samsonadejoroscrumy:scrumboard'))
        goal_item.save()
        messages.success(request, 'Goal moved successfully')
        return HttpResponseRedirect(reverse('samsonadejoroscrumy:scrumboard'))
    else:
        messages.error(request, 'Error: Please login')
        return HttpResponseRedirect(reverse('login'))

'''
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request):
        username = request.data['username']
        password = request.data['password']

        login_user = authenticate(request, username=username, password=password)
        if login_user is not None:
            return JsonResponse({'exit': 0, 'message': 'Welcome to your Scrum Board', 'role': login_user.groups.all()[0].name,'data': filtered_users()})
        else: 
            return JsonResponse({'exit': 1, 'message': 'Error: Invalid Credentials'})

'''
# class ScrumUserViewSet(viewsets.ModelViewSet):
#     queryset = ScrumyGoals.objects.all()
#     serializer_class = ScrumUserSerializer

#     def create(self, request):
#         user, created = User.objects.get_or_create(username=request.data['username'])
#         if created:

#             group = Group.objects.get(name=request.data['usertype'])
#             group.user_set.add(user)
#             user.save()
#             scrum_user = ScrumUser(user=user,
#                                    fullname=request.data['full_name'],
#                                    age=request.data['age'])
#             scrum_user.save()
#             return JsonResponse({'message': 'User created successfully'})
#         else:
#             return JsonResponse({'message': 'Error: Username already exist'})
def filtered_users():
    users = ScrumUserSerializer(ScrumUser.objects.all(), many=True).data

    for user in users:
        user['scrumygoals_set'] = [x for x in user['scrumygoals_set']
         if x['visible'] == True]
    return users

'''
class ScrumUserViewSet(viewsets.ModelViewSet):
    queryset = ScrumUser.objects.all()
    serializer_class = ScrumUserSerializer
    def create(self,request):
        user, created = User.objects.get_or_create(username=request.data['username'], email=request.data['email'])
        if created:
            scrum_user = ScrumUser(user=user, nickname=request.data['full_name'])
            scrum_user.save()
            if request.data['usertype'] == 'Owner':
                scrum_project_role = ScrumProjectRole(role="Owner", user=scrum_user)
                scrum_project_role.save()

            user.set_password(request.data['password'])
            user.save()
            return JsonResponse({'message': 'User Created Successfully.'})
        else:
            return JsonResponse({'message': 'Error: User with that e-mail already exists.'})
'''
class ScrumUserViewSet(viewsets.ModelViewSet):
    queryset = ScrumUser.objects.all()
    serializer_class = ScrumUserSerializer

    def create(self, request):
        password = request.data['password']
        confirmpassword = request.data['pass_auth']
        role = request.data['usertype']
        fullname = request.data['full_name']
        username = request.data['username']

        if password == '' and role == '' and fullname == '' and username == '':
            return JsonResponse({'message': 'Error: All fields are required.'})
        if password != confirmpassword:
            return JsonResponse({'message': 'Error: Password Do not match.'})
        user, created = User.objects.get_or_create(username = request.data['username'])
        if created:
            user.set_password(password)
            group = Group.objects.get(name = request.data['usertype'])
            group.user_set.add(user)
            user.save()
            scrum_user = ScrumUser(user=user, nickname=request.data['full_name'])
            scrum_user.save()
            return JsonResponse({'message':'User Created Successfully'})
        else:
            return JsonResponse({'message': 'Error: Username Already Exists.'})

class ScrumGoalViewSet(viewsets.ModelViewSet):
    '''
    API endpoint that allows groups to be viewed or edited
    '''
    queryset = ScrumyGoals.objects.all()
    serializer_class = ScrumGoalSerializer

    def create(self,request):
        username = request.data['username']
        password = request.data['password']


        user = authenticate(request, username=username, password=password)
        if user is not None:
            name_goal = request.data['name']
            id_goal = request.data['id']
            group_name = user.groups.all()[0].name
            status_start = GoalStatus.objects.get(pk=1)
            if group_name == 'Admin':
                status_start = GoalStatus.objects.get(pk=3)
            elif group_name == 'Quality Assurance':
                status_start = GoalStatus.objects.get(pk=2)
            goal = ScrumyGoals(user=user.scrumuser, goal_id= id_goal, goal_name=name_goal,goal_status=status_start)
            goal.save()
            return JsonResponse({'exit':0, 'message':'Goal added', 'data': filtered_users()})
        else:
            return JsonResponse({'exit':1, 'message':'Not Logged In! Please Login First'})
    
    def patch(self, request):
            goals_id = request.data['goal_id']
            to_id = request.data['to_id']
            user = authenticate(request, username=request.data['username'], password=request.data['password'])
            if to_id == 5:
                if user.groups.all()[0].name == 'Developer':
                    if user != ScrumyGoals.objects.get(id = goals_id).user:
                        return JsonResponse({'message':'Permission Denied: Unauthorized Deletion of Goal', 'data':filtered_users()})          
                del_goal = ScrumyGoals.objects.get(id = goals_id)
                del_goal.visible = False
                print (goals_id)
                del_goal.save()
                return JsonResponse({'message':'Goal Removed Successfully', 'data':filtered_users()})
            else:
                goal_item = ScrumyGoals.objects.get(id = goals_id)

                group = user.groups.all()[0].name
                from_allowed = []
                to_allowed = []
                    
                if group == 'Developer':
                    if user != goal_item.user:
                        return JsonResponse({'message':'Permission Denied: Unauthorized Movement of Goal', 'data':filtered_users()})
                           
                if group == 'Owner':
                    from_allowed = [1, 2, 3, 4]
                    to_allowed = [1, 2, 3, 4]
                elif group == 'Admin':
                    from_allowed = [2, 3]
                    to_allowed = [1, 2]
                elif group == 'Developer':
                    from_allowed = [1, 2]
                    to_allowed = [1, 2]
                # elif group == 'Quality Analyst':
                #     from_allowed = [3, 4]
                #     to_allowed = [3, 4]
                        
                if (goal_item.goal_status_id in from_allowed) and (to_id in to_allowed):
                    # if to_id >= 0:
                        goal_item.goal_status_id = to_id 
                elif group == 'Quality Assurance' and goal_item.goal_status_id == 3 and to_id == 1:
                    goal_item.goal_status_id = to_id 
                else:
                    return JsonResponse({'message':'Permission Denied: Unauthorized Movement of Goal', 'data':filtered_users()})
                    
                goal_item.save()
                return JsonResponse({'message':'Goal Moved Successfully', 'data':filtered_users()})


    def put(self, request):
            if request.data['mode'] == 0:
                from_id = request.data['from_id']
                to_id = request.data['to_id']
               
                
                user = authenticate(request, username=request.data['username'], password=request.data['password'])

                if user.groups.all()[0].name == 'Developer':
                    return JsonResponse({'exit':0, 'message':'Permission Denied: Reassignment of Goal', 'data':filtered_users()})

                goal = ScrumyGoals.objects.get(id=from_id)

                author = None
                if to_id [0] == 'u':
                    author = ScrumUser.objects.get(id=to_id[1:])
                else:
                    author = ScrumyGoals.objects.get(id=to_id).user
                goal.user = author
                goal.save()
                return JsonResponse({'message':'Goal Reassigned Successfully', 'data':filtered_users()})
            else:
                goal = ScrumyGoals.objects.get(id=request.data['goal_id'])
                if request.user.groups.all()[0].name != 'Owner' and user != request.goal.scrumuser.user:
                    return JsonResponse({'exit':0, 'message':'Permission Denied: Unauthorized Name Change of Goal', 'data':filtered_users()})
                goal.goal_name = request.data['new_name']
                goal.save()
                return JsonResponse({'message':'Goal Name Changed', 'data':filtered_users()})

def jwt_response_payload_handler(token, user=None, request=None):
    return {
        'token': token,
        'message': 'Welcome!',
        'data': filtered_users(),
        'role': user.groups.all()[0].name
    }

def index(request):
      if request.method == 'POST':
          form = SignUpForm(request.POST)
          # check whether it's valid:
          if form.is_valid():
              user = form.save(commit=False)
              # group = form.cleaned_data['group_choices']
              username = form.cleaned_data['username']
              password = form.cleaned_data['password']
              user.set_password(password)
              user.save()
              user_group = Group.objects.get(name='Developer')
              user_group.user_set.add(user)
              user = authenticate(username=username, password=password)
              return HttpResponseRedirect('success/')
      else:
              form = SignUpForm()
      return render(request, 'samsonadejoroscrumy/signup.html', {'form': form})




def add_goal(request):
    if request.user.is_authenticated:
        name_goal = request.POST.get('name', None)
        group_name = request.user.groups.all()[0].name
        status_start = 0
        if group_name == 'Admin':
            status_start = 1
        elif group_name == 'Quality_Analyst':
            status_start = 2
        goal = ScrumyGoals(user=request.user.username, name=name_goal, status=status_start)
        goal.save()
        return HttpResponseRedirect('http://127.0.0.1:8000/samsonadejoroscrumy/goalsuccess/')
    else:
        return HttpResponseRedirect('')
       



def add_goal(request):
    current_user = request.user
    if current_user.is_authenticated:
            if request.method == 'POST':
                form = CreateGoalForm(request.POST)
                if form.is_valid():
                    post = form.save(commit=False)
                    goal_id = randint(1000, 9999)
                    status_name = GoalStatus(id=1)
                    post.created_by = current_user.first_name
                    post.moved_by = current_user.first_name
                    post.owner = current_user.first_name
                    post.goal_id = goal_id
                    post.goal_status = status_name
                    post.user = current_user
                    post.save()
            else:
                form = CreateGoalForm()
            return render(request, 'samsonadejoroscrumy/home.html', {'form': form})


def add_goal(request):
    #if not request.user.is_authenticated:
        #return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    current_user = request.user
    if request.method == 'POST':
        form = AddGoalForm(request.POST)
        post = form.save(commit=False)
        goal_id = randint(1000, 9999)
        status_name = GoalStatus(id=1)
        post.created_by = current_user.first_name
        post.moved_by = current_user.first_name
        post.owner = current_user.first_name
        post.goal_id = goal_id
        post.goal_status = status_name
        post.user_id = current_user.id
        post.save()
        return HttpResponseRedirect('/samsonadejoroscrumy/goalsuccess/')
    else:
        form = AddGoalForm()
    return render(request, 'samsonadejoroscrumy/addgoal.html', {'form': form})



'''

def success_page(request):
    success = 'Your account has been successfully created'
    context = {'success': success}
    return render(request, 'samsonadejoroscrumy/success.html', context)


def success_goal(request):
    success2 = 'Your goal has been successfully added'
    context = {'success2': success2}
    return render(request, 'samsonadejoroscrumy/goalsuccess.html', context)


def move_goal(request, goal_id):
    # if not request.user.is_authenticated:
    # return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    current_user = request.user
    usr_grp = request.user.groups.all()[0]
    # goals = get_object_or_404(ScrumyGoals, pk=goal_id)
    try:
        goals = ScrumyGoals.objects.get(goal_id=goal_id)
    except ObjectDoesNotExist:
        not_exist = 'A record with that goal id does not exist'
        context = {'not_exist': not_exist}
        return render(request, 'samsonadejoroscrumy/exception.html', context)
    if usr_grp == Group.objects.get(name='Developer') and current_user == goals.user:
        form = DevMoveGoalForm()
        if request.method == 'GET':
            return render(request, 'samsonadejoroscrumy/movegoal.html',
                          {'form': form, 'goals': goals, 'current_user': current_user, 'group': usr_grp})

        if request.method == 'POST':
            form = DevMoveGoalForm(request.POST)
            if form.is_valid():
                selected_status = form.save(commit=False)
                selected = form.cleaned_data['goal_status']
                get_status = selected_status.status_name
                choice = GoalStatus.objects.get(id=int(selected))
                goals.goal_status = choice
                goals.save()
                return HttpResponseRedirect('/samsonadejoroscrumy/movegoalsuccess')

        else:
            form = DevMoveGoalForm()
            return render(request, 'samsonadejoroscrumy/movegoal.html',
                          {'form': form, 'goal': goals, 'current_user': current_user, 'group': usr_grp})

    if usr_grp == Group.objects.get(name='Developer') and current_user != goals.user:
        form = DevMoveGoalForm()
        if request.method == 'GET':
            return HttpResponseRedirect('/samsonadejoroscrumy/error')

    if usr_grp == Group.objects.get(name='Admin') and current_user == goals.user:
        form = AdminChangeGoalForm()
        if request.method == 'GET':
            return render(request, 'samsonadejoroscrumy/movegoal.html',
                          {'form': form, 'goals': goals, 'current_user': current_user, 'group': usr_grp})
        if request.method == 'POST':
            form = AdminChangeGoalForm(request.POST)
            if form.is_valid():
                selected_status = form.save(commit=False)
                selected = form.cleaned_data['goal_status']
                get_status = selected_status.status_name
                choice = GoalStatus.objects.get(id=int(selected))
                goals.goal_status = choice
                goals.save()
                return HttpResponseRedirect('/samsonadejoroscrumy/movegoalsuccess')
        else:
            form = AdminChangeGoalForm()
            return render(request, 'samsonadejoroscrumy/movegoal.html',
                          {'form': form, 'goals': goals, 'current_user': current_user, 'group': usr_grp})

    if usr_grp == Group.objects.get(name='Admin') and current_user != goals.user:
        form = AdminChangeForm()
        if request.method == 'GET':
            return render(request, 'samsonadejoroscrumy/movegoal.html',
                          {'form': form, 'goals': goals, 'current_user': current_user, 'group': usr_grp})
        if request.method == 'POST':
            form = AdminChangeForm(request.POST)
            if form.is_valid():
                selected_status = form.save(commit=False)
                selected = form.cleaned_data['goal_status']
                get_status = selected_status.status_name
                choice = GoalStatus.objects.get(id=int(selected))
                goals.goal_status = choice
                goals.save()
                return HttpResponseRedirect('/samsonadejoroscrumy/movegoalsuccess')
        else:
            form = AdminChangeForm()
            return render(request, 'samsonadejoroscrumy/movegoal.html',
                          {'form': form, 'goals': goals, 'current_user': current_user, 'group': usr_grp})

    if usr_grp == Group.objects.get(name='Owner'):
        form = OwnerChangeForm()

        if request.method == 'GET':
            return render(request, 'samsonadejoroscrumy/movegoal.html',
                          {'form': form, 'goals': goals, 'current_user': current_user, 'group': usr_grp})
        if request.method == 'POST':
            form = OwnerChangeForm(request.POST)
            if form.is_valid():
                selected_status = form.save(commit=False)
                selected = form.cleaned_data['goal_status']
                get_status = selected_status.goal_status
                # choice = GoalStatus.objects.get(id = int(selected))
                goals.goal_status = get_status
                goals.save()
                return HttpResponseRedirect('/samsonadejoroscrumy/movegoalsuccess')
        else:
            form = OwnerChangeForm()
            return render(request, 'samsonadejoroscrumy/movegoal.html',
                          {'form': form, 'goals': goals, 'current_user': current_user, 'group': usr_grp})
    # else:
    # not_exist = 'You cannot move other users goals'
    # context = {'not_exist': not_exist}
    # return render(request, 'samsonadejoroscrumy/exception.html', context)

    if usr_grp == Group.objects.get(name='Quality Assurance') and goals.goal_status == dailygoal:
        return HttpResponseRedirect('/samsonadejoroscrumy/errors')
       
form = QAChangeGoalForm()
if request.method == 'GET':
                return render(request, 'samsonadejoroscrumy/movegoal.html',
                    {'form': form, 'goals': goals, 'current_user': current_user, 'group': usr_grp})
        if request.method == 'POST':
            form = QAChangeGoalForm(request.POST)
            if form.is_valid():
                selected_status = form.save(commit=False)
                selected = form.cleaned_data['goal_status']
                get_status = selected_status.status_name
                choice = GoalStatus.objects.get(id=int(selected))
                goals.goal_status = choice
                goals.save()
                return HttpResponseRedirect('/samsonadejoroscrumy/movegoalsuccess')
            form = QAChangeGoalForm()
            return render(request, 'samsonadejoroscrumy/movegoal.html',
                          {'form': form, 'goals': goals, 'current_user': current_user, 'group': usr_grp})
       

if usr_grp == Group.objects.get(name='Quality Assurance') and goals.goal_status == donegoal:
        form = QAForms()
        if request.method == 'GET':
            return render(request, 'samsonadejoroscrumy/movegoal.html',
                         {'form': form, 'goals': goals, 'current_user': current_user, 'group': usr_grp})
        if request.method == 'POST':
            form = QAForms(request.POST)
            if form.is_valid():
                selected_status = form.save(commit=False)
                selected = form.cleaned_data['goal_status']
                get_status = selected_status.status_name
                choice = GoalStatus.objects.get(id=int(selected))
                goals.goal_status = choice
                goals.save()
                return HttpResponseRedirect('/samsonadejoroscrumy/movegoalsuccess')
                form = QAForms()
                return render(request, 'samsonadejoroscrumy/movegoal.html',
                              {'form': form, 'goals': goals, 'current_user': current_user, 'group': usr_grp})

        # if usr_grp == Group.objects.get(name='Quality Assurance') and current_user != goals.user and goals.goal_status == verifygoal:
        #     form = QAChangeGoalForm()
        #     if request.method == 'GET':
        #         return render(request, 'tobmag1scrumy/movegoal.html',
        #                       {'form': form, 'goals': goals, 'currentuser': current_user, 'group': usr_grp})
        #     if request.method == 'POST':
        #         form = QAChangeGoalForm(request.POST)
        #         if form.is_valid():
        #             selected_status = form.save(commit=False)
        #             selected = form.cleaned_data['goal_status']
        #             get_status = selected_status.status_name
        #             choice = GoalStatus.objects.get(id=int(selected))
        #             goals.goal_status = choice
        #             goals.save()
        #             return HttpResponseRedirect('/tobmag1scrumy/movegoalsuccess')

        #     else:
        #         form = QAChangeGoalForm()
        #         return render(request, 'tobmag1scrumy/movegoal.html',
        #                       {'form': form, 'goals': goals, 'currentuser': current_user, 'group': usr_grp})
        # else:
        #     not_exist = 'You can only move goal from verify goals to done goals'
        #     context = {'not_exist': not_exist}
        #     return render(request, 'tobmag1scrumy/exception.html', context)
else:
        form = QAMoveForm()
        if request.method == 'GET':
            return render(request, 'samsonadejoroscrumy/movegoal.html',
                          {'form': form, 'goals': goals, 'currentuser': current_user, 'group': usr_grp})
        if request.method == 'POST':
            form = QAMoveForm(request.POST)
            if form.is_valid():
                selected_status = form.save(commit=False)
                selected = form.cleaned_data['goal_status']
                get_status = selected_status.status_name
                choice = GoalStatus.objects.get(id=int(selected))
                goals.goal_status = choice
                goals.save()
                return HttpResponseRedirect('/samsonadejoroscrumy/movegoalsuccess')


def home(request):
    #if not request.user.is_authenticated:
        #return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    user = User.objects.all()
    current_user = request.user
    group = current_user.groups.values_list('name', flat=True)[0]
    weekly_goal = GoalStatus.objects.get(status_name="Weekly Goal")
    wg = weekly_goal.scrumygoals_set.all()
    daily_goal = GoalStatus.objects.get(status_name="Daily Target")
    dg = daily_goal.scrumygoals_set.all()
    verify_goal = GoalStatus.objects.get(status_name="Verify Goal")
    vg = verify_goal.scrumygoals_set.all()
    done_goal = GoalStatus.objects.get(status_name="Done Goal")
    gd = done_goal.scrumygoals_set.all()

    if current_user.is_authenticated:
        if group == 'Developer' or group == 'Owner' or group == 'Quality Assurance':
            form = WeekOnlyAddGoalForm()
            context = {'user': user, 'weekly_goal': wg, 'daily_goal': dg, 'verify_goal': vg,
                       'done_goal': gd, 'form': form, 'current_user': current_user.username, 'group': group}
            if request.method == 'GET':
                return render(request, 'samsonadejoroscrumy/home.html', context)
            if request.method == 'POST':
                form = WeekOnlyAddGoalForm(request.POST)
                if form.is_valid():
                    post = form.save(commit=False)
                    goal_id = randint(1000, 9999)
                    post.moved_by = current_user.first_name
                    post.owner = current_user.first_name
                    post.goal_id = goal_id
                    post.goal_status = weekly_goal
                    post.user = current_user
                    post.save()
            else:
                form = WeekOnlyAddGoalForm()
                return HttpResponseRedirect('/samsonadejoroscrumy/movegoalsuccess')
        if group == 'Admin':
            context = {'user': user, 'weekly_goal': wg, 'daily_goal': dg, 'verify_goal': vg,
                       'done_goal': gd, 'current_user': current_user.username, 'group': group}
            if request.method == 'GET':
                return render(request, 'samsonadejoroscrumy/home.html', context)



def error(request):
    current_user = request.user
    return render(request, 'samsonadejoroscrumy/error.html', {'current_user': current_user})


def errors(request):
    current_user = request.user
    return render(request, 'samsonadejoroscrumy/errors.html',  {'current_user': current_user})

def move_goal_success(request):
    current_user = request.user
    return render(request, 'samsonadejoroscrumy/movegoalsuccess.html', {'current_user': current_user})
'''