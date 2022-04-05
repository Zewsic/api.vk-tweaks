from api.tweaks_list import GetUnblocked
from api.utils import *
import requests

tweaks = [
  {"name":"GetUnblocked", "desk":"Позволяет вам просматривать страницы пользователей, если они вас заблокировали.", "author":"Zewsic", "uses":"0", "ver":"1.0 BETA"},
  {"name":"Everyone UserID", "desk":"Принудительно использует UserID, даже если у пользователя имеется короткое имя.", "author":"Zewsic", "uses":"0", "ver":"IN DEV"},
  {"name":"Local Chat Editor", "desk":"Позволяет локально редактировать информацию о диалоге.", "author":"Zewsic", "uses":"0", "ver":"IN DEV"}
]

nl = "\n"

def get_tweaks_info(token):
    infos = []
    id_ = 0
    for tweak in tweaks:
        lb, pl, cl = ("Деактивировать", f"tweak_off {str(id_)}", "negative") if tweak_check(get_id_from_token(token), id_) else ("Активировать",f"tweak_on {str(id_)}", "positive")
        infos.append({'date': 9000000000, 'from_id': -210967996, 'id': 1900001+id_, 'out': 0, 'attachments': [],
           'conversation_message_id': 1900001+id_, 'fwd_messages': [], 'important': False, 'is_hidden': False, 
           'peer_id': -210967996, 'random_id': 0, 
           'text': f'{tweak["name"]}{nl}Версия: {tweak["ver"]}{nl}{nl}{tweak["desk"]}{nl}{nl}Автор: {tweak["author"]}{nl}Активировано на {tweak["uses"]} аккаунтах.', 
           'keyboard':{"one_time":False,"buttons":
                       [[{"action":{"label":lb,"type":"callback","payload":pl},"color":cl}]]
                       ,"author_id":-210967996,"inline":True}})
        id_ += 1
    return infos
 
def parse_preRequest(method, data, token):
  if method == "execute.getFullProfileNewNew": 
    if tweak_check(get_id_from_token(token), 0):
      data = GetUnblocked.execute(data)
  if method == "messages.sendMessageEvent":
    requests.get(f'https://api.vk.com/method/messages.send?peer_id={data["peer_id"]}&v=5.135&random_id=0&message=VK Tweaks Callback: {data["payload"]}&access_token={data["access_token"]}').text
  return data
    

def parse_postRequest(method, vk_request, token):
  if method == "messages.getHistory": #VK Tweaks Menu
    if vk_request["response"]["conversations"][0]["peer"]["id"] == -210967996:
        vk_request["response"]["items"] = get_tweaks_info(token)
    else:
        if tweak_check(get_id_from_token(token), 2): #Chat Editor
            vk_request["response"]["items"].append(
                {'date': 9000000000, 'from_id': -210967996, 'id': 1900001, 'out': 0, 'attachments': [], 'conversation_message_id': 1900001, 'fwd_messages': [], 'important': False, 'is_hidden': False, 'peer_id': vk_request["response"]["conversations"][0]["peer"]["id"], 'random_id': 0, 'text': 'Твики для данной беседы.', 
                'keyboard':{"one_time":False,"buttons":[[{"action":{"label":"Тестовая кнопка","type":"callback","payload":"cmd_test"},"color":"positive"}]],"author_id":-210967996,"inline":True}})
        if tweak_check(get_id_from_token(token), 3): #Neirobot
            vk_request["response"]["items"][0]["keyboard"] = {"one_time":True,"buttons":[[{"action":{"label":f"Ответ нейробота {str(i+1)}","type":"text"},"color":"secondary"}] for i in range(3)],"author_id":vk_request["response"]["items"][0]['from_id'], "inline":False}
  return vk_request

  


        
