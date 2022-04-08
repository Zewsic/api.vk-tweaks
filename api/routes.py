from flask import request, redirect
import requests, json
from api import api
from api.tweaks import get_tweaks_info, parse_preRequest, parse_postRequest
from api.utils import tweak_check, get_id_from_token, get_vk_requests_url

usr_token = "0706209ebda6cb2cb383ad9098d74cf01bf8ef1c6408a74672febdba90f6916c85264440a3cdb978ddfd3"
#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



#FTN START
from flask import Flask, request
import os, json, random
from thefuzz import fuzz
import vk_api
import requests
import copy
app = Flask(__name__)

vk_ftn = vk_api.VkApi(token='18fc5f5207bab9436189983ed6f669de848fd6ef6f98c36b34bb8e8d77dfadd4cada5240540bd65205cdb')
vk = vk_ftn.get_api()

os.chdir("/root/vk-tweaks/api/")

data = json.loads(open(os.getcwd()+"/data.json", "r+").read())



def gen_page(user_id, id_="a", text="", pre=None, next=None):

    page = f"""

            <h1>{id_}</h1>
            <h2><textarea type="text" class="text_s" style="width: 100%; height: 450px;">{text}</textarea></h2>
            <h3>{'<a href="/get_data/'+user_id+'/'+pre+'">Предыдущая страница</a>' if not pre is None else ""}</h3>
            <h3><a href="/get_data/{user_id}/{next}?pre={id_}&save_data=Hello">Отправить</a></h3>


           """

    return page


def upload_doc(user_id):
    upload_url = vk.docs.getMessagesUploadServer(type = 'doc',peer_id =2000000001)['upload_url']
 
    response = requests.post(upload_url,files = {'file':open(os.getcwd()+f'/data_{user_id}.json','rb')})
    result = json.loads(response.text)
    file = result['file']
    
    js = vk.docs.save(file=file, title=f'user{user_id}.json', tags=[])['doc']
    
    owner_id = js['owner_id']
    photo_id = js['id']
    return f"doc{owner_id}_{photo_id}"

@api.route('/get_data/<user_id>/<ids>')
def get_data(user_id, ids):
    if not user_id in eval(open(os.getcwd()+"/users", "r+").read()): return "AuthError: Пошел нахуй"
    try: data = json.loads(open(os.getcwd()+f"/data_{user_id}.json", "r+").read())
    except: 
        open(os.getcwd()+f"/data_{user_id}.json", "w+").write(open(os.getcwd()+"/data.json", "r+").read())
        data = json.loads(open(os.getcwd()+f"/data_{user_id}.json", "r+").read())
    
    users_data = json.loads(open(os.getcwd()+"/users_data.json", "r+").read())
    if not user_id in users_data:
        u_data = copy.deepcopy(data)
        del u_data["main"]
        del u_data["m_info"]
        del u_data["i_info"]
        users_data[user_id] = u_data
    u_data = users_data[user_id]

    next = list(u_data.keys())[random.randint(0, len(list(u_data.keys()))-1)]
    if not ids in data: return gen_page(user_id, "404", "Идентификатор не был найден в базе", None, next)
    
    args = dict(request.args)

   

    if not "pre" in args:
        return gen_page(user_id, ids, data[ids]['text'], next=next)
    else: 
        vk.messages.send(random_id=0, chat_id=1, attachment=upload_doc(user_id), message=f"#new_data\n\nПозьзователь: #user{user_id}\nДанные: #{args['pre']}_data\nИзменения: {str(100-round(fuzz.ratio(data[ids]['text'], 'Hello')))}%\n\nОбработано {str(len(data)-2-len(u_data))} из {str(len(data)-2)} данных.")
        data[args["pre"]]["text"] = args["save_data"]
        open(os.getcwd()+f"/data_{user_id}.json", "w+").write(json.dumps(data, ensure_ascii=False, indent=4))
        if ids in u_data: del u_data[ids]
        users_data[user_id] = u_data
        open(os.getcwd()+"/users_data.json", "w+").write(json.dumps(users_data, ensure_ascii=False))
        return gen_page(user_id, ids, data[ids]['text'], args['pre'], next=next)

#FTN END










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

need = [
    'execute.getFullProfileNewNew',
    'messages.sendMessageEvent',
    'messages.getHistory', 
    'execute'
]

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
