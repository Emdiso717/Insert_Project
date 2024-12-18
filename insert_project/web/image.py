import requests
import base64
from urllib.parse import quote_plus
API_KEY = "G9z013xbe3MVAEv6wOl7qkF4"
SECRET_KEY = "iAgsxdNtl3CkvS9hXLMIznhK4KYQXDLD"


def Baidu(image):
    url = "https://aip.baidubce.com/rest/2.0/image-classify/v1/animal?access_token=" + get_access_token()
    image = quote_plus(image)
    payload = 'image=' + image + '&baike_num=2'
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json",
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.json())
    return response.json()


def get_access_token():

    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {
        "grant_type": "client_credentials",
        "client_id": API_KEY,
        "client_secret": SECRET_KEY,
    }
    return str(requests.post(url, params=params).json().get("access_token"))


