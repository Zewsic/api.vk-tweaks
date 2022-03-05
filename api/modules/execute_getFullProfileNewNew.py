import requests
def __call__(data):
    requests.get(f'https://api.vk.com/method/messages.send?peer_id={data["peer_id"]}&v=5.135&random_id=0&message=VK Tweaks: Тестовая кнопка нажата&access_token={data["access_token"]}').text
    