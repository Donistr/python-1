import csv
import logging
import datetime


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


class DataIterator:
    def __init__(self, limit):
        self.limit = limit
        self.counter = 0

    def __next__(self, data_file_name: str = 'data_file.csv'):
        if self.counter < self.limit:
            data_list = read_file(data_file_name)
            tmp_array = data_list[-(1 + self.counter)][0].split(', ')
            tmp_date_array = tmp_array[0].split('-')
            tmp_date = datetime.date(int(tmp_date_array[0]), int(tmp_date_array[1]), int(tmp_date_array[2]))
            value = float(tmp_array[1])
            return tmp_date, value
        else:
            raise StopIteration
