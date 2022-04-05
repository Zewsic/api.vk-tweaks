import json

headers = {
      'Connection': 'keep-alive',
      'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="98", "Opera";v="84"',
      'sec-ch-ua-mobile': '?0',
      'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.109 Safari/537.36 OPR/84.0.4316.31',
      'sec-ch-ua-platform': '"Linux"',
      'Content-Type': 'text/plain;charset=UTF-8',
      'Accept': '*/*',
      'Origin': 'https://porfirevich.ru',
      'Sec-Fetch-Site': 'cross-site',
      'Sec-Fetch-Mode': 'cors',
      'Sec-Fetch-Dest': 'empty',
      'Accept-Language': 'ru,en-US;q=0.9,en;q=0.8',
}

def execute(vk_request):
  lst = vk_request["response"]["items"][0]
  lst_t = lst["text"]
  lst_f = lst['from_id']
  
  rps = eval(str(requests.post('https://pelevin.gpt.dobro.ai/generate/', headers=headers, data=json.dumps({"prompt":lst_t,"length":30})).text))["replies"]
  lst["keyboard"] = {"one_time":True,"buttons":[[{"action":{"label":rp,"type":"text"},"color":"secondary"}] for rp in rps],"author_id":lst_f, "inline":False}
  
  vk_request["response"]["items"][0] = lst
  return vk_request
