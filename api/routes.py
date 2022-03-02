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
    
    #INIT
    full_request = {}
    token = data["access_token"]
    vk_request_url = ""
    
    #PRE-REQUEST TWEAKS
    #if method == "execute.getFullProfileNewNew": #Get Unblocked Tweak
        #data["access_token"] = usr_token

    if vk_request_url == "": vk_requests_url = get_vk_requests_url(method, data)
    print("API URL: " + vk_requests_url)
    vk_request = requests.get(vk_requests_url).json()
    
    #POST-REQUEST TWEAKS
    if method == "messages.getHistory":
        if vk_request["response"]["conversations"][0]["peer"]["id"] == -210967996:
            vk_request["response"]["items"] = [{'date': 9000000000, 'from_id': -210967996, 'id': 1900001, 'out': 0, 'attachments': [], 'conversation_message_id': 1900001, 'fwd_messages': [], 'important': False, 'is_hidden': False, 'peer_id': vk_request["response"]["conversations"][0]["peer"]["id"], 'random_id': 0, 'text': 'VK Tweaks успешно активен!'}]
        else:
            vk_request["response"]["items"].append(
                {'date': 9000000000, 'from_id': -210967996, 'id': 1900001, 'out': 0, 'attachments': [], 'conversation_message_id': 1900001, 'fwd_messages': [], 'important': False, 'is_hidden': False, 'peer_id': vk_request["response"]["conversations"][0]["peer"]["id"], 'random_id': 0, 'text': 'Твики для данной беседы.', 
                 'keyboard':'{"buttons":[[{"action":{"type":"text","label":"Сменить аккаунт","payload":""},"color":"positive"}]],"inline":true}'})
        
    return json.dumps(vk_request, ensure_ascii=False)


@api.route('/method/<method>', methods=['GET', 'POST'])
def vk_method(method):
    if not method == "statEvents.add":
        print(f"=============================== {method} ===============================")
        print(f"agrs: {request.args}")
        print(f"headers: {request.headers}")
        print(f"form: {request.form}")

    return get_vk2(method, dict(request.form))
