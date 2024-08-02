import json
import os.path
import time
import requests
import file_manager
from connector import VK, Yandex
from config import photos_dir
from file_manager import save_to_file
from tqdm import tqdm
from datetime import datetime
from environs import Env


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
                file_name = f"{likes} - {datetime.now().strftime('%m-%d-%Y %H-%M-%S')}.jpg"
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


def upload_to_yandex_disk(user_id, files):
    env = Env()
    env.read_env()
    TOKEN = env('TOKEN')

    ya_disk = Yandex(TOKEN, user_id=user_id)

    # Проверяет, есть ли уже папка на яндекс диске
    if ya_disk.yandex_find_dir().status_code == 404:
        ya_disk.yandex_create_dir()
    else:
        return f"Directory {user_id} exists"

    # Из полученного json объекта берет имена файлов, которые нужно загрузить на диск
    for file in tqdm(files.get('images'), desc=f'Загрузка на Я.Диск в папку {user_id}'):
        # Запрашиваем у яндекса URL для загрузки файла
        upload_url = ya_disk.yandex_get_file_url(filename=file['file_name']).text
        try:
            with open(f"{photos_dir}{file['file_name']}", 'rb') as f:
                # Загружаем файл по полученному URL
                ya_disk.yandex_upload_file(json.loads(upload_url)['href'], f)
        except KeyError:
            pass


if __name__ == '__main__':
    user_id = str(input('Введите id пользователя VK: '))
    json_files = download_avatars(user_id)
    with open('download_report.json', 'w') as file:
        file.write(json.dumps(json_files))
    file.close()
    upload_to_yandex_disk(user_id, json_files)
    file_manager.clean_tmp_dir(photos_dir)






