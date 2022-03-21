def get_vk_requests_url(method, data):
    new_data = []
    data_keys = list(data.keys())
    for key in data_keys:
        new_data.append({"key":key, "value":data[key]})

    vk_requests_url = f"https://api.vk.com/method/{method}?"

    for param in new_data:
        vk_requests_url += f"{param['key']}={param['value']}&"

    vk_requests_url = vk_requests_url[0: -1]
    return vk_requests_url

  
def tweak_check(user_id=0, tweak_id=0):
    return not tweak_id == 2

def get_id_from_token(token):
    return 1
