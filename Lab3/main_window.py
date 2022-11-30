import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox, QDesktopWidget, QMainWindow, QHBoxLayout, \
    QVBoxLayout, QLabel, QFileDialog, QLineEdit
from PyQt5.QtCore import QSize
import shutil
import datetime
import re
from t_1 import partition_data_two_files
from t_2_3 import partition_data_n_files_years_or_weeks, FunctionStatePartition
from t_4 import FunctionStateGetValue, get_value_from_basic_or_year_or_week_file, \
    get_value_from_dates_only_and_values_only_files


class MainWindow(QMainWindow):
    """
    класс, реализующий графический интерфейс для работы с функциями второй лабораторной
    """

    def __init__(self):
        super().__init__()
        self.line_edit = None
        self.default_dataset_path = None
        self.dataset_two_files_path = None
        self.dataset_n_files_years_path = None
        self.dataset_n_files_weeks_path = None
        self.init_ui()

    def init_ui(self) -> None:
        """
        функция инициализирует графический интерфейс
        :return: ничего не возвращает
        """
        self.setFixedSize(1350, 500)
        self.center()
        self.setWindowTitle('Работа с датасетами 24/7')
        v_box_1 = QVBoxLayout()
        default_data_annotation_button = self.create_button(v_box_1, 'Создать файл-аннотацию исходного '
                                                                     'датасета', 550, 30)
        partition_data_two_files_button = self.create_button(v_box_1, 'Создать датасет, разделённый на файл с датами и '
                                                                      'файл со значениями', 550, 30)
        partition_data_n_files_years_button = self.create_button(v_box_1, 'Создать датасет, разделённый на файлы по'
                                                                          ' годам', 550, 30)
        partition_data_n_files_weeks_button = self.create_button(v_box_1, 'Создать датасет, разделённый на файлы по'
                                                                          ' неделям', 550, 30)
        v_box_1.addSpacing(50)
        massage = QLabel(f'Дата, для которой нужно найти значение(в формате ГГГГ-ММ-ДД):', self)
        v_box_1.addWidget(massage)
        self.line_edit = QLineEdit(self)
        v_box_1.addWidget(self.line_edit)
        v_box_1.addSpacing(20)
        get_value_from_default_dataset_button = self.create_button(v_box_1, 'Найти в исходном датасете значение для '
                                                                            'выбранной даты', 550, 30)
        get_value_from_dataset_two_files_button = self.create_button(v_box_1, 'Найти в датасете, разделённом'
                                                                              ' на файл с датами и файл со '
                                                                              'значениями, значение для '
                                                                              'выбранной даты', 550, 30)
        get_value_from_dataset_n_files_years_button = self.create_button(v_box_1, 'Найти в датасете,'
                                                                                  ' разделённом на файлы по '
                                                                                  'годам, значение для '
                                                                                  'выбранной даты', 550, 30)
        get_value_from_dataset_n_files_weeks_button = self.create_button(v_box_1, 'Найти в датасете, '
                                                                                  'разделённом на файлы по '
                                                                                  'неделям, значение для '
                                                                                  'выбранной даты', 550, 30)
        v_box_1.addStretch(1)
        h_box = QHBoxLayout()
        h_box.addLayout(v_box_1)
        h_box.addStretch(1)
        v_box_2 = QVBoxLayout()
        set_path_for_default_dataset_button = self.create_button(v_box_2, 'Указать путь к исходному датасету', 400, 30)
        v_box_2.addSpacing(259)
        set_path_for_dataset_two_files_button = self.create_button(v_box_2, 'Указать путь к датасету, разделённому на '
                                                                            'файлы с датами и значениями', 400, 30)
        set_path_for_dataset_n_files_years_button = self.create_button(v_box_2, 'Указать путь к датасету разделённому '
                                                                                'по годам', 400, 30)
        set_path_for_dataset_n_files_weeks_button = self.create_button(v_box_2, 'Указать путь к датасету разделённому '
                                                                                'по неделям', 400, 30)
        v_box_2.addStretch(1)
        h_box.addLayout(v_box_2)
        h_box.addStretch(1)
        v_box_3 = QVBoxLayout()
        self.default_dataset_path = QLabel()
        self.dataset_two_files_path = QLabel()
        self.dataset_n_files_years_path = QLabel()
        self.dataset_n_files_weeks_path = QLabel()
        v_box_3.addWidget(QLabel(f'Путь к исходному датасету:'))
        v_box_3.addWidget(self.default_dataset_path)
        v_box_3.addSpacing(256)
        v_box_3.addWidget(QLabel(f'Путь к датасету, разделённому на файлы с датами и значениями:'))
        v_box_3.addWidget(self.dataset_two_files_path)
        v_box_3.addWidget(QLabel(f'Путь к датасету разделённому по годам:'))
        v_box_3.addWidget(self.dataset_n_files_years_path)
        v_box_3.addWidget(QLabel(f'Путь к датасету разделённому по неделям:'))
        v_box_3.addWidget(self.dataset_n_files_weeks_path)
        v_box_3.addStretch(1)
        h_box.addLayout(v_box_3)
        h_box.addStretch(1)
        default_data_annotation_button.clicked.connect(self.create_annotation)
        partition_data_two_files_button.clicked.connect(self.partition_data_two_files)
        partition_data_n_files_years_button.clicked.connect(self.partition_data_n_files_years)
        partition_data_n_files_weeks_button.clicked.connect(self.partition_data_n_files_weeks)
        get_value_from_default_dataset_button.clicked.connect(self.get_value_from_default_data)
        get_value_from_dataset_two_files_button.clicked.connect(self.get_value_from_data_partitioned_two_files)
        get_value_from_dataset_n_files_years_button.clicked.connect(self.get_value_from_data_partitioned_n_files_years)
        get_value_from_dataset_n_files_weeks_button.clicked.connect(self.get_value_from_data_partitioned_n_files_weeks)
        set_path_for_default_dataset_button.clicked.connect(self.get_and_set_path_for_default_dataset)
        set_path_for_dataset_two_files_button.clicked.connect(self.get_and_set_path_for_dataset_two_files)
        set_path_for_dataset_n_files_years_button.clicked.connect(self.get_and_set_path_for_dataset_n_files_years)
        set_path_for_dataset_n_files_weeks_button.clicked.connect(self.get_and_set_path_for_dataset_n_files_weeks)
        central_widget = QWidget()
        central_widget.setLayout(h_box)
        self.setCentralWidget(central_widget)
        self.show()

    def closeEvent(self, event) -> None:
        """
        функция спрашивает пользователь действительно ли он хочет выйти, когда он нажал на крестик
        :return: ничего не возвращает
        """
        reply = QMessageBox.question(self, 'Выход', 'Вы уверены, что хотите выйти?', QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def center(self) -> None:
        """
        функция центрирует окно приложения на мониторе
        :return: ничего не возвращает
        """
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    @staticmethod
    def create_button(v_box: QVBoxLayout, name: str, width: int, height: int) -> QPushButton:
        """
        функция создаёт кнопку
        :param v_box: v-box в который добавится кнопка
        :param name: текст кнопки
        :param width: ширина кнопки
        :param height: высота кнопки
        :return: возвращает кнопку
        """
        button = QPushButton(name)
        button.setFixedSize(QSize(width, height))
        v_box.addWidget(button)
        return button

    def get_and_set_path_for_default_dataset(self) -> None:
        """
        функция предоставляет пользователю возможность выбрать папку, в которой хранится исходный датасет, путь
        к папке записывается в self.default_dataset_path, если пользователь не стал указывать путь и
        отменил действие, то остаётся старое значение
        :return: ничего не возвращает
        """
        dataset_path = QFileDialog.getExistingDirectory(self, 'Выберите папку с исходным датасетом')
        if dataset_path != '':
            self.default_dataset_path.setText(dataset_path)

    def get_and_set_path_for_dataset_two_files(self) -> None:
        """
        функция предоставляет пользователю возможность выбрать папку, в которой хранится датасет из двух файлов, путь
        к папке записывается в self.dataset_two_files_path, если пользователь не стал указывать путь и
        отменил действие, то остаётся старое значение
        :return: ничего не возвращает
        """
        dataset_path = QFileDialog.getExistingDirectory(self, 'Выберите папку с датасетом, разделённым на файлы с '
                                                              'датами и значениями')
        if dataset_path != '':
            self.dataset_two_files_path.setText(dataset_path)

    def get_and_set_path_for_dataset_n_files_years(self) -> None:
        """
        функция предоставляет пользователю возможность выбрать папку, в которой хранится датасет из n файлов,
        разделённых по годам, путь к папке записывается в self.dataset_n_files_years_path, если пользователь не стал
        указывать путь и отменил действие, то остаётся старое значение
        :return: ничего не возвращает
        """
        dataset_path = QFileDialog.getExistingDirectory(self, 'Выберите папку с датасетом, разделённым по годам')
        if dataset_path != '':
            self.dataset_n_files_years_path.setText(dataset_path)

    def get_and_set_path_for_dataset_n_files_weeks(self) -> None:
        """
        функция предоставляет пользователю возможность выбрать папку, в которой хранится датасет из n файлов,
        разделённых по неделям, путь к папке записывается в self.dataset_n_files_weeks_path, если пользователь не стал
        указывать путь и отменил действие, то остаётся старое значение
        :return: ничего не возвращает
        """
        dataset_path = QFileDialog.getExistingDirectory(self, 'Выберите папку с датасетом разделённым по неделям')
        if dataset_path != '':
            self.dataset_n_files_weeks_path.setText(dataset_path)

    def create_annotation(self) -> None:
        """
        функция создаёт аннотацию исходного датасета(пользователь задаёт путь)
        :return: ничего не возвращает
        """
        try:
            file_name = 'data_file.csv'
            dataset_path = f'{self.default_dataset_path.text()}/{file_name}'
            annotation_path = QFileDialog.getExistingDirectory(self, 'Выберите папку в которой будет создана аннотация')
            annotation_path = f'{annotation_path}/{file_name}'
            shutil.copy(dataset_path, annotation_path)
            self.show_message(f'Ура, всё получилось!')
        except OSError as error:
            self.show_message(f'Ой, что-то пошло не так! (Проверьте, указан ли путь к датасету)\nОшибка:{error}')

    def partition_data_two_files(self) -> None:
        """
        функция разделяет исходный датасет(пользователь задаёт путь) на два файла(пользователь задаёт путь)
        :return: ничего не возвращает
        """
        try:
            file_name = 'data_file.csv'
            dataset_path = f'{self.default_dataset_path.text()}/{file_name}'
            res_file_path = QFileDialog.getExistingDirectory(self, 'Выберите папку в которой будет создан датасет '
                                                                   'разделённый на 2 файла')
            date_file = f'{res_file_path}/X.csv'
            value_file = f'{res_file_path}/Y.csv'
            partition_data_two_files(dataset_path, date_file, value_file)
            self.dataset_two_files_path.setText(res_file_path)
            self.show_message(f'Ура, всё получилось!')
        except OSError as error:
            self.show_message(f'Ой, что-то пошло не так! (Проверьте, указан ли путь к датасету)\nОшибка:{error}')

    def partition_data_n_files_years(self) -> None:
        """
        функция разделяет исходный датасет(пользователь задаёт путь) на n файлов по годам(пользователь задаёт путь)
        :return: ничего не возвращает
        """
        try:
            file_name = 'data_file.csv'
            dataset_path = f'{self.default_dataset_path.text()}/{file_name}'
            res_file_path = QFileDialog.getExistingDirectory(self, 'Выберите папку в которой будет создан датасет '
                                                                   'разделённый на n файлов по годам')
            partition_data_n_files_years_or_weeks(FunctionStatePartition.partition_years, res_file_path, dataset_path)
            self.dataset_n_files_years_path.setText(res_file_path)
            self.show_message(f'Ура, всё получилось!')
        except OSError as error:
            self.show_message(f'Ой, что-то пошло не так! (Проверьте, указан ли путь к датасету)\nОшибка:{error}')

    def partition_data_n_files_weeks(self) -> None:
        """
        функция разделяет исходный датасет(пользователь задаёт путь) на n файлов по неделям(пользователь задаёт путь)
        :return: ничего не возвращает
        """
        try:
            file_name = 'data_file.csv'
            dataset_path = f'{self.default_dataset_path.text()}/{file_name}'
            res_file_path = QFileDialog.getExistingDirectory(self, 'Выберите папку в которой будет создан датасет '
                                                                   'разделённый на n файлов по неделям')
            partition_data_n_files_years_or_weeks(FunctionStatePartition.partition_weeks, res_file_path, dataset_path)
            self.dataset_n_files_weeks_path.setText(res_file_path)
            self.show_message(f'Ура, всё получилось!')
        except OSError as error:
            self.show_message(f'Ой, что-то пошло не так! (Проверьте, указан ли путь к датасету)\nОшибка:{error}')

    @staticmethod
    def show_message(message: str) -> None:
        """
        функция показывает пользователю окно с текстом
        :param message: отображаемый в окне текст
        :return: ничего не возвращает
        """
        msg = QMessageBox()
        msg.setText(message)
        msg.setWindowTitle('Информация')
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec()

    def get_value_from_default_data(self) -> None:
        """
        функция ищет значение для даты(пользователь задаёт дату) в исходном датасете(пользователь задаёт путь)
        :return: ничего не возвращает
        """
        try:
            str_date = self.line_edit.text()
            if re.match('\d{4}-\d\d-\d\d', str_date) is None:
                self.show_message(f'Неверно задана дата')
                return
            date = datetime.datetime.strptime(str_date, '%Y-%m-%d').date()
            file_path = self.default_dataset_path.text()
            res = get_value_from_basic_or_year_or_week_file(date, FunctionStateGetValue.basic_file, file_path)
            if res is not None:
                self.show_message(f'Значение: {res}')
            else:
                self.show_message(f'Не удалось найти значение')
        except OSError as error:
            self.show_message(f'Ой, что-то пошло не так! (Проверьте, указан ли путь к датасету)\nОшибка:{error}')

    def get_value_from_data_partitioned_two_files(self) -> None:
        """
        функция ищет значение для даты(пользователь задаёт дату) в датасете из двух файлов(пользователь задаёт путь)
        :return: ничего не возвращает
        """
        try:
            str_date = self.line_edit.text()
            if re.match('\d{4}-\d\d-\d\d', str_date) is None:
                self.show_message(f'Неверно задана дата')
                return
            date = datetime.datetime.strptime(str_date, '%Y-%m-%d').date()
            file_path = self.dataset_two_files_path.text()
            date_file = f'{file_path}/X.csv'
            value_file = f'{file_path}/Y.csv'
            res = get_value_from_dates_only_and_values_only_files(date, date_file, value_file)
            if res is not None:
                self.show_message(f'Значение: {res}')
            else:
                self.show_message(f'Не удалось найти значение')
        except OSError as error:
            self.show_message(f'Ой, что-то пошло не так! (Проверьте, указан ли путь к датасету)\nОшибка:{error}')

    def get_value_from_data_partitioned_n_files_years(self) -> None:
        """
        функция ищет значение для даты(пользователь задаёт дату) в датасете из n файлов по
        годам(пользователь задаёт путь)
        :return: ничего не возвращает
        """
        try:
            str_date = self.line_edit.text()
            if re.match('\d{4}-\d\d-\d\d', str_date) is None:
                self.show_message(f'Неверно задана дата')
                return
            date = datetime.datetime.strptime(str_date, '%Y-%m-%d').date()
            file_path = self.dataset_n_files_years_path.text()
            res = get_value_from_basic_or_year_or_week_file(date, FunctionStateGetValue.year_file, file_path)
            if res is not None:
                self.show_message(f'Значение: {res}')
            else:
                self.show_message(f'Не удалось найти значение')
        except OSError as error:
            self.show_message(f'Ой, что-то пошло не так! (Проверьте, указан ли путь к датасету)\nОшибка:{error}')

    def get_value_from_data_partitioned_n_files_weeks(self) -> None:
        """
        функция ищет значение для даты(пользователь задаёт дату) в датасете из n файлов по
        неделям(пользователь задаёт путь)
        :return: ничего не возвращает
        """
        try:
            str_date = self.line_edit.text()
            if re.match('\d{4}-\d\d-\d\d', str_date) is None:
                self.show_message(f'Неверно задана дата')
                return
            date = datetime.datetime.strptime(str_date, '%Y-%m-%d').date()
            file_path = self.dataset_n_files_weeks_path.text()
            res = get_value_from_basic_or_year_or_week_file(date, FunctionStateGetValue.week_file, file_path)
            if res is not None:
                self.show_message(f'Значение: {res}')
            else:
                self.show_message(f'Не удалось найти значение')
        except OSError as error:
            self.show_message(f'Ой, что-то пошло не так! (Проверьте, указан ли путь к датасету)\nОшибка:{error}')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    app.exec()
