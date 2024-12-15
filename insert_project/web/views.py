from sqlite3 import IntegrityError

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
import json
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import Insect
from  .image import Baidu
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

@csrf_exempt
def search_insect(request):
        query = request.GET.get('name')
        if not query:
                return JsonResponse({"error":"未成功请求"}, status=400)

        try:
                insect = Insect.objects.select_related('taxonomy').get(chinese_name=query)
                data = {
                        "chinese_name":insect.chinese_name,
                        "latin_name":insect.latin_name,
                        "common_name":insect.common_name,
                        "taxonomy":{
                                'kingdom': insect.taxonomy.kingdom,
                                'phylum': insect.taxonomy.phylum,
                                'class_name': insect.taxonomy.class_name,
                                'subclass_name': insect.taxonomy.subclass_name,
                                'order': insect.taxonomy.order,
                                'family': insect.taxonomy.family,
                                'genus': insect.taxonomy.genus,
                                'species': insect.taxonomy.species,
                                'subspecies': insect.taxonomy.subspecies,
                        },
                        'aliases': insect.aliases,
                        'appearance': insect.appearance,
                        'habits': insect.habits,
                        'distribution': insect.distribution,
                        'relatives': insect.relatives,
                        'image_url': insect.image_url,
                }
                return JsonResponse(data)
        except Insect.DoesNotExist:
                return JsonResponse({'error': 'Insect not found'}, status=404)

@csrf_exempt
def imagesearch(request):
        data = json.loads(request.body)
        result = Baidu(data.get('image'))
        return JsonResponse(result)