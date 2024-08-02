import os.path
import time
import requests
from connector import VK
from config import photos_dir
from file_manager import save_to_file
from tqdm import tqdm
from datetime import datetime


user_id = 'asdasdqwer'
#user_id = 289697403


def download_avatars(user_id: str, count=5):
    vk = VK(user_id, count)
    user_photos = vk.get_list_avatars()
    try:
        photos = user_photos['response']['items']
        for photo in tqdm(photos, desc=f'Скачивание аватарок {user_id}'):
            likes = photo['likes']['count']
            photo_content = requests.get(photo['sizes'][-1]['url'])
            if os.path.exists(f"{photos_dir}{likes}.jpg"):
                file_name = f"{likes} - {datetime.now()}.jpg"
            else:
                file_name = f"{likes}.jpg"
            save_to_file(photo_content.content, photos_dir, file_name)
            time.sleep(1)
    except KeyError:
        print('Couldnt connect to profile, it is probably closed')


if __name__ == '__main__':
    download_avatars(user_id)
