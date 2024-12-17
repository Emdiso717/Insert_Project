from django.urls import path
from .views import login
from .views import register
from .views import search_insect
from .views import search_detail
from .views import search_relative_insect
from .views import imagesearch
urlpatterns = [
    path('login/register',register,name='register'),
    path('login',login,name='login'),
    path('search_insect',search_insect,name='search_insect'),
    path('search_detail',search_detail,name='search_detail'),
    path('search_relative_insect',search_relative_insect,name='search_relative_insect'),
    path('imagesearch',imagesearch,name='imagesearch'),
]