from django.urls import path
from .views import login
from .views import register
urlpatterns = [
    path('login/register',register,name='register'),
    path('login',login,name='login'),
]