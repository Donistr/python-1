import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox, QDesktopWidget, QMainWindow, QHBoxLayout,\
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

    def __init__(self):
        super().__init__()
        self.line_edit = None
        self.init_ui()

    def init_ui(self) -> None:
        self.resize(1000, 500)
        self.center()
        self.setWindowTitle('Работа с датасетами 24/7')
        v_box = QVBoxLayout()
        default_data_annotation_button = self.create_button(v_box, 'Создать файл-аннотацию исходного датасета', 700, 30)
        partition_data_two_files_button = self.create_button(v_box, 'Создать датасет, разделённый на файл с датами и'
                                                                    ' файл со значениями', 700, 30)
        partition_data_n_files_years_button = self.create_button(v_box, 'Создать датасет, разделённый на файлы по'
                                                                        ' годам', 700, 30)
        partition_data_n_files_weeks_button = self.create_button(v_box, 'Создать датасет, разделённый на файлы по'
                                                                        ' неделям', 700, 30)
        v_box.addSpacing(50)
        massage = QLabel(f'Дата, для которой нужно найти значение(в формате ГГГГ-ММ-ДД):', self)
        v_box.addWidget(massage)
        self.line_edit = QLineEdit(self)
        v_box.addWidget(self.line_edit)
        v_box.addSpacing(20)
        get_value_from_default_dataset_button = self.create_button(v_box, 'Найти в исходном датасете значение для '
                                                                       'выбранной даты', 700, 30)
        get_value_from_dataset_two_files_button = self.create_button(v_box, 'Найти в датасете, разделённом'
                                                                                     ' на файл с датами и файл со '
                                                                                     'значениями, значение для '
                                                                                     'выбранной даты', 700, 30)
        get_value_from_dataset_n_files_years_button = self.create_button(v_box, 'Найти в датасете,'
                                                                                         ' разделённом на файлы по '
                                                                                         'годам, значение для '
                                                                                         'выбранной даты', 700, 30)
        get_value_from_dataset_n_files_weeks_button = self.create_button(v_box, 'Найти в датасете, '
                                                                                         'разделённом на файлы по '
                                                                                         'неделям, значение для '
                                                                                         'выбранной даты', 700, 30)
        v_box.addStretch(1)
        h_box = QHBoxLayout()
        h_box.addLayout(v_box)
        h_box.addStretch(1)
        default_data_annotation_button.clicked.connect(self.create_annotation)
        partition_data_two_files_button.clicked.connect(self.partition_data_two_files)
        partition_data_n_files_years_button.clicked.connect(self.partition_data_n_files_years)
        partition_data_n_files_weeks_button.clicked.connect(self.partition_data_n_files_weeks)
        get_value_from_default_dataset_button.clicked.connect(self.get_value_from_default_data)
        get_value_from_dataset_two_files_button.clicked.connect(self.get_value_from_data_partitioned_two_files)
        get_value_from_dataset_n_files_years_button.clicked.connect(self.get_value_from_data_partitioned_n_files_years)
        get_value_from_dataset_n_files_weeks_button.clicked.connect(self.get_value_from_data_partitioned_n_files_weeks)
        central_widget = QWidget()
        central_widget.setLayout(h_box)
        self.setCentralWidget(central_widget)
        self.show()

    def closeEvent(self, event) -> None:
        reply = QMessageBox.question(self, 'Выход', 'Вы уверены, что хотите выйти?', QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def center(self) -> None:
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    @staticmethod
    def create_button(v_box: QVBoxLayout, name: str, width: int, height: int) -> QPushButton:
        button = QPushButton(name)
        button.setFixedSize(QSize(width, height))
        v_box.addWidget(button)
        return button

    def create_annotation(self) -> None:
        dataset_path = QFileDialog.getExistingDirectory(self, 'Выберите папку с исходным датасетом')
        file_name = 'data_file.csv'
        dataset_path = f'{dataset_path}/{file_name}'
        annotation_path = QFileDialog.getExistingDirectory(self, 'Выберите папку в которой будет создана аннотация')
        annotation_path = f'{annotation_path}/{file_name}'
        try:
            shutil.copy(dataset_path, annotation_path)
        except OSError as error:
            raise error

    def partition_data_two_files(self) -> None:
        dataset_path = QFileDialog.getExistingDirectory(self, 'Выберите папку с исходным датасетом')
        dataset_file_name = 'data_file.csv'
        dataset_path = f'{dataset_path}/{dataset_file_name}'
        res_file_path = QFileDialog.getExistingDirectory(self, 'Выберите папку в которой будет создан датасет '
                                                               'разделённый на 2 файла')
        date_file = f'{res_file_path}/X.csv'
        value_file = f'{res_file_path}/Y.csv'
        partition_data_two_files(dataset_path, date_file, value_file)

    def partition_data_n_files_years(self) -> None:
        dataset_path = QFileDialog.getExistingDirectory(self, 'Выберите папку с исходным датасетом')
        dataset_file_name = 'data_file.csv'
        dataset_path = f'{dataset_path}/{dataset_file_name}'
        res_file_path = QFileDialog.getExistingDirectory(self, 'Выберите папку в которой будет создан датасет '
                                                               'разделённый на n файлов по годам')
        partition_data_n_files_years_or_weeks(FunctionStatePartition.partition_years, res_file_path, dataset_path)

    def partition_data_n_files_weeks(self) -> None:
        dataset_path = QFileDialog.getExistingDirectory(self, 'Выберите папку с исходным датасетом')
        dataset_file_name = 'data_file.csv'
        dataset_path = f'{dataset_path}/{dataset_file_name}'
        res_file_path = QFileDialog.getExistingDirectory(self, 'Выберите папку в которой будет создан датасет '
                                                               'разделённый на n файлов по годам')
        partition_data_n_files_years_or_weeks(FunctionStatePartition.partition_weeks, res_file_path, dataset_path)

    @staticmethod
    def show_message(message: str) -> None:
        msg = QMessageBox()
        msg.setFixedSize(400, 300)
        msg.setText(message)
        msg.setWindowTitle('Информация')
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec()

    def get_value_from_default_data(self) -> None:
        str_date = self.line_edit.text()
        if re.match('\d{4}-\d\d-\d\d', str_date) is None:
            self.show_message(f'Неверно задана дата')
            return
        date = datetime.datetime.strptime(str_date, '%Y-%m-%d').date()
        file_path = QFileDialog.getExistingDirectory(self, 'Выберите папку в которой хранится исходный датасет')
        res = get_value_from_basic_or_year_or_week_file(date, FunctionStateGetValue.basic_file, file_path)
        if res is not None:
            self.show_message(f'Значение: {res}')
        else:
            self.show_message(f'Не удалось найти значение')

    def get_value_from_data_partitioned_two_files(self) -> None:
        str_date = self.line_edit.text()
        if re.match('\d{4}-\d\d-\d\d', str_date) is None:
            self.show_message(f'Неверно задана дата')
            return
        date = datetime.datetime.strptime(str_date, '%Y-%m-%d').date()
        file_path = QFileDialog.getExistingDirectory(self, 'Выберите папку в которой хранится датасет, '
                                                           'разделённый на 2 файла')
        date_file = f'{file_path}/X.csv'
        value_file = f'{file_path}/Y.csv'
        res = get_value_from_dates_only_and_values_only_files(date, date_file, value_file)
        if res is not None:
            self.show_message(f'Значение: {res}')
        else:
            self.show_message(f'Не удалось найти значение')

    def get_value_from_data_partitioned_n_files_years(self) -> None:
        str_date = self.line_edit.text()
        if re.match('\d{4}-\d\d-\d\d', str_date) is None:
            self.show_message(f'Неверно задана дата')
            return
        date = datetime.datetime.strptime(str_date, '%Y-%m-%d').date()
        file_path = QFileDialog.getExistingDirectory(self, 'Выберите папку в которой хранится датасет, состоящий '
                                                           'из n файлов, разделённых по годам')
        res = get_value_from_basic_or_year_or_week_file(date, FunctionStateGetValue.year_file, file_path)
        if res is not None:
            self.show_message(f'Значение: {res}')
        else:
            self.show_message(f'Не удалось найти значение')

    def get_value_from_data_partitioned_n_files_weeks(self) -> None:
        str_date = self.line_edit.text()
        if re.match('\d{4}-\d\d-\d\d', str_date) is None:
            self.show_message(f'Неверно задана дата')
            return
        date = datetime.datetime.strptime(str_date, '%Y-%m-%d').date()
        file_path = QFileDialog.getExistingDirectory(self, 'Выберите папку в которой хранится датасет, состоящий '
                                                           'из n файлов, разделённых по неделям')
        res = get_value_from_basic_or_year_or_week_file(date, FunctionStateGetValue.week_file, file_path)
        if res is not None:
            self.show_message(f'Значение: {res}')
        else:
            self.show_message(f'Не удалось найти значение')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    app.exec()
