import requests
import json
import config


class VK:
    def __init__(self, user_id, version='5.131'):
        self.token = config.vk_token
        self.id = user_id
        self.version = version
        self.params = {'access_token': self.token, 'v': self.version}

    def users_info(self):
        url = 'https://api.vk.com/method/users.get'
        params = {'user_ids': self.id}
        response = requests.get(url, params={**self.params, **params})
        return response.json()

    def get_list_photos(self):
        user_id_number = self.users_info()['response'][0]['id']
        url = 'https://api.vk.com/method/photos.get'
        params = {'owner_id': user_id_number, 'album_id': 'profile', 'count': 5, 'extended': 1}
        response = requests.get(url, params={**self.params, **params})
        return response.text

    def download_vk_photos(self):
        photos = json.loads(self.get_list_photos())
        for photo in photos['response']['items']:
            likes = photo['likes']['count']
            photo_content = requests.get(photo['sizes'][-1]['url'])
            with open(f"{config.photos_dir}{likes}.jpg", 'wb') as new_photo:
                new_photo.write(photo_content.content)
            new_photo.close()


user_id = 'asdasdqwer'
vk = VK(user_id)
print(vk.get_list_photos())
vk.download_vk_photos()














