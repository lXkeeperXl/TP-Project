# ///////////////////////////////////////////////////////////////
#
# BY: WANDERSON M.PIMENTA
# PROJECT MADE WITH: Qt Designer and PySide6
# V: 1.0.0
#
# This project can be used freely for all uses, as long as they maintain the
# respective credits only in the Python scripts, any information in the visual
# interface (GUI) can be modified without any implication.
#
# There are limitations on Qt licenses if you want to use your products
# commercially, I recommend reading them on the official website:
# https://doc.qt.io/qtforpython/licenses.html
#
# ///////////////////////////////////////////////////////////////

import json
import uuid

# MAIN FILE
# ///////////////////////////////////////////////////////////////
from main import *

# WITH ACCESS TO MAIN WINDOW WIDGETS
# ///////////////////////////////////////////////////////////////
class AppFunctions(MainWindow):
    def setThemeHack(self):
        Settings.BTN_LEFT_BOX_COLOR = "background-color: #495474;"
        Settings.BTN_RIGHT_BOX_COLOR = "background-color: #495474;"
        Settings.MENU_SELECTED_STYLESHEET = MENU_SELECTED_STYLESHEET = """
        border-left: 22px solid qlineargradient(spread:pad, x1:0.034, y1:0, x2:0.216, y2:0, stop:0.499 rgba(255, 121, 198, 255), stop:0.5 rgba(85, 170, 255, 0));
        background-color: #566388;
        """

        # SET MANUAL STYLES
        self.ui.lineEdit.setStyleSheet("background-color: #6272a4;")
        self.ui.pushButton.setStyleSheet("background-color: #6272a4;")
        self.ui.plainTextEdit.setStyleSheet("background-color: #6272a4;")
        self.ui.tableWidget.setStyleSheet("QScrollBar:vertical { background: #6272a4; } QScrollBar:horizontal { background: #6272a4; }")
        self.ui.scrollArea.setStyleSheet("QScrollBar:vertical { background: #6272a4; } QScrollBar:horizontal { background: #6272a4; }")
        self.ui.comboBox.setStyleSheet("background-color: #6272a4;")
        self.ui.horizontalScrollBar.setStyleSheet("background-color: #6272a4;")
        self.ui.verticalScrollBar.setStyleSheet("background-color: #6272a4;")
        self.ui.commandLinkButton.setStyleSheet("color: #ff79c6;")

    TASKS_FILE = "tasks.json"  # Имя файла для хранения задач

    def load_tasks_from_file(self, filepath=TASKS_FILE):
        """Загружает задачи из JSON файла."""
        try:
            with open(filepath, "r") as f:
                tasks = json.load(f)
        except FileNotFoundError:
            tasks = []  # Если файл не найден, возвращаем пустой список
        return tasks

    def save_tasks_to_file(self, filepath=TASKS_FILE, tasks=[]):
        """Сохраняет задачи в JSON файл."""
        with open(filepath, "w") as f:
            json.dump(tasks, f, indent=4)  # indent=4 для форматирования JSON

    def add_task(self, task_text, tags=[]):
        """Добавляет новую задачу с указанными тегами."""
        tasks = self.load_tasks_from_file()
        new_task = {
            "id": str(uuid.uuid4()),  # Генерируем уникальный ID для задачи
            "task": task_text,
            "tags": tags
        }
        tasks.append(new_task)
        self.save_tasks_to_file(tasks=tasks)

    def get_task_by_id(self, task_id):
        """Возвращает задачу по её ID."""
        tasks = self.load_tasks_from_file()
        for task in tasks:
            if task["id"] == task_id:
                return task
        return None  # Если задача не найдена

    def get_tasks_by_tag(self, tag):
        """Возвращает список задач, содержащих указанный тег."""
        tasks = self.load_tasks_from_file()
        matching_tasks = []
        for task in tasks:
            if tag in task["tags"]:
                matching_tasks.append(task)
        return matching_tasks

    def add_tag_to_task(self, task_id, tag):
        """Добавляет тег к задаче."""
        tasks = self.load_tasks_from_file()
        for task in tasks:
            if task["id"] == task_id:
                if tag not in task["tags"]:
                    task["tags"].append(tag)
                    self.save_tasks_to_file(tasks=tasks)
                return

    def remove_tag_from_task(self, task_id, tag):
        """Удаляет тег из задачи."""
        tasks = self.load_tasks_from_file()
        for task in tasks:
            if task["id"] == task_id:
                if tag in task["tags"]:
                    task["tags"].remove(tag)
                    self.save_tasks_to_file(tasks=tasks)
                return

    def edit_task_text(self, task_id, new_text):
        """Редактирует текст задачи."""
        tasks = self.load_tasks_from_file()
        for task in tasks:
            if task["id"] == task_id:
                task["task"] = new_text
                self.save_tasks_to_file(tasks=tasks)
                return

    def delete_task(self, task_id):
        """Удаляет задачу."""
        tasks = self.load_tasks_from_file()
        for i, task in enumerate(tasks):
            if task["id"] == task_id:
                del tasks[i]
                self.save_tasks_to_file(tasks=tasks)
                return