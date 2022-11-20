from t_1 import write_string_to_csv
from t_1 import read_file


def partition_data_n_files_years(data_file_name: str = 'data_file.csv') -> None:
    """
    функция разделяет исходный массив данных на n файлов, где каждый файл содержит данные за конкретный год
    каждый файл будет назван так: годмесяцдень_годмесяцдень, по первой и последней датам за этот год
    data_file_name - название файла с данными
    """
    data_list = read_file(data_file_name)
    last_date = data_list[0]['date']
    last_year = last_date.year
    array = list()
    for item in data_list:
        tmp_date = item['date']
        if tmp_date.year == last_year:
            array.append(item)
        else:
            file_name = f'{last_year}{array[-1]["date"].month:02d}{array[-1]["date"].day:02d}_' \
                        f'{last_year}{array[0]["date"].month:02d}{array[0]["date"].day:02d}.csv'
            for i in range(len(array)):
                write_string_to_csv(f'{array[i]["date"]}, {array[i]["value"]}', file_name)
            last_year = tmp_date.year
            array.clear()
            array.append(item)
    file_name = f'{last_year}{array[-1]["date"].month:02d}{array[-1]["date"].day:02d}_' \
                f'{last_year}{array[0]["date"].month:02d}{array[0]["date"].day:02d}.csv'
    for i in range(len(array)):
        write_string_to_csv(f'{array[i]["date"]}, {array[i]["value"]}', file_name)


if __name__ == "__main__":
    partition_data_n_files_years()
