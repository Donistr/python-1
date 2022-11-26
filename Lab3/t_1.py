import csv
import logging
import re
import datetime


def write_string_to_csv(data_string: str, file_name: str = 'res_file.csv') -> None:
    """
        функция дописывает в конец csv файла строку data_string
        data_string - строка, которую записываем
        file_name - название файла, в который записываем(или путь)
    """
    try:
        with open(file_name, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow({data_string})
    except OSError as error:
        logging.error(f'Ошибка, не удалось открыть файл: {error}')


def read_file(file_name: str = 'data_file.csv') -> list:
    """
    функция считывает данные из csv файла
    file_name - название файла, из которого считываем(или путь)
    """
    try:
        with open(file_name, newline='') as file:
            reader = csv.reader(file)
            data = list()
            for row in reader:
                str_date = re.match('\d{4}-\d\d-\d\d', row[0]).group(0)
                tmp_date = datetime.datetime.strptime(str_date, '%Y-%m-%d').date()
                str_value = re.match('(?:\d*\.\d+|\d+)', row[0][12:]).group(0)
                tmp_value = float(str_value)
                data.append({'date': tmp_date, 'value': tmp_value})
            return data
    except OSError as error:
        logging.error(f'Ошибка, не удалось открыть файл: {error}')


def partition_data_two_files(data_file_name: str = 'data_file.csv', file_name_1: str = 'X.csv',
                             file_name_2: str = 'Y.csv') -> None:
    """
    функция разделяет исходный массив данных на 2 файла: в 1 даты, в другом данные
    data_file_name - название файла с данными(или путь)
    file_name_1 - название файла, в который запишутся все даты(или путь)
    file_name_2 - название файла, в который запишутся все данные(или путь)
    """
    data_list = read_file(data_file_name)
    for item in data_list:
        write_string_to_csv(item['date'], file_name_1)
        write_string_to_csv(item['value'], file_name_2)
