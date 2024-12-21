from sqlite3 import IntegrityError

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
import json
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import Insect
from  .image import Baidu
import requests
from sparkai.llm.llm import ChatSparkLLM, ChunkPrintHandler
from sparkai.core.messages import ChatMessage
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

@csrf_exempt
def search_detail(request):

        name = request.GET.get('name')
        dbaseName = request.GET.get('dbaseName')
        apiKey = request.GET.get('apiKey')

        if not name or not dbaseName or not apiKey:
                return JsonResponse({"error": "缺少必要参数"}, status=400)

        # 构造目标 API 的 URL 和请求数据
        api_url = "http://zoology.especies.cn/api/v1/descriptionType"
        payload = {
                "scientificName": name,
                "dbaseName": dbaseName,
                "apiKey": apiKey
        }
        print(payload)
        try:
                # 向目标 API 发起 POST 请求
                response = requests.post(api_url, data=payload)

                # 检查目标 API 的响应状态
                if response.status_code == 200:
                        print(response.json())
                        if(response.json().get('message')=='没有此物种'):
                                return JsonResponse({"error": "没有此物种"}, status=500)
                        # 用于存储所有的DescriptionInfo
                        all_description_info = []
                        des_type_data = response.json().get('data', {}).get('desType', [])
                        for item in des_type_data:
                                for key, value in item.items():
                                        print(key, value)
                                        api_url = "http://zoology.especies.cn/api/v1/description"
                                        payload = {
                                                "scientificName": name,
                                                "dbaseName": dbaseName,
                                                "descriptionType": key,
                                                "apiKey": apiKey
                                        }
                                        response = requests.post(api_url, data=payload)
                                        if response.status_code == 200:
                                                data = response.json()
                                                print(data)
                                                # 获取 DescriptionInfo 数据
                                                description_info = data.get("data", {}).get("DescriptionInfo", [])

                                                # 如果DescriptionInfo非空，获取第一项
                                                if description_info:
                                                        all_description_info.append({
                                                                "descriptionType": value,  # 描述类型的名称
                                                                "descriptionInfo": description_info[0]  # 只获取第一项
                                                        })
                        for desc in all_description_info:
                                print(f"描述类型: {desc['descriptionType']}")
                                print(f"标题: {desc['descriptionInfo']['destitle']}")
                                print(f"内容: {desc['descriptionInfo']['descontent']}")
                                print(f"引用: {', '.join(desc['descriptionInfo']['refs'])}")
                                print("-" * 50)

                        return JsonResponse({"data": all_description_info}, status=200)  # 成功时直接返回 API 数据
                else:
                        print(response.text)
                        return JsonResponse({
                                "error": "目标 API 请求失败",
                                "status_code": response.status_code,
                                "response": response.text
                        }, status=response.status_code)
        except requests.exceptions.RequestException as e:
                # 捕获请求异常
                return JsonResponse({"error": "请求处理失败", "message": str(e)}, status=500)

@csrf_exempt
def search_relative_insect(request):
        name = request.GET.get('name')
        appid = "4c47a46e"  # 填写控制台中获取的 APPID 信息
        api_secret = "MWU5ZmZjNWE2NzU2NTI4YmY1YzMyYjUw"  # 填写控制台中获取的 APISecret 信息
        api_key = "222160bb4f1116c85b582c58ed881ed8"  # 填写控制台中获取的 APIKey 信息
        spark = ChatSparkLLM(
                spark_api_url="wss://spark-api.xf-yun.com/v3.5/chat",
                spark_app_id=appid,
                spark_api_key=api_key,
                spark_api_secret=api_secret,
                spark_llm_domain="generalv3.5",
                streaming=False,
        )
        messages = [ChatMessage(
                role="user",
                content='只给我输出关于这个昆虫：' + name + '类别相近的有关联的十个昆虫的中文名称,不要与我给你的昆虫重复，只要学名，不要介绍这个昆虫，只输出下面我告诉你的输出格式' +
                        '精简你的输出，输出格式为"昆虫名-昆虫名-昆虫名"'
                        # '精简你的输出，输出格式为"昆虫名1-昆虫名2-昆虫名3-昆虫名4-昆虫名5"'
        )]
        a = spark.generate([messages])
        string = a.generations[0][0].text
        names = string.split("-")
        print(names)
        return JsonResponse({"data": names}, status=200)  # 成功时直接返回 API 数据
def search_ai(request):
        message = request.GET.get('message')
        appid = "4c47a46e"  # 填写控制台中获取的 APPID 信息
        api_secret = "MWU5ZmZjNWE2NzU2NTI4YmY1YzMyYjUw"  # 填写控制台中获取的 APISecret 信息
        api_key = "222160bb4f1116c85b582c58ed881ed8"  # 填写控制台中获取的 APIKey 信息
        spark = ChatSparkLLM(
                spark_api_url="wss://spark-api.xf-yun.com/v3.5/chat",
                spark_app_id=appid,
                spark_api_key=api_key,
                spark_api_secret=api_secret,
                spark_llm_domain="generalv3.5",
                streaming=False,
        )
        messages = [ChatMessage(
                role="user",
                # content="请以html的格式返回我下面的问题，我会直接把你的回答插入到<p v-html=""></p >这样一个html块在前端显示出来，"+
                #         "我的问题如下："+message
                content="请回答我的问题，只需要纯文本的输出："+message

        )]
        a = spark.generate([messages])
        string = a.generations[0][0].text
        print(string)

        return JsonResponse({"data": string}, status=200)  # 成功时直接返回 API 数据
@csrf_exempt
def get_account(request):
    data = json.loads(request.body)
    account = data.get('account')
    user = User.objects.filter(username=account).first()
    date_joined = user.date_joined

    chinese_time_str = date_joined.strftime("%Y.%m.%d %A %H:%M:%S")

    information= {'account': user.username,'email':user.email,'date_joined':chinese_time_str}
    print(user.date_joined)
    return JsonResponse(information, safe=False)