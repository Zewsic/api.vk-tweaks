from flask import request, redirect
import requests, json
from api import api
from api.tweaks import get_tweaks_info
from api.utils import tweak_check, get_id_from_token, get_vk_requests_url

usr_token = "0706209ebda6cb2cb383ad9098d74cf01bf8ef1c6408a74672febdba90f6916c85264440a3cdb978ddfd3"

methods = []
def work(method, data):
    
    #INIT
    full_request = {}
    token = data["access_token"]
    vk_request_url = ""
    
    #PRE-REQUEST TWEAKS
    if method == "execute.getFullProfileNewNew": 
        if tweak_check(get_id_from_token(token), 0): #Get Unblocked
            data["access_token"] = usr_token
    if method == "messages.sendMessageEvent":
        if data['payload'] == "cmd_test":
            requests.get(f'https://api.vk.com/method/messages.send?peer_id={data["peer_id"]}&v=5.135&random_id=0&message=VK Tweaks: Тестовая кнопка нажата&access_token={data["access_token"]}').text
    
    
    if vk_request_url == "": vk_requests_url = get_vk_requests_url(method, data)
    print("API URL: " + vk_requests_url)
    vk_request = requests.get(vk_requests_url).json()
    
    #POST-REQUEST TWEAKS
    if method == "messages.getHistory": #VK Tweaks Menu
        if vk_request["response"]["conversations"][0]["peer"]["id"] == -210967996:
            vk_request["response"]["items"] = get_tweaks_info()
        else:
            if tweak_check(get_id_from_token(token), 2): #Chat Editor
                vk_request["response"]["items"].append(
                    {'date': 9000000000, 'from_id': -210967996, 'id': 1900001, 'out': 0, 'attachments': [], 'conversation_message_id': 1900001, 'fwd_messages': [], 'important': False, 'is_hidden': False, 'peer_id': vk_request["response"]["conversations"][0]["peer"]["id"], 'random_id': 0, 'text': 'Твики для данной беседы.', 
                    'keyboard':{"one_time":False,"buttons":[[{"action":{"label":"Тестовая кнопка","type":"callback","payload":"cmd_test"},"color":"positive"}]],"author_id":-210967996,"inline":True}})
        
    return json.dumps(vk_request, ensure_ascii=False)


@api.route('/method/<method>', methods=['GET', 'POST'])
def vk_method(method):
    print(request.args.to_dict())
    redir = redirect('https://api.vk.com/method/'+method) 
    redir.headers = request.headers
    redir.data = request.args
    return redir
    if not method == "statEvents.add":
        print(f"=============================== {method} ===============================")
        print(f"agrs: {request.args}")
        print(f"headers: {request.headers}")
        print(f"form: {request.form}")

        return work(method, dict(request.form))
    
    #requests.get(get_vk_requests_url(method, request.form)).json()
