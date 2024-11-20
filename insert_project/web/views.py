from sqlite3 import IntegrityError

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
import json
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
@csrf_exempt
def login(request):
        data = json.loads(request.body)
        account = data.get('account')
        password = data.get('password')
        user = authenticate(username=account,password=password)
        if user is not None:
                return HttpResponse("success")
        else:
                return HttpResponse("用户名或密码错误")


@csrf_exempt
def register(request):
        data = json.loads(request.body)
        account = data.get('account')
        email=data.get('email')
        password = data.get('password')
        if  User.objects.filter(email=email).exists():
               return HttpResponse("错误：邮箱号重复使用")
        try:
                new_user=User(username=account,email=email)
                new_user.set_password(password)
                new_user.save()
                return HttpResponse("success")
        except IntegrityError as e2:
                return HttpResponse("错误：用户名重复使用")
