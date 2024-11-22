from django.urls import path
from .views import login
from .views import register
from .views import search_insect
urlpatterns = [
    path('login/register',register,name='register'),
    path('login',login,name='login'),
    path('search_insect',search_insect,name='search_insect'),
]