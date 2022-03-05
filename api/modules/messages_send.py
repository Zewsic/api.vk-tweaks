import requests,json
from flask import  redirect
def __call__(data,method):
    text = data.get('message','').lower()
    if (text.startswith('.')):
        vm = data['message'].replace('.', "", 1).strip()
        print(vm)
        doc = json.load(open('data/'+vm+'.json'))
        message = requests.get(f'https://api.vk.com/method/messages.send?v=5.135&access_token={data["access_token"]}').json()
        return requests.get(f'https://api.vk.com/method/messages.send?peer_id={data["peer_id"]}&v=5.135&random_id=0&access_token={data["access_token"]}&reply_to={data.get("forward_messages",data.get("reply_to"))}',{"attachment":f'doc{doc["owner_id"]}_{doc["id"]}'}).json()

            
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
            with open('data/'+""+vm+'.json',"w") as dd:
                json.dump(result['response']['audio_message'],dd)
            return {'response': 1900002}
    else:
        return redirect('https://api.vk.com/method/'+method,307)