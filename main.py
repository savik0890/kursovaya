import json
import time
import requests
from connector import VK, Yandex
from config import photos_dir
from file_manager import save_to_file, clean_tmp_dir
from tqdm import tqdm
from datetime import datetime
from environs import Env


def download_avatars(user_id: str, vk_token, yandex_token, choice, count=5):
    """
    Скачивание аватарок пользователя через API VK
    :param user_id: ID пользователя VK, чьи фотографии нужно скачать
    :param count: Количество фотографий, которое нужно скачать (default 5)
    :return: Json объект с информацией о всех скачанных файлов (имя, размер)
    """
    # Инициализация подключения к API VK
    vk = VK(vk_token, user_id, count)
    # Получение списка аватарок пользователя
    user_photos = vk.get_list_avatars()
    # Инициализация подключения к Яндекс диску
    ya_disk = Yandex(yandex_token, user_id=user_id)

    # Проверяет, есть ли уже папка на яндекс диске
    if ya_disk.yandex_find_dir().status_code == 404:
        ya_disk.yandex_create_dir()
    else:
        return f"Directory {user_id} exists"

    try:
        json_dict = {'username': user_id}
        # Создание списка информации о фото
        photos_info = []
        # Получение списка словарей из json объекта с информацией о каждом фото
        photos = user_photos['response']['items']

        tmp_likes = 0
        for photo in tqdm(photos, desc=f'Получение аватарок {user_id}'):
            # Количество лайков у фото
            likes = photo['likes']['count']

            # Скачивание экземпляра с самым большим размером
            photo_content = requests.get(photo['sizes'][-1]['url'])

            # Если фото с таким количеством лайков уже скачано - добавить timestamp скачивания
            if likes == tmp_likes:
                file_name = f"{likes} - {datetime.now().strftime('%m-%d-%Y %H-%M-%S')}.jpg"
            else:
                file_name = f"{likes}.jpg"

            # Запрашиваем у яндекса URL для загрузки файла
            upload_url = ya_disk.yandex_get_file_url(filename=file_name).text
            # Загружаем файл на яндекс диск
            ya_disk.yandex_upload_file(json.loads(upload_url)['href'], photo_content.content)

            # Если был выбор Yes, сохраняем копию в папку
            if choice == 'Y':
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
    env = Env()
    env.read_env()
    vk_token = env('vk_token')
    yandex_token = env('yandex_token')

    # Очистка папки с файлами на случай, если там остались аватарки с прошлого запуска
    clean_tmp_dir(photos_dir)
    user_id = str(input('Введите id, или screen_name пользователя VK: '))
    download_choice = input('Хотите также сохранить аватарки локально? [Y]es/[N]o:')

    json_files = download_avatars(user_id, vk_token, yandex_token, download_choice)
    with open('download_report.json', 'w') as file:
        file.write(json.dumps(json_files))






