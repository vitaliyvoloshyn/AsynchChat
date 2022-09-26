'''
Задание на закрепление знаний по модулю CSV. Написать скрипт, осуществляющий выборку
определенных данных из файлов info_1.txt, info_2.txt, info_3.txt и формирующий новый
«отчетный» файл в формате CSV. Для этого:

a. Создать функцию get_data(), в которой в цикле осуществляется перебор файлов с
данными, их открытие и считывание данных. В этой функции из считанных данных
необходимо с помощью регулярных выражений извлечь значения параметров
«Изготовитель системы», «Название ОС», «Код продукта», «Тип системы». Значения
каждого параметра поместить в соответствующий список. Должно получиться четыре
списка — например, os_prod_list, os_name_list, os_code_list, os_type_list. В этой же
функции создать главный список для хранения данных отчета — например, main_data
— и поместить в него названия столбцов отчета в виде списка: «Изготовитель
системы», «Название ОС», «Код продукта», «Тип системы». Значения для этих
столбцов также оформить в виде списка и поместить в файл main_data (также для
каждого файла);

b. Создать функцию write_to_csv(), в которую передавать ссылку на CSV-файл. В этой
функции реализовать получение данных через вызов функции get_data(), а также
сохранение подготовленных данных в соответствующий CSV-файл;

c. Проверить работу программы через вызов функции write_to_csv()
'''

import csv
import os
import re
from itertools import zip_longest

SOURCE_DATA_PATH = 'source_data'
OUTPUT_FILE = 'main_data.csv'


def get_data() -> dict:
    """читает файлы с исходными данными и возвращает словарь со значениями параметров
    «Изготовитель системы», «Название ОС», «Код продукта», «Тип системы»"""
    # проверить наличие исходных данных
    if not __check_source_data():
        exit(1)

    # задаем структуру хранения данных
    main_data = {
        'os_prod': {'list': [], 're': 'Изготовитель системы:.*', 'title': 'Изготовитель системы'},
        'os_name': {'list': [], 're': 'Название ОС:.*', 'title': 'Название ОС'},
        'os_type': {'list': [], 're': 'Тип системы:.*', 'title': 'Тип системы'},
        'os_code': {'list': [], 're': 'Код продукта:.*', 'title': 'Код продукта'},
    }
    # чтение файлов
    for root, dirs, files in os.walk(SOURCE_DATA_PATH):
        for file in files:
            with open(os.path.join(SOURCE_DATA_PATH, file), "r", encoding="windows-1251") as f:
                strings = f.read()
                for item in main_data.values():
                    find_str = re.findall(fr"{item['re']}",
                                          strings)  # поиск нужной строки в файле. напр. "Изготовитель системы:             LENOVO"
                    if find_str:
                        find_str = re.sub(r"\s{2,30}", "",
                                          find_str[0])  # удаляем пробелы между параметром и его значением
                        item['list'].append(find_str[find_str.find(":") + 1:])  # добавляем в список значение параметра
    return main_data


def write_to_csv(file: str) -> None:
    """Сохраняет данные в файл CSV"""
    data = get_data() # получаем данные
    header_row = []
    data_rows = []
    # проходимся по исходным данным и формируем заголовки и данные для вывода в файл
    for items in data.values():
        header_row.append(items['title'])
        data_rows.append(items['list'])
    # комбинируем списки с данными
    data_rows = zip_longest(*data_rows, fillvalue='')

    # запись в файл
    with open(file, "w", encoding='utf-8', newline='') as f:
        file_writer = csv.writer(f)
        file_writer.writerow(header_row)
        file_writer.writerows(data_rows)



def __check_source_data() -> bool:
    """проверяет наличие исходных данных"""
    try:
        if not os.listdir(SOURCE_DATA_PATH):
            raise FileExistsError
    except FileNotFoundError:
        print("Отсутсвует директория с исходными данными")
        return False
    except FileExistsError:
        print("Отсутсвуют файлы с исходными данными")
        return False
    return True


if __name__ == "__main__":
    write_to_csv(OUTPUT_FILE)
