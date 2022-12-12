import pandas as pd
import matplotlib.pyplot as plt
import re
from math import isnan
import numpy as np


def read_csv_to_dataframe(file_name: str = 'data_file.csv') -> pd.DataFrame:
    """
    функция считывает данные из csv файла, устанавливает названия колонок и убирает невалидные значения
    :param file_name: название файла
    :return: возвращает датафрейм
    """
    df = pd.read_csv(file_name, sep=', ')
    columns_array = df.columns
    df.rename(columns={columns_array[0]: 'date', columns_array[1]: 'value'}, inplace=True)
    remove_invalid_values_in_dataframe(df)
    df.date = pd.to_datetime(df.date, format='%Y-%m-%d')
    return df


def remove_invalid_values_in_dataframe(df: pd.DataFrame) -> None:
    """
    функция убирает строки с невалидными значениями
    :param df: датафрейм
    :return: ничего не возвращает
    """
    deleted_counter = 0
    i = 0
    while i < len(df['date']):
        date = df.iloc[i]['date']
        value = df.iloc[i]['value']
        if date == 0 or date is None or isnan(value) or value <= 0 or value is None:
            df.drop(index=i + deleted_counter, inplace=True)
            i -= 1
            deleted_counter += 1
        else:
            if type(date) != str or re.match('\d{4}-\d\d-\d\d', date) is None:
                df.drop(index=i + deleted_counter, inplace=True)
                i -= 1
                deleted_counter += 1
        i += 1


def create_fill_median_and_average_columns_in_dataframe(df: pd.DataFrame) -> None:
    """
    функция создаёт и заполняет столбцы отклонения от медианы и отклонения от среднего
    :param df: датафрейм
    :return: ничего не возвращает
    """
    median_value = df['value'].median()
    average_value = df['value'].mean()
    df['deviation_median'] = df['value'] - median_value
    df['deviation_average'] = df['value'] - average_value


def filter_dataframe_deviation_average(df: pd.DataFrame, deviation_average_value: float) -> pd.DataFrame:
    """
    функция возвращает отфильтрованный датафрейм, в котором у всех записей отклонение от
    среднего больше deviation_average_value
    :param df: датафрейм
    :param deviation_average_value: отклонение от среднего
    :return: возвращает отфильтрованный датафрейм
    """
    return df[df.deviation_average >= deviation_average_value]


def filter_dataframe_date(df: pd.DataFrame, date_start: pd.Timestamp, date_end: pd.Timestamp) -> pd.DataFrame:
    """
    функция возвращает отфильтрованный датафрейм, в котором находятся записи принадлежащий отрезку времени от
    date_start до date_end
    :param df: датафрейм
    :param date_start: начальная дата
    :param date_end: конечная дата
    :return: возвращает отфильтрованный датафрейм
    """
    return df[(date_start <= df.date) & (df.date <= date_end)]


def group_dataframe_months(df: pd.DataFrame) -> pd.DataFrame:
    """
    функция группирует датафрейм по месяцам
    :param df: датафрейм
    :return: возвращает сгруппированный датафрейм
    """
    return df.groupby(pd.Grouper(key='date', axis=0, freq='M')).mean()


def draw_exchange_rate(df: pd.DataFrame, draw: bool, title: str, x: str = 'date', y: str = 'value',
                       exp_graphic: bool = False, x_label: str = 'date', y_label: str = 'value') -> None:
    """
    функция рисует график по датафрейму
    :param df: датафрейм
    :param draw: параметр указывающий отрисовать график или нет
    :param title: название графика
    :param x: название столбца датафрейма, который лежит по оси x
    :param y: название столбца датафрейма, который лежит по оси y
    :param exp_graphic: параметр отвечает за то, отрисовывать график по оси y экспоненциально или нет
    :param x_label: название оси x
    :param y_label: название оси y
    :return: ничего не возвращает
    """
    plt.figure(figsize=(18, 5))
    plt.plot(df[x], df[y])
    if exp_graphic:
        plt.yscale('log')
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    if draw:
        plt.show()


def draw_exchange_rate_month(df: pd.DataFrame, month: int, year: int) -> None:
    """
    функция рисует 3 графика(просто значений, отклонений от медианы и отклонений от среднего) за выбранный месяц
    :param df: датафрейм
    :param month: месяц
    :param year: год
    :return: ничего не возвращает
    """
    date_start = pd.Timestamp(year, month, 1)
    date_end = pd.Timestamp(year, month, date_start.days_in_month)
    df_filtered = filter_dataframe_date(df, date_start, date_end)
    draw_exchange_rate(df_filtered, False, f'values to month {year}-{month:02d}', 'date', 'value')
    draw_exchange_rate(df_filtered, False, f'median to month {year}-{month:02d}', 'date', 'deviation_median')
    draw_exchange_rate(df_filtered, False, f'average to month {year}-{month:02d}', 'date', 'deviation_average')
    plt.show()


if __name__ == "__main__":
    dataset_df = read_csv_to_dataframe()
    create_fill_median_and_average_columns_in_dataframe(dataset_df)
    print('\n', dataset_df)
    df_filtered_average = filter_dataframe_deviation_average(dataset_df, 5000)
    print('\n', df_filtered_average)
    date_1 = pd.Timestamp(2022, 10, 11)
    date_2 = pd.Timestamp(2022, 10, 15)
    df_filtered_date = filter_dataframe_date(dataset_df, date_1, date_2)
    print('\n', df_filtered_date)
    df_grouped_month = group_dataframe_months(dataset_df)
    print('\n', df_grouped_month)
    draw_exchange_rate(dataset_df, True, 'ruble to dollar exchange rate(all time)', 'date', 'value', True)
    draw_exchange_rate_month(dataset_df, 9, 2022)
