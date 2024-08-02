import requests
import json
import config


class VK:
    def __init__(self, user_id, count, version='5.131'):
        self.token = config.vk_token
        self.id = user_id
        self.version = version
        self.params = {'access_token': self.token, 'v': self.version}
        self.count = count

    def users_info(self):
        """
        Получение json объекта с информацией о пользователе VK
        """
        url = 'https://api.vk.com/method/users.get'
        params = {'user_ids': self.id}
        response = requests.get(url, params={**self.params, **params})
        return response.json()

    def get_list_avatars(self):
        """
        Получение списка аватарок пользователя
        :return: Json объект с тем количеством фотографий, которое было указано в self.count
        """
        user_id_number = self.users_info()['response'][0]['id']
        url = 'https://api.vk.com/method/photos.get'
        params = {'owner_id': user_id_number, 'album_id': 'profile', 'count': self.count, 'extended': 1}
        response = requests.get(url, params={**self.params, **params})
        return json.loads(response.text)



















