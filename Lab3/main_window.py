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
import enum


class FunctionStateForGUI(enum.Enum):
    default_dataset = 1
    dates_and_values_dataset = 2
    years_dataset = 3
    weeks_dataset = 4


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
        self.setFixedSize(1120, 215)
        self.center()
        self.setWindowTitle('Работа с датасетами 24/7')
        v_box_1 = QVBoxLayout()
        default_data_copy_button = self.create_button(v_box_1, 'Создать копию исходного датасета', 273, 30)
        partition_data_two_files_button = self.create_button(v_box_1, 'Создать датасет, разделённый '
                                                                      'на 2 файла', 273, 30)
        partition_data_n_files_years_button = self.create_button(v_box_1, 'Создать датасет, разделённый '
                                                                          'по годам', 273, 30)
        partition_data_n_files_weeks_button = self.create_button(v_box_1, 'Создать датасет, разделённый '
                                                                          'по неделям', 273, 30)
        v_box_1.addSpacing(20)
        get_value_from_default_dataset_button = self.create_button(v_box_1, 'Найти в исходном датасете', 273, 30)
        v_box_1.addStretch(1)
        h_box = QHBoxLayout()
        h_box.addLayout(v_box_1)
        h_box.addStretch(1)
        v_box_2 = QVBoxLayout()
        set_path_for_default_dataset_button = self.create_button(v_box_2, 'Путь к исходному датасету', 273, 30)
        set_path_for_dataset_two_files_button = self.create_button(v_box_2, 'Путь к датасету, разделённому '
                                                                            'на 2 файла', 273, 30)
        set_path_for_dataset_n_files_years_button = self.create_button(v_box_2, 'Указать путь к датасету разделённому '
                                                                                'по годам', 273, 30)
        set_path_for_dataset_n_files_weeks_button = self.create_button(v_box_2, 'Указать путь к датасету разделённому '
                                                                                'по неделям', 273, 30)
        v_box_2.addSpacing(20)
        get_value_from_dataset_two_files_button = self.create_button(v_box_2, 'Найти в датасете, разделённом на '
                                                                              '2 файла', 273, 30)
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
        v_box_3.addWidget(QLabel(f'Путь к датасету, разделённому на 2 файла:'))
        v_box_3.addWidget(self.dataset_two_files_path)
        v_box_3.addWidget(QLabel(f'Путь к датасету разделённому по годам:'))
        v_box_3.addWidget(self.dataset_n_files_years_path)
        v_box_3.addWidget(QLabel(f'Путь к датасету разделённому по неделям:'))
        v_box_3.addWidget(self.dataset_n_files_weeks_path)
        v_box_3.addSpacing(12)
        get_value_from_dataset_n_files_years_button = self.create_button(v_box_3, 'Найти в датасете, разделённом '
                                                                                  'по годам', 273, 30)
        v_box_3.addStretch(1)
        h_box.addLayout(v_box_3)
        v_box_4 = QVBoxLayout()
        v_box_4.addSpacing(80)
        massage_1 = QLabel(f'Дата, для которой нужно найти значение', self)
        massage_2 = QLabel(f'(в формате ГГГГ-ММ-ДД):', self)
        v_box_4.addWidget(massage_1)
        v_box_4.addWidget(massage_2)
        self.line_edit = QLineEdit(self)
        v_box_4.addWidget(self.line_edit)
        v_box_4.addSpacing(20)
        get_value_from_dataset_n_files_weeks_button = self.create_button(v_box_4, 'Найти в датасете, разделённом '
                                                                                  'по неделям', 273, 30)
        v_box_4.addStretch(1)
        h_box.addLayout(v_box_4)
        h_box.addStretch(1)
        default_data_copy_button.clicked.connect(self.copy_default_dataset)
        partition_data_two_files_button.clicked.connect(lambda: self.process_default_dataset(FunctionStateForGUI.dates_and_values_dataset, 'Выберите '
                                                                                                                                           'папку в '
                                                                                                                                           'которой будет'
                                                                                                                                           ' создан датасет'
                                                                                                                                           ' разделённый на'
                                                                                                                                           ' 2 файла'))
        partition_data_n_files_years_button.clicked.connect(lambda: self.process_default_dataset(FunctionStateForGUI.years_dataset, 'Выберите папку '
                                                                                                                                    'в которой будет'
                                                                                                                                    ' создан датасет'
                                                                                                                                    ' разделённый '
                                                                                                                                    'на n файлов '
                                                                                                                                    'по годам'))
        partition_data_n_files_weeks_button.clicked.connect(lambda: self.process_default_dataset(FunctionStateForGUI.weeks_dataset, 'Выберите папку '
                                                                                                                                    'в которой будет'
                                                                                                                                    ' создан датасет'
                                                                                                                                    ' разделённый на'
                                                                                                                                    ' n файлов по'
                                                                                                                                    ' неделям'))
        get_value_from_default_dataset_button.clicked.connect(lambda: self.get_value_from_dataset(FunctionStateForGUI.default_dataset))
        get_value_from_dataset_two_files_button.clicked.connect(lambda: self.get_value_from_dataset(FunctionStateForGUI.dates_and_values_dataset))
        get_value_from_dataset_n_files_years_button.clicked.connect(lambda: self.get_value_from_dataset(FunctionStateForGUI.years_dataset))
        get_value_from_dataset_n_files_weeks_button.clicked.connect(lambda: self.get_value_from_dataset(FunctionStateForGUI.weeks_dataset))
        set_path_for_default_dataset_button.clicked.connect(lambda: self.get_and_set_path_for_dataset('Выберите папку '
                                                                                                      'с исходным '
                                                                                                      'датасетом',
                                                                                                      self.default_dataset_path))
        set_path_for_dataset_two_files_button.clicked.connect(lambda: self.get_and_set_path_for_dataset('Выберите '
                                                                                                        'папку с '
                                                                                                        'датасетом, '
                                                                                                        'разделённым '
                                                                                                        'на файлы с '
                                                                                                        'датами и '
                                                                                                        'значениями',
                                                                                                        self.dataset_two_files_path))
        set_path_for_dataset_n_files_years_button.clicked.connect(lambda: self.get_and_set_path_for_dataset('Выберите '
                                                                                                            'папку с '
                                                                                                            'датасетом, '
                                                                                                            'разделённым'
                                                                                                            ' по годам', self.dataset_n_files_years_path))
        set_path_for_dataset_n_files_weeks_button.clicked.connect(lambda: self.get_and_set_path_for_dataset('Выберите '
                                                                                                            'папку с '
                                                                                                            'датасетом '
                                                                                                            'разделённым'
                                                                                                            ' по неделям', self.dataset_n_files_weeks_path))
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

    def get_and_set_path_for_dataset(self, text: str, label: QLabel) -> None:
        """
        функция предоставляет пользователю возможность выбрать папку, в которой датасет, путь к папке записывается
        в label, если пользователь не стал указывать путь и отменил действие, то остаётся старое значение
        :param text: текст который не даёт пользователю забыть путь к чему он указывает
        :param label: лейбл в котором хранится путь к датасету
        :return: ничего не возвращает
        """
        dataset_path = QFileDialog.getExistingDirectory(self, text)
        if dataset_path != '':
            label.setText(dataset_path)

    def copy_default_dataset(self) -> None:
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

    def process_default_dataset(self, function_type: FunctionStateForGUI, text: str) -> None:
        """
        функция обрабатывает исходный датасет: либо разделяется на 2 файла, либо на n файлов по годам, либо на
        n файлов по неделям
        :param function_type: параметр, который контролирует какой функцией будет обрабатываться датасет
        :param text: текст который не даёт пользователю забыть путь к чему он указывает
        :return: ничего не возвращает
        """
        try:
            file_name = 'data_file.csv'
            dataset_path = f'{self.default_dataset_path.text()}/{file_name}'
            res_file_path = QFileDialog.getExistingDirectory(self, text)
            if function_type == FunctionStateForGUI.dates_and_values_dataset:
                date_file = f'{res_file_path}/X.csv'
                value_file = f'{res_file_path}/Y.csv'
                partition_data_two_files(dataset_path, date_file, value_file)
                self.dataset_two_files_path.setText(res_file_path)
            elif function_type == FunctionStateForGUI.years_dataset:
                partition_data_n_files_years_or_weeks(FunctionStatePartition.partition_years, res_file_path,
                                                      dataset_path)
                self.dataset_n_files_years_path.setText(res_file_path)
            elif function_type == FunctionStateForGUI.weeks_dataset:
                partition_data_n_files_years_or_weeks(FunctionStatePartition.partition_weeks, res_file_path,
                                                      dataset_path)
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

    def get_value_from_dataset(self, dataset_type: FunctionStateForGUI) -> None:
        """
        функция ищет значение для выбранной пользователем даты
        :param dataset_type: параметр, который контролирует тип файла в котором будет искаться информация
        :return: ничего не возвращает
        """
        try:
            str_date = self.line_edit.text()
            if re.match('\d{4}-\d\d-\d\d', str_date) is None:
                self.show_message(f'Неверно задана дата')
                return
            date = datetime.datetime.strptime(str_date, '%Y-%m-%d').date()
            res = None
            if dataset_type == FunctionStateForGUI.default_dataset:
                file_path = self.default_dataset_path.text()
                res = get_value_from_basic_or_year_or_week_file(date, FunctionStateGetValue.basic_file, file_path)
            elif dataset_type == FunctionStateForGUI.dates_and_values_dataset:
                file_path = self.dataset_two_files_path.text()
                date_file = f'{file_path}/X.csv'
                value_file = f'{file_path}/Y.csv'
                res = get_value_from_dates_only_and_values_only_files(date, date_file, value_file)
            elif dataset_type == FunctionStateForGUI.years_dataset:
                file_path = self.dataset_n_files_years_path.text()
                res = get_value_from_basic_or_year_or_week_file(date, FunctionStateGetValue.year_file, file_path)
            elif dataset_type == FunctionStateForGUI.weeks_dataset:
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
