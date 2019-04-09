from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('samsonadejoroscrumy/', include('samsonadejoroscrumy.urls')),
    path('admin/', admin.site.urls),
]
