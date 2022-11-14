import csv
import logging
import datetime
from os import listdir


def read_file(file_name: str = 'data_file.csv') -> list:
    """
    функция считывает данные из csv файла
    file_name - название файла, из которого считываем
    """
    try:
        with open(file_name, newline='') as file:
            reader = csv.reader(file)
            data = list()
            for row in reader:
                data.append(row)
            return data
    except OSError as error:
        logging.error(f'Ошибка, не удалось открыть файл: {error}')


def get_value_from_0_type_file(required_date: datetime, data_file_name: str = 'data_file.csv') -> [float, None]:
    """
    функция ищет в исходном файле данные за конкретный день, если они есть - возвращает данные за этот день, если нет -
    возвращает None
    required_date - дата, для которой ищем данные
    data_file_name - название файла с данными
    """
    data_list = read_file(data_file_name)
    array_date = list()
    array_val = list()
    for item in data_list:
        tmp_array = item[0].split(', ')
        tmp_date_array = tmp_array[0].split('-')
        tmp_date = datetime.date(int(tmp_date_array[0]), int(tmp_date_array[1]), int(tmp_date_array[2]))
        value = float(tmp_array[1])
        array_date.append(tmp_date)
        array_val.append(value)
    if required_date in array_date:
        required_index = array_date.index(required_date)
        return array_val[required_index]
    else:
        return None


def get_value_from_1_type_file(required_date: datetime, data_file_name_1: str = 'X.csv',
                               data_file_name_2: str = 'Y.csv') -> [float, None]:
    """
    функция ищет конкретную дату в файле, котором хранятся данные, если она есть - возвращает данные за этот день из
    файла с данными, если нет - возвращает None
    required_date - дата, для которой ищем данные
    data_file_name_1 - имя файла с датами
    data_file_name_2 - имя файла с данными
    """
    data_list_x = read_file(data_file_name_1)
    data_list_y = read_file(data_file_name_2)
    array_date = list()
    array_val = list()
    for item in data_list_x:
        tmp_date_array = item[0].split('-')
        tmp_date = datetime.date(int(tmp_date_array[0]), int(tmp_date_array[1]), int(tmp_date_array[2]))
        array_date.append(tmp_date)
    for item in data_list_y:
        array_val.append(float(item[0]))
    if required_date in array_date:
        required_index = array_date.index(required_date)
        return array_val[required_index]
    else:
        return None


def get_value_from_2_type_file(required_date: datetime) -> [float, None]:
    """
    функция ищет файл, содержащий данные за год, указанный в искомой дате, считывает его и ищет в нём данные для искомой
    даты, если они есть - возвращает их, если нет - возвращает None
    required_date - дата, для которой ищем данные
    """
    file_names = listdir()
    for item in file_names:
        if '.csv' in item:
            if f'{required_date.year}' in item:
                date_1_str = item.split('_')[0]
                date_2_str = item.split('_')[1].split('.')[0]
                date_1 = datetime.date(int(date_1_str[:4]), int(date_1_str[4:6]), int(date_1_str[6:8]))
                date_2 = datetime.date(int(date_2_str[:4]), int(date_2_str[4:6]), int(date_2_str[6:8]))
                if date_2 - date_1 > datetime.timedelta(7):
                    file_name = item
                    data_list = read_file(file_name)
                    for obj in data_list:
                        tmp_array = obj[0].split(', ')
                        tmp_date_array = tmp_array[0].split('-')
                        tmp_date = datetime.date(int(tmp_date_array[0]), int(tmp_date_array[1]), int(tmp_date_array[2]))
                        if required_date == tmp_date:
                            return float(tmp_array[1])
    return None


def get_value_from_3_type_file(required_date: datetime) -> [float, None]:
    """
    функция ищет файл, который содержит данные за тот год и за ту неделю, которые содержат искомую дату, считывает его
    и ищет в нём данные для искомой даты, если они есть - возвращает их, если нет - возвращает None
    required_date - дата, для которой ищем данные
    """
    file_names = listdir()
    for item in file_names:
        if '.csv' in item:
            if f'{required_date.year}' in item:
                date_1_str = item.split('_')[0]
                date_2_str = item.split('_')[1].split('.')[0]
                date_1 = datetime.date(int(date_1_str[:4]), int(date_1_str[4:6]), int(date_1_str[6:8]))
                date_2 = datetime.date(int(date_2_str[:4]), int(date_2_str[4:6]), int(date_2_str[6:8]))
                if date_2 - date_1 < datetime.timedelta(7) and date_1 <= required_date <= date_2:
                    file_name = item
                    data_list = read_file(file_name)
                    for obj in data_list:
                        tmp_array = obj[0].split(', ')
                        tmp_date_array = tmp_array[0].split('-')
                        tmp_date = datetime.date(int(tmp_date_array[0]), int(tmp_date_array[1]), int(tmp_date_array[2]))
                        if required_date == tmp_date:
                            return float(tmp_array[1])
    return None


def next(data_file_name: str = 'data_file.csv') -> (datetime, float):
    """
    функция при первом вызове возвращает данные для самой ранней даты, при последующих вызовах возвращает данные для
    следующей по порядку даты, для которой есть данные
    data_file_name - название файла с данными
    """
    data_list = read_file(data_file_name)
    tmp_array = data_list[-(1 + next.counter)][0].split(', ')
    tmp_date_array = tmp_array[0].split('-')
    tmp_date = datetime.date(int(tmp_date_array[0]), int(tmp_date_array[1]), int(tmp_date_array[2]))
    value = float(tmp_array[1])
    next.counter += 1
    return tmp_date, value


next.counter = 0


if __name__ == "__main__":
    date_str = '2022-10-15'
    tmp = date_str.split('-')
    date = datetime.date(int(tmp[0]), int(tmp[1]), int(tmp[2]))
    print(next())
    print(next())
    print(next())
    print(get_value_from_0_type_file(date))
    print(get_value_from_1_type_file(date))
    print(get_value_from_2_type_file(date))
    print(get_value_from_3_type_file(date))
