from django.urls import path, include
from django.conf.urls import url,include
from . import views
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import obtain_jwt_token

app_name = 'samsonadejoroscrumy'
router = DefaultRouter()
#router.register(r'users', views.UserViewSet, basename='users')
router.register(r'scrumusers', views.ScrumUserViewSet, basename='scrumusers')
router.register(r'goals', views.ScrumGoalViewSet, basename='scrumgoals')

urlpatterns = [
    path('', views.index, name='index'),
    #path('movegoal/<int:goal_id>/', views.move_goal, name='movegoal'),
    #path('home/', views.home, name='home'),
    #path('addgoal/', views.add_goal, name='add_goal'),
    #path('accounts/', include('django.contrib.auth.urls')),
    #path('success/', views.success_page, name='success'),
    #path('goalsuccess/', views.success_goal, name='goalsuccess'),
    #path('error/', views.error, name='error'),
    #path('movegoalsuccess/', views.move_goal_success, name='movegoalsuccess'),
    #path('errors/', views.errors, name='errors'),
    path('api/', include((router.urls, 'app_name'))),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api-token-auth/', obtain_jwt_token),
]












