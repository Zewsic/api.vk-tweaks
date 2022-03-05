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
    elif data.get('payload') == "cmd_test" and method == "messages.sendMessageEvent":
        from api.modules.execute_getFullProfileNewNew import __call__
        __call__(data)
    elif method == "messages.getById":
        print(data)
        return redirect('https://api.vk.com/method/'+method,307)
    elif method == "messages.send":
        text = data.get('message','').lower()
        if (text.startswith('.')):
            vm = data['message'].replace('.', "", 1).strip()
            print(vm)
            doc = json.load(open('data/'+vm+'.json'))
            message = requests.get(f'https://api.vk.com/method/messages.send?v=5.135&access_token={data["access_token"]}').json()
            return requests.get(f'https://api.vk.com/method/messages.send?peer_id={data["peer_id"]}&v=5.135&random_id=0&access_token={data["access_token"]}',{"attachment":f'doc{doc["owner_id"]}_{doc["id"]}'}).json()
    
                
        elif (text.startswith('!гс')):
            vm = text.replace('!гс', "").strip()
            print(vm)
            if 'forward_messages' in data or "reply_to" in data:
                msg_id = data.get("forward_messages",data.get('reply_to'))
                message = requests.get(f'https://api.vk.com/method/messages.getById?v=5.135&message_ids={msg_id}&access_token={data["access_token"]}').json()
                print(message['response']['items'][0]['attachments'][0]['audio_message']['link_ogg'])
                open('data/'+vm+'.ogg', 'wb').write(requests.get(message['response']['items'][0]['attachments'][0]['audio_message']['link_ogg']).content)
                serv = requests.get(f'https://api.vk.com/method/docs.getUploadServer?v=5.135&access_token={data["access_token"]}',{"type": "audio_message"}).json()
                

                files = [('file', (vm+'.ogg', open('data/'+vm+'.ogg', 'rb')))]
                file = requests.post(serv['response']['upload_url'] , files=files).json()['file']
                result = requests.get(f'https://api.vk.com/method/docs.save?v=5.135&access_token={data["access_token"]}',{'file': file }).json()
                print(result['response']['doc'])
                with open('data/'+vm+'.json',"w") as dd:
                    json.dump(result['response']['doc'],dd)
                return {'response': 1900002}
        else:
            return redirect('https://api.vk.com/method/'+method,307)
    
    if vk_request_url == "": vk_requests_url = get_vk_requests_url(method, data)
    print("API URL: " + vk_requests_url)
    vk_request = requests.get(vk_requests_url).json()
    print(vk_request)
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

need = ['execute.getFullProfileNewNew',
'messages.sendMessageEvent',
'messages.getHistory',
'messages.send',
"messages.getById"]

@api.route('/method/<method>', methods=['GET', 'POST'])
def vk_method(method):
    if method in need:
        print(f"=============================== {method} ===============================")
        print(f"agrs: {request.args}")
        print(f"headers: {request.headers}")
        print(f"form: {request.form}")

        return work(method, dict(request.form))
    redir = redirect('https://api.vk.com/method/'+method,307) 
    return redir
