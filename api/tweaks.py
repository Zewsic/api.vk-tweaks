from api.tweaks_list import *
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
    

def parse_postRequest():
  pass

  


        
