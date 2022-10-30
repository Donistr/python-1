import requests
import json
import csv
import logging


def write_string_to_csv(data_string: str, file_name = "res_file.csv") -> None:
    """
        функция дописывает в конец csv файла строку data_string
        data_string - строка, которую записываем
        file_name - название файла, в который записываем
    """
    try:
        with open(file_name, 'a', newline='') as file_name:
            writer = csv.writer(file_name)
            writer.writerow({data_string})
    except OSError as error:
        logging.error(f'Ошибка, не удалось открыть файл: {error}')


def get_curency_course(curency: str = 'USD', start_url_string: str = 'https://www.cbr-xml-daily.ru/daily_json.js') -> None:
    """
    функция получает курс заданной валюты на момент конкретной даты
    и записывает в файл до тех пор, пока не дойдёт до последней возможной даты
    curency - валюта, для которой получаем курс
    start_url_string - стартовая ссылка, с которой начинаем парсить
    """
    response = requests.get(start_url_string)
    url_text = json.loads(response.text)

    while True:
        date = url_text['Date'][:10]
        curency_course = url_text['Valute'][curency]['Value']
        print(f'Программа на данный момент на дате: {date}')
        res_string = date + ', ' + str(curency_course)
        write_string_to_csv(res_string)
        prev_url_string = "https:" + url_text['PreviousURL']
        prev_response = requests.get(prev_url_string)
        url_text = json.loads(prev_response.text)
        if not prev_response.ok:
            print(f'Программа дошла до последней возможной даты')
            break


if __name__ == "__main__":
    get_curency_course()
