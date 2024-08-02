import os


def save_to_file(content, tmp_dir, filename):
    """
    Сохраняет бинарный поток в файл
    :param content: бинарный поток данных
    :param tmp_dir: Директория для сохранения
    :param filename: Имя файла с расширением
    :return: None
    """
    try:
        file = open(f"{tmp_dir}{filename}", 'wb')
        file.write(content)
        file.close()
    except Exception as e:
        print(e)


def clean_tmp_dir(tmp_dir):
    """
    Очищает временную папку от всех файлов
    :param tmp_dir: Папка
    :return: None
    """
    files = os.listdir(tmp_dir)
    for file in files:
        if file.endswith('.jpg'):
            os.remove(tmp_dir + file)

