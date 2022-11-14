import csv
import logging
import datetime


def write_string_to_csv(data_string: str, file_name: str = 'res_file.csv') -> None:
    """
        функция дописывает в конец csv файла строку data_string
        data_string - строка, которую записываем
        file_name - название файла, в который записываем
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


def partition_data_n_files_years(data_file_name: str = 'data_file.csv') -> None:
    """
    функция разделяет исходный массив данных на n файлов, где каждый файл содержит данные за конкретный год
    каждый файл будет назван так: годмесяцдень_годмесяцдень, по первой и последней датам за этот год
    data_file_name - название файла с данными
    """
    data_list = read_file(data_file_name)
    last_str = data_list[0][0]
    last_array = last_str.split(', ')
    last_date_array = last_array[0].split('-')
    last_date = datetime.date(int(last_date_array[0]), int(last_date_array[1]), int(last_date_array[2]))
    last_year = last_date.year
    array_date = list()
    array_val = list()
    for item in data_list:
        tmp_array = item[0].split(', ')
        tmp_date_array = tmp_array[0].split('-')
        tmp_date = datetime.date(int(tmp_date_array[0]), int(tmp_date_array[1]), int(tmp_date_array[2]))
        if tmp_date.year == last_year:
            array_date.append(tmp_date)
            array_val.append(tmp_array[1])
        else:
            file_name = f'{last_year}{array_date[-1].month:02d}{array_date[-1].day:02d}_' \
                        f'{last_year}{array_date[0].month:02d}{array_date[0].day:02d}.csv'
            for i in range(len(array_date)):
                write_string_to_csv(f'{array_date[i]}, {array_val[i]}', file_name)
            last_year = tmp_date.year
            array_date.clear()
            array_val.clear()
            array_date.append(tmp_date)
            array_val.append(tmp_array[1])
    file_name = f'{last_year}{array_date[-1].month:02d}{array_date[-1].day:02d}_' \
                f'{last_year}{array_date[0].month:02d}{array_date[0].day:02d}.csv'
    for i in range(len(array_date)):
        write_string_to_csv(f'{array_date[i]}, {array_val[i]}', file_name)


if __name__ == "__main__":
    partition_data_n_files_years()
