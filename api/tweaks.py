tweaks = [
  {"name":"GetUnblocked", "desk":"Позволяет вам просматривать страницы пользователей, если они вас заблокировали.", "author":"Zewsic", "uses":"0", "ver":"1.0 BETA"},
  {"name":"Force UserID", "desk":"Принудительно использует UserID, даже если у пользователя имеется короткое имя.", "author":"Zewsic", "uses":"0", "ver":"IN DEV"},
  {"name":"Local Chat Editer", "desk":"Позволяет локально редактировать информацию о диалоге.", "author":"Zewsic", "uses":"0", "ver":"IN DEV"}
]

nl = "\n"

def get_tweaks_info():
    infos = []
    id_ = 0
    for tweak in tweaks:
        infos.append({'date': 9000000000, 'from_id': -210967996, 'id': 1900001+id_, 'out': 0, 'attachments': [],
           'conversation_message_id': 1900001+id_, 'fwd_messages': [], 'important': False, 'is_hidden': False, 
           'peer_id': -210967996, 'random_id': 0, 
           'text': f'{tweak["name"]} {tweak["ver"]}{nl}{nl}{tweak["desk"]}{nl}{nl}Автор: {tweak["author"]}{nl}Активировано на {tweak["uses"]} аккаунтах.', 
           'keyboard':{"one_time":False,"buttons":
                       [[{"action":{"label":"Активировать","type":"callback","payload":"cmd_test"},"color":"positive"}]]
                       ,"author_id":-210967996,"inline":True}})
        id_ += 1
  return infos
        
