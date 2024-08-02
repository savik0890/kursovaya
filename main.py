import time
import requests
from connector import VK
from config import photos_dir
from tqdm import tqdm


user_id = 'asdasdqwer'
vk = VK(user_id)
user_photos = vk.get_list_avatars()
photos = user_photos['response']['items']


for photo in tqdm(photos, desc=f'Скачивание аватарок {user_id}'):
    likes = photo['likes']['count']
    photo_content = requests.get(photo['sizes'][-1]['url'])
    with open(f"{photos_dir}{likes}.jpg", 'wb') as new_photo:
        new_photo.write(photo_content.content)
    new_photo.close()
    time.sleep(1)


