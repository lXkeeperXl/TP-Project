import json
import uuid
import datetime
from plyer import notification

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

    def add_notification_to_task(self, task_id, notification_datetime, message=""):
        """Добавляет уведомление к задаче."""
        tasks = self.load_tasks_from_file()
        for task in tasks:
            if task["id"] == task_id:
                if "notifications" not in task:
                    task["notifications"] = []
                new_notification = {
                    "id": str(uuid.uuid4()),
                    "datetime": notification_datetime,
                    "message": message,
                    "sent": False
                }
                task["notifications"].append(new_notification)
                self.save_tasks_to_file(tasks=tasks)
                return

    def get_notifications_for_task(self, task_id):
        """Возвращает список уведомлений для задачи."""
        tasks = self.load_tasks_from_file()
        for task in tasks:
            if task["id"] == task_id:
                return task.get("notifications", [])
        return []

    def get_unsent_notifications(self):
        """Возвращает список всех неотправленных уведомлений."""
        tasks = self.load_tasks_from_file()
        unsent_notifications = []
        for task in tasks:
            if "notifications" in task:
                for notification in task["notifications"]:
                    if not notification["sent"]:
                        unsent_notifications.append(notification)
        return unsent_notifications

    def mark_notification_as_sent(self, notification_id):
        """Помечает уведомление как отправленное."""
        tasks = self.load_tasks_from_file()
        for task in tasks:
            if "notifications" in task:
                for notification in task["notifications"]:
                    if notification["id"] == notification_id:
                        notification["sent"] = True
                        self.save_tasks_to_file(tasks=tasks)
                        return

    def remove_notification(self, notification_id):
        """Удаляет уведомление."""
        tasks = self.load_tasks_from_file()
        for task in tasks:
            if "notifications" in task:
                for i, notification in enumerate(task["notifications"]):
                    if notification["id"] == notification_id:
                        del task["notifications"][i]
                        self.save_tasks_to_file(tasks=tasks)
                        return

    def check_and_send_notifications(self):
        """Проверяет и отправляет уведомления."""
        unsent_notifications = self.get_unsent_notifications()
        now = datetime.datetime.now()
        for notification_data in unsent_notifications:
            notification_datetime_str = notification_data["datetime"]
            notification_datetime = datetime.datetime.strptime(notification_datetime_str, "%Y-%m-%d %H:%M")
            if now >= notification_datetime:
                # Отправляем уведомление
                try:
                    notification.notify(
                        title="Напоминание о задаче",
                        message=notification_data.get("message", ""),
                        timeout=10  # Время отображения уведомления (в секундах)
                    )
                    self.mark_notification_as_sent(notification_data["id"])
                except Exception as e:
                    print(f"Ошибка при отправке уведомления: {e}")