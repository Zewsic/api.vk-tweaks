from flask import request, redirect
import requests, json
from api import api
from api.tweaks import get_tweaks_info, parse_preRequest
from api.utils import tweak_check, get_id_from_token, get_vk_requests_url

usr_token = "0706209ebda6cb2cb383ad9098d74cf01bf8ef1c6408a74672febdba90f6916c85264440a3cdb978ddfd3"


def work(method, data):
    
    #INIT
    full_request = {}
    token = data["access_token"]
    vk_request_url = ""
    
    
    data = parse_preRequest(method, data, token)
    if vk_request_url == "": vk_requests_url = get_vk_requests_url(method, data)
    print("API URL: " + vk_requests_url)
    vk_request = requests.get(vk_requests_url).json()
    
    #POST-REQUEST TWEAKS
    if method == "messages.getHistory": #VK Tweaks Menu
        if vk_request["response"]["conversations"][0]["peer"]["id"] == -210967996:
            vk_request["response"]["items"] = get_tweaks_info(token)
        else:
            if tweak_check(get_id_from_token(token), 2): #Chat Editor
                vk_request["response"]["items"].append(
                    {'date': 9000000000, 'from_id': -210967996, 'id': 1900001, 'out': 0, 'attachments': [], 'conversation_message_id': 1900001, 'fwd_messages': [], 'important': False, 'is_hidden': False, 'peer_id': vk_request["response"]["conversations"][0]["peer"]["id"], 'random_id': 0, 'text': 'Твики для данной беседы.', 
                    'keyboard':{"one_time":False,"buttons":[[{"action":{"label":"Тестовая кнопка","type":"callback","payload":"cmd_test"},"color":"positive"}]],"author_id":-210967996,"inline":True}})
            if tweak_check(get_id_from_token(token), 3): #Neirobot
                vk_request["response"]["items"][0]["keyboard"] = {"one_time":True,"buttons":[[{"action":{"label":"Ответ нейробота 1","type":"text"},"color":"secondary"}]],"author_id":vk_request["response"]["items"][0]['from_id'], "inline":False}
                
    return json.dumps(vk_request, ensure_ascii=False)

need = ['execute.getFullProfileNewNew',
'messages.sendMessageEvent',
'messages.getHistory']

@api.route('/method/<method>', methods=['GET', 'POST'])
def vk_method(method):
    if method in need:
        print(f"=============================== {method} ===============================")
        print(f"agrs: {request.args}")
        print(f"headers: {request.headers}")
        print(f"form: {request.form}")
        
        try: return work(method, dict(request.form))
        except: redirect('https://api.vk.com/method/'+method,307)
    redir = redirect('https://api.vk.com/method/'+method,307) 
    return redir
