import requests
import json
import csv


def write_string_to_csv(data_string: str) -> None:
    """
        функция дописывает в конец csv файла строку data_string
    """
    try:
        with open("res_file.csv", 'a', newline='') as res_file:
            writer = csv.writer(res_file)
            writer.writerow({data_string})
    except OSError:
        print('Ошибка, не удалось открыть файл')


def get_valute_course(valute: str = 'USD') -> None:
    """
    функция получает курс заданной валюты на момент конкретной даты
    и записывает в файл до тех пор, пока не дойдёт до последней возможной даты
    valute - валюта для которой получаем курс
    """
    start_url_string = 'https://www.cbr-xml-daily.ru/daily_json.js'
    response = requests.get(start_url_string)
    url_text = json.loads(response.text)

    while True:
        date = url_text['Date'][:10]
        valute_course = url_text['Valute'][valute]['Value']

        print('Программа на данный момент на дате: ', date)

        res_string = date + ', ' + str(valute_course)
        write_string_to_csv(res_string)

        prev_url_string = "https:" + url_text['PreviousURL']
        prev_response = requests.get(prev_url_string)
        url_text = json.loads(prev_response.text)

        if not prev_response.ok:
            break


if __name__ == "__main__":
    get_valute_course()
