import json
import os
import sys
import subprocess
from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QComboBox,
    QApplication,
    QListWidget,
    QMessageBox,
    QColorDialog,
    QGridLayout,
    QFileDialog,
    QDialog
)
from main import main
class MyQtModule(QWidget):
    def __init__(self):
        super().__init__()
        self.figures = []
        self.is_authenticated = False
        self.data_file = "users.txt"  # Файл для хранения логинов и паролей
        self.initUI()
        self.username = ''

    def initUI(self):
        self.setWindowTitle('Ввод конфигурации симуляции')
        self.vbox = QVBoxLayout()

        # Элементы для аутентификации
        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText("Введите имя пользователя")
        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("Введите пароль")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.register_button = QPushButton('Зарегистрироваться')
        self.login_button = QPushButton('Войти')

        # Добавляем элементы аутентификации в основной layout
        self.vbox.addWidget(self.username_input)
        self.vbox.addWidget(self.password_input)
        self.vbox.addWidget(self.register_button)
        self.vbox.addWidget(self.login_button)

        # Основной интерфейс (по умолчанию скрыт)
        self.main_interface_widget = QWidget()
        self.main_layout = QVBoxLayout()

        self.ruk_button = QPushButton('Руководство пользователя')
        self.ruk_button.clicked.connect(lambda file_path: subprocess.run(['notepad', 'README.txt']))
        # Кнопки для добавления и удаления фигур
        self.add_button = QPushButton('Добавить фигуру (+)')
        self.add_button.clicked.connect(self.add_figure)

        self.remove_button = QPushButton('Удалить фигуру (-)')
        self.remove_button.clicked.connect(self.remove_figure)

        self.save_button = QPushButton('Сохранить пресет')
        self.save_button.clicked.connect(self.save_preset)
        self.save_button.setEnabled(False)  # Disable until authenticated

        self.load_button = QPushButton('Загрузить пресет')
        self.load_button.clicked.connect(self.load_preset)
        self.load_button.setEnabled(False)  # Disable until authenticated

        self.shape_combo = QComboBox()
        self.shape_combo.addItems(['Тессеракт', 'Апекс'])

        self.coord_label = QLabel('Введите координаты центра:')
        self.grid_layout = QGridLayout()
        self.x_input = QLineEdit()
        self.y_input = QLineEdit()
        self.z_input = QLineEdit()
        self.w_input = QLineEdit()  # Добавляем W
        self.size_label = QLabel('Введите размер:')
        self.size_input = QLineEdit()

        # Заполняем грид
        self.grid_layout.addWidget(QLabel('X:'), 0, 0)
        self.grid_layout.addWidget(self.x_input, 0, 1)
        self.grid_layout.addWidget(QLabel('Y:'), 1, 0)
        self.grid_layout.addWidget(self.y_input, 1, 1)
        self.grid_layout.addWidget(QLabel('Z:'), 2, 0)
        self.grid_layout.addWidget(self.z_input, 2, 1)
        self.grid_layout.addWidget(QLabel('W:'), 3, 0)
        self.grid_layout.addWidget(self.w_input, 3, 1)
        self.grid_layout.addWidget(self.size_label, 4, 0)
        self.grid_layout.addWidget(self.size_input, 4, 1)

        # Кнопка выбора цвета
        self.color_button = QPushButton('Выбрать цвет')
        self.color_button.clicked.connect(self.choose_color)

        self.launch_button = QPushButton('Запустить программу')
        self.launch_button.clicked.connect(self.launch_program)

        # Список для отображения фигур
        self.figure_list = QListWidget()

        # Упорядочиваем элементы

        self.main_layout.addWidget(self.ruk_button)
        self.main_layout.addWidget(self.add_button)
        self.main_layout.addWidget(self.remove_button)
        self.main_layout.addWidget(self.save_button)
        self.main_layout.addWidget(self.load_button)
        self.main_layout.addWidget(self.shape_combo)
        self.main_layout.addWidget(self.coord_label)
        self.main_layout.addLayout(self.grid_layout)
        self.main_layout.addWidget(self.color_button)
        self.main_layout.addWidget(self.launch_button)
        self.main_layout.addWidget(self.figure_list)

        self.main_interface_widget.setLayout(self.main_layout)
        self.vbox.addWidget(self.main_interface_widget)

        # Устанавливаем основной интерфейс как скрытый по умолчанию
        self.main_interface_widget.setVisible(False)

        self.setLayout(self.vbox)

        # Подключаем кнопки для аутентификации
        self.register_button.clicked.connect(self.register)
        self.login_button.clicked.connect(self.login)

    def register(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if not username or not password:
            QMessageBox.warning(self, 'Ошибка', 'Введите имя пользователя и пароль.')
            return

        if self.user_exists(username):
            QMessageBox.warning(self, 'Ошибка', 'Пользователь с таким именем уже существует.')
            return

        with open(self.data_file, 'a') as f:
            f.write(f"{username}:{password}\n")

        os.makedirs(username, exist_ok=True)  # Создаем директорию с именем пользователя
        QMessageBox.information(self, 'Успех', 'Регистрация прошла успешно!')
        self.username_input.clear()
        self.password_input.clear()

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if self.check_credentials(username, password):
            self.is_authenticated = True
            self.username_input.clear()
            self.password_input.clear()
            self.show_main_interface()
            self.username = username
        else:
            QMessageBox.warning(self, 'Ошибка авторизации', 'Неверное имя пользователя или пароль.')

    def user_exists(self, username):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as f:
                for line in f:
                    if line.split(':')[0] == username:
                        return True
        return False

    def check_credentials(self, username, password):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as f:
                for line in f:
                    user, pwd = line.strip().split(':')
                    if user == username and pwd == password:
                        return True
        return False

    def show_main_interface(self):
        # Скрываем элементы аутентификации
        self.username_input.setVisible(False)
        self.password_input.setVisible(False)
        self.register_button.setVisible(False)
        self.login_button.setVisible(False)

        # Показываем элементы основного интерфейса
        self.main_interface_widget.setVisible(True)
        self.save_button.setEnabled(True)
        self.load_button.setEnabled(True)

    def add_figure(self):
        shape = self.shape_combo.currentText()
        x = self.x_input.text()
        y = self.y_input.text()
        z = self.z_input.text()
        w = self.w_input.text()
        size = self.size_input.text()

        if not (x and y and z and size):
            QMessageBox.warning(self, 'Input Error', 'Введите все координаты и размер.')
            return

        if not hasattr(self, 'selected_color') or self.selected_color is None:
            QMessageBox.warning(self, 'Input Error', 'Выберите цвет для фигуры.')
            return

        # Добавляем фигуру в список
        self.figures.append((shape, (x, y, z, w), size, self.selected_color.name()))
        self.figure_list.addItem(
            f"{shape}: Центр({x}, {y}, {z}, {w}), Размер: {size}, Цвет: {self.selected_color.name()}")

    def remove_figure(self):
        selected_item = self.figure_list.currentRow()
        if selected_item >= 0:
            del self.figures[selected_item]
            self.figure_list.takeItem(selected_item)
        else:
            QMessageBox.warning(self, 'Remove Error', 'Выберите фигуру для удаления.')

    def choose_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.selected_color = color
            self.color_button.setStyleSheet(f'background-color: {self.selected_color.name()}')

    def launch_program(self):
        if not self.figures:
            QMessageBox.warning(self, 'Input Error', 'Нет фигур для запуска программы.')
            return

        # Формируем массив строк с описанием фигур
        figure_descriptions = []
        for shape, coords, size, color in self.figures:
            description = f"Фигура: {shape}, Центр: ({coords[0]}, {coords[1]}, {coords[2]}), Размер: {size}, Цвет: {color}"
            coords_imp = []
            for i in range(len(coords)):
                coords_imp.append(int(coords[i]))
            color = color.lstrip('#')
            color = tuple(int(color[i:i + 2], 16) for i in (0, 2, 4))
            figure_descriptions.append([shape, coords_imp, size, color])

        # Передаем массив в функцию main
        main(figure_descriptions)  # Предполагается, что main принимает массив фигур

        # Информируем пользователя об успешном завершении
        QMessageBox.information(self, 'Success', 'Программа успешно запущена с фигурами!')

    def save_preset(self):
        dialog = FileNameDialog(self.username)
        if dialog.exec_() == QDialog.Accepted:
            filename = dialog.filename
            try:
                with open(filename, 'w') as f:
                    json.dump(self.figures, f, default=lambda x: x.__dict__)
                QMessageBox.information(self, 'Успех', 'Пресет успешно сохранен!')
            except Exception as e:
                QMessageBox.critical(self, 'Ошибка', f'Не удалось сохранить пресет: {str(e)}')

    def load_preset(self):
        dialog = FileListDialog(self.username, self)
        if dialog.exec_() == QDialog.Accepted:
            selected_file = dialog.load_selected_file()
            if selected_file:
                full_path = os.path.join(self.username, selected_file)
                try:
                    with open(full_path, 'r') as f:
                        self.figures = json.load(f)  # Загрузка фигур из JSON
                        self.figure_list.clear()
                        for shape, coords, size, color in self.figures:
                            self.figure_list.addItem(
                                f"{shape}: Центр({coords[0]}, {coords[1]}, {coords[2]}, {coords[3]}), Размер: {size}, Цвет: {color}")
                    QMessageBox.information(self, 'Успех', 'Пресет успешно загружен!')
                except Exception as e:
                    QMessageBox.critical(self, 'Ошибка', f'Не удалось загрузить пресет: {str(e)}')


class FileListDialog(QDialog):
    def __init__(self, directory, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Выбор файла")
        self.setGeometry(100, 100, 400, 300)

        self.layout = QVBoxLayout(self)

        self.file_list = QListWidget(self)
        self.layout.addWidget(self.file_list)

        self.load_button = QPushButton("Загрузить", self)
        self.load_button.clicked.connect(self.load_selected_file)
        self.layout.addWidget(self.load_button)

        self.populate_file_list(directory)

    def populate_file_list(self, directory):
        if os.path.exists(directory):
            for filename in os.listdir(directory):
                if filename.endswith('.json'):  # Добавляем только JSON файлы
                    self.file_list.addItem(filename)
        else:
            QMessageBox.critical(self, 'Ошибка', 'Указанная папка не существует.')

    def load_selected_file(self):
        selected_items = self.file_list.selectedItems()
        if selected_items:
            selected_file = selected_items[0].text()
            self.accept()  # Закрываем диалог
            return selected_file
        else:
            QMessageBox.warning(self, 'Предупреждение', 'Выберите файл для загрузки.')


class FileNameDialog(QDialog):
    def __init__(self, directory):
        super().__init__()
        self.directory = directory
        self.filename = None
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Сохранить пресет")

        layout = QVBoxLayout()

        self.label = QLabel("Введите имя файла (без расширения):")
        layout.addWidget(self.label)

        self.filename_input = QLineEdit(self)
        layout.addWidget(self.filename_input)

        self.submit_button = QPushButton("Сохранить", self)
        self.submit_button.clicked.connect(self.check_file)
        layout.addWidget(self.submit_button)

        self.setLayout(layout)

    def check_file(self):
        filename = self.filename_input.text().strip()
        full_path = os.path.join(self.directory, filename + ".json")

        if not filename:  # Проверка на пустое имя файла
            QMessageBox.warning(self, "Ошибка", "Имя файла не может быть пустым.")
            return

        if os.path.exists(full_path):
            QMessageBox.warning(self, "Ошибка", "Файл с таким именем уже существует.")
        else:
            self.filename = full_path
            self.accept()  # Закрыть диалог, если имя файла корректное

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyQtModule()
    ex.show()
    sys.exit(app.exec_())
