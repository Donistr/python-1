from t_1 import read_file
import datetime
from os import listdir
import csv
import logging
import re
import enum


class FunctionStateGetValue(enum.Enum):
    dates_only_file = 1
    values_only_file = 2
    basic_file = 3
    year_file = 4
    week_file = 5


def get_value_from_basic_or_year_or_week_file(required_date: datetime, type_file: FunctionStateGetValue, path: str,
                                              data_file_0_type_name: str = 'data_file.csv') -> [float, None]:
    """
    функция ищет конкретную дату в файле, в котором хранятся данные, если она есть - возвращает данные за этот день из
    файла с данными, если нет - возвращает None
    required_date - дата, для которой ищем данные
    type_file - параметр, который контролирует из файла какого типа будут считываться данные
    path - путь к папке с файлами
    data_file_0_type_name - название исходного файла
    """
    file_name = ''
    if type_file == FunctionStateGetValue.basic_file:
        file_name = f'{path}/{data_file_0_type_name}'
    else:
        if type_file == FunctionStateGetValue.year_file or type_file == FunctionStateGetValue.week_file:
            file_names = listdir(path)
            for item in file_names:
                if '.csv' in item:
                    if f'{required_date.year}' in item:
                        date_1_str = item.split('_')[0]
                        date_2_str = item.split('_')[1].split('.')[0]
                        date_1 = datetime.date(int(date_1_str[:4]), int(date_1_str[4:6]), int(date_1_str[6:8]))
                        date_2 = datetime.date(int(date_2_str[:4]), int(date_2_str[4:6]), int(date_2_str[6:8]))
                        if type_file == FunctionStateGetValue.year_file and date_2 - date_1 > datetime.timedelta(7):
                            file_name = f'{path}/{item}'
                        else:
                            if type_file == FunctionStateGetValue.week_file and date_2 - date_1 < datetime.timedelta(7) and \
                                    date_1 <= required_date <= date_2:
                                file_name = f'{path}/{item}'
    if file_name == '':
        return None
    data_list = read_file(file_name)
    for obj in data_list:
        if required_date == obj['date']:
            return obj['value']
    return None


def read_dates_only_or_values_only_file(file_name: str, type_file: FunctionStateGetValue) -> list:
    """
    функция считывает дыти или значения из файла
    file_name - название файла, из которого считываем(или путь)
    type_file - параметр, который контролирует считывает функция данный из файла с датами или из файла со значениями
    """
    try:
        with open(file_name, newline='') as file:
            reader = csv.reader(file)
            data = list()
            for row in reader:
                if type_file == FunctionStateGetValue.dates_only_file:
                    str_date = re.match('\d{4}-\d\d-\d\d', row[0]).group(0)
                    tmp_date = datetime.datetime.strptime(str_date, '%Y-%m-%d').date()
                    data.append(tmp_date)
                else:
                    if type_file == FunctionStateGetValue.values_only_file:
                        str_value = re.match('(?:\d*\.\d+|\d+)', row[0]).group(0)
                        tmp_value = float(str_value)
                        data.append(tmp_value)
            return data
    except OSError as error:
        logging.error(f'Ошибка, не удалось открыть файл: {error}')


def get_value_from_dates_only_and_values_only_files(required_date: datetime, data_file_name_1: str = 'X.csv',
                                                    data_file_name_2: str = 'Y.csv') -> [float, None]:
    """
    функция ищет конкретную дату в файле, в котором хранятся данные, если она есть - возвращает данные за этот день из
    файла с данными, если нет - возвращает None
    required_date - дата, для которой ищем данные
    data_file_name_1 - имя файла с датами(или путь)
    data_file_name_2 - имя файла с данными(или путь)
    """
    data_list_x = read_dates_only_or_values_only_file(data_file_name_1, FunctionStateGetValue.dates_only_file)
    data_list_y = read_dates_only_or_values_only_file(data_file_name_2, FunctionStateGetValue.values_only_file)
    if required_date in data_list_x:
        required_index = data_list_x.index(required_date)
        return data_list_y[required_index]
    else:
        return None


def next(counter: int, data_file_name: str = 'data_file.csv') -> (datetime, float):
    """
    функция при первом вызове возвращает данные для самой ранней даты, при последующих вызовах возвращает данные для
    следующей по порядку даты, для которой есть данные
    data_file_name - название файла с данными(или путь)
    """
    data_list = read_file(data_file_name)
    return data_list[-counter]['date'], data_list[-counter]['value']
