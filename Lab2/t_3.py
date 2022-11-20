from t_1 import write_string_to_csv
from t_1 import read_file


def partition_data_n_files_weeks(data_file_name: str = 'data_file.csv') -> None:
    """
    функция разделяет исходный массив данных на n файлов, где каждый файл содержит данные за конкретную неделю
    каждый файл будет назван так: годмесяцдень_годмесяцдень, по первой и последней датам за эту неделю
    data_file_name - название файла с данными
    """
    data_list = read_file(data_file_name)
    last_date = data_list[0]['date']
    last_week = last_date.isocalendar()[1]
    array = list()
    for item in data_list:
        tmp_date = item['date']
        if tmp_date.isocalendar()[1] == last_week:
            array.append(item)
        else:
            file_name = f'{array[-1]["date"].year}{array[-1]["date"].month:02d}{array[-1]["date"].day:02d}_' \
                        f'{array[0]["date"].year}{array[0]["date"].month:02d}{array[0]["date"].day:02d}.csv'
            for i in range(len(array)):
                write_string_to_csv(f'{array[i]["date"]}, {array[i]["value"]}', file_name)
            array.clear()
            array.append(item)
            last_week = tmp_date.isocalendar()[1]
    file_name = f'{array[-1]["date"].year}{array[-1]["date"].month:02d}{array[-1]["date"].day:02d}_' \
                f'{array[0]["date"].year}{array[0]["date"].month:02d}{array[0]["date"].day:02d}.csv'
    for i in range(len(array)):
        write_string_to_csv(f'{array[i]["date"]}, {array[i]["value"]}', file_name)


if __name__ == "__main__":
    partition_data_n_files_weeks()
