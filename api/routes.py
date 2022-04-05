from flask import request, redirect
import requests, json
from api import api
from api.tweaks import get_tweaks_info, parse_preRequest, parse_postRequest
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
    
    vk_request = parse_postRequest(method, vk_request, token)
    
        
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
        
        #try: 
        return work(method, dict(request.form))
        #except: redirect('https://api.vk.com/method/'+method,307)
    redir = redirect('https://api.vk.com/method/'+method,307) 
    return redir
