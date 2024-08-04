import requests
import json
import config


class VK:
    def __init__(self, vk_token, user_id, count, version='5.131'):
        self.token = vk_token
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


class Yandex:
    def __init__(self, token, user_id, filename=''):
        self.url = 'https://cloud-api.yandex.net'
        self.token = token
        self.user_id = user_id
        self.headers = {'Authorization': f'OAuth {self.token}'}
        self.filename = filename

    def yandex_disk_info(self):
        method = '/v1/disk'
        response = requests.get(f"{self.url}{method}", headers=self.headers)
        return response

    def yandex_find_dir(self):
        method = '/v1/disk/resources?path='
        response = requests.get(f"{self.url}{method}{self.user_id}", headers=self.headers)
        return response

    def yandex_create_dir(self):
        method = '/v1/disk/resources?path='
        response = requests.put(f"{self.url}{method}{self.user_id}", headers=self.headers)
        return response

    def yandex_get_file_url(self, filename):
        method = '/v1/disk/resources/upload?path='
        response = requests.get(f"{self.url}{method}{self.user_id}/{filename}", headers=self.headers)
        return response
    
    def yandex_upload_file(self, url, file):
        response = requests.put(url, files={'file': file})
        return response







