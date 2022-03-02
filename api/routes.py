from flask import request
import requests, json
from api import api

usr_token = "0706209ebda6cb2cb383ad9098d74cf01bf8ef1c6408a74672febdba90f6916c85264440a3cdb978ddfd3"


def get_vk_requests_url(method, data):
    new_data = []
    data_keys = list(data.keys())
    for key in data_keys:
        new_data.append({"key":key, "value":data[key]})

    vk_requests_url = f"https://api.vk.com/method/{method}?"

    for param in new_data:
        vk_requests_url += f"{param['key']}={param['value']}&"

    vk_requests_url = vk_requests_url[0: -1]
    return vk_requests_url

def get_vk2(method, data):

    full_request = {}
    token = data["access_token"]
    vk_request_url = ""

    if method == "execute.getFullProfileNewNew":
        data["access_token"] = usr_token

    if vk_request_url == "": vk_requests_url = get_vk_requests_url(method, data)
    print("API URL: " + vk_requests_url)
    vk_request = requests.get(vk_requests_url).json()
    full_request = vk_request

    return json.dumps(full_request, ensure_ascii=False)


@api.route('/method/<method>', methods=['GET', 'POST'])
def vk_method(method):
    print(f"=============================== {method} ===============================")
    print(f"agrs: {request.args}")
    print(f"headers: {request.headers}")
    print(f"form: {request.form}")

    return get_vk2(method, dict(request.form))
