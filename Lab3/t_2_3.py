from t_1 import write_string_to_csv
from t_1 import read_file
import enum


class FunctionStatePartition(enum.Enum):
    partition_years = 1
    partition_weeks = 2


def partition_data_n_files_years_or_weeks(type_file: FunctionStatePartition, path: str, data_file_name: str = 'data_file.csv') -> None:
    """
    функция разделяет исходный массив данных на n файлов, где каждый файл содержит данные за конкретный год
    или неделю, каждый файл будет назван так: годмесяцдень_годмесяцдень, по первой и последней датам в файле
    type_file - параметр, который контролирует разбивает функция файлы по годам или по неделям
    data_file_name - название файла с данными(или путь)
    path - путь по которому будут созданы файлы
    """
    try:
        data_list = read_file(data_file_name)
        last_date = data_list[0]['date']
        if type_file == FunctionStatePartition.partition_years:
            last_year = last_date.year
        else:
            if type_file == FunctionStatePartition.partition_weeks:
                last_week = last_date.isocalendar()[1]
        array = list()
        for item in data_list:
            tmp_date = item['date']
            if type_file == FunctionStatePartition.partition_years:
                if tmp_date.year == last_year:
                    array.append(item)
                else:
                    file_name = f'{last_year}{array[-1]["date"].month:02d}{array[-1]["date"].day:02d}_' \
                                f'{last_year}{array[0]["date"].month:02d}{array[0]["date"].day:02d}.csv'
                    file_name = f'{path}/{file_name}'
                    for i in range(len(array)):
                        write_string_to_csv(f'{array[i]["date"]}, {array[i]["value"]}', file_name)
                    last_year = tmp_date.year
                    array.clear()
                    array.append(item)
            else:
                if type_file == FunctionStatePartition.partition_weeks:
                    if tmp_date.isocalendar()[1] == last_week:
                        array.append(item)
                    else:
                        file_name = f'{array[-1]["date"].year}{array[-1]["date"].month:02d}{array[-1]["date"].day:02d}_' \
                                    f'{array[0]["date"].year}{array[0]["date"].month:02d}{array[0]["date"].day:02d}.csv'
                        file_name = f'{path}/{file_name}'
                        for i in range(len(array)):
                            write_string_to_csv(f'{array[i]["date"]}, {array[i]["value"]}', file_name)
                        last_week = tmp_date.isocalendar()[1]
                        array.clear()
                        array.append(item)
        if type_file == FunctionStatePartition.partition_years:
            file_name = f'{last_year}{array[-1]["date"].month:02d}{array[-1]["date"].day:02d}_' \
                        f'{last_year}{array[0]["date"].month:02d}{array[0]["date"].day:02d}.csv'
            file_name = f'{path}/{file_name}'
        else:
            if type_file == FunctionStatePartition.partition_weeks:
                file_name = f'{array[-1]["date"].year}{array[-1]["date"].month:02d}{array[-1]["date"].day:02d}_' \
                            f'{array[0]["date"].year}{array[0]["date"].month:02d}{array[0]["date"].day:02d}.csv'
                file_name = f'{path}/{file_name}'
        for i in range(len(array)):
            write_string_to_csv(f'{array[i]["date"]}, {array[i]["value"]}', file_name)
    except OSError as error:
        raise error
