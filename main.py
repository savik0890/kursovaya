import os.path
import time
import requests
from connector import VK
from config import photos_dir
from file_manager import save_to_file
from tqdm import tqdm
from datetime import datetime


def download_avatars(user_id: str, count=5):
    """
    Скачивание аватарок пользователя через API VK
    :param user_id: ID пользователя VK, чьи фотографии нужно скачать
    :param count: Количество фотографий, которое нужно скачать (default 5)
    :return: Json объект с информацией о всех скачанных файлов (имя, размер)
    """
    vk = VK(user_id, count)
    user_photos = vk.get_list_avatars()

    try:
        json_dict = {'username': user_id}
        # Создание списка информации о фото
        photos_info = []

        # Получение списка словарей из json объекта с информацией о каждом фото
        photos = user_photos['response']['items']

        for photo in tqdm(photos, desc=f'Скачивание аватарок {user_id}'):
            # Количество лайков у фото
            likes = photo['likes']['count']

            # Скачивание экземпляра с самым большим размером
            photo_content = requests.get(photo['sizes'][-1]['url'])

            # Если фото с таким количеством лайков уже скачано - добавить timestamp скачивания
            if os.path.exists(f"{photos_dir}{likes}.jpg"):
                file_name = f"{likes} - {datetime.now()}.jpg"
            else:
                file_name = f"{likes}.jpg"
            
            # Сохраняем бинарный поток данных в jpg файл
            save_to_file(photo_content.content, photos_dir, file_name)

            # Пауза 1 сек для корректного отображения progressbar
            time.sleep(1)

            photos_info.append({'file_name': file_name, 'size': f"{photo['sizes'][-1]['height']}x{photo['sizes'][-1]['width']}"})
        json_dict.update({'images': photos_info})
        return json_dict
    except KeyError:
        return 'Couldnt connect to profile, it is probably closed'


if __name__ == '__main__':
    user_id = 'asdasdqwer'
    #user_id = 289697403
    print(download_avatars(user_id))
