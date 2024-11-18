from PyQt5 import QtWidgets, QtSql, QtCore
from PyQt5.QtCore import QTimer
import sys
import requests
import asyncio
import sqlite3


# Подключение к БД
def create_connection():
    DB = QtSql.QSqlDatabase.addDatabase('QSQLITE')
    DB.setDatabaseName('posts.db')
    if not DB.open():
        QtWidgets.QMessageBox.critical(None, "Ошибка", "Не удалось подключиться к базе данных.")
        return False
    return True


def add_record():
    row = main_model.rowCount()
    main_model.insertRow(row)
    main_model.setData(main_model.index(row, 1), postUserID_text.text())
    main_model.setData(main_model.index(row, 2), postTitle_text.text())
    main_model.setData(main_model.index(row, 3), postBody_text.text())
    if not main_model.submitAll():
        QtWidgets.QMessageBox.warning(None, "Ошибка", "Не удалось добавить запись.")
    else:
        postUserID_text.clear()
        postTitle_text.clear()
        postBody_text.clear()
        main_model.select()


def display_selected_row(index):
    if index.isValid():
        user_id = str(main_model.data(main_model.index(index.row(), 1)))
        title = str(main_model.data(main_model.index(index.row(), 2)))
        body = str(main_model.data(main_model.index(index.row(), 3)))

        postUserID_text.setText(user_id)
        postTitle_text.setText(title)
        postBody_text.setText(body)


def update_record(index):
    main_model.setData(main_model.index(index.row(), 1), postUserID_text.text())
    main_model.setData(main_model.index(index.row(), 2), postTitle_text.text())
    main_model.setData(main_model.index(index.row(), 3), postBody_text.text())

    if not main_model.submitAll():
        QtWidgets.QMessageBox.warning(None, "Ошибка", "Не удалось обновить запись.")
    else:
        postUserID_text.clear()
        postTitle_text.clear()
        postBody_text.clear()
        main_model.select()


def delete_record():
    index = main_table.selectionModel().currentIndex()
    if index.isValid():
        main_model.removeRow(index.row())
        if not main_model.submitAll():
            QtWidgets.QMessageBox.warning(None, "Ошибка", "Не удалось удалить запись.")
        else:
            postUserID_text.clear()
            postTitle_text.clear()
            postBody_text.clear()
            main_model.select()


def search_post():
    search_text = search_line.text()
    filter_str = f"Title LIKE '%{search_text}%'"
    main_model.setFilter(filter_str)
    main_model.select()

class UploadWorker(QtCore.QThread):
    progress_updated = QtCore.pyqtSignal(int)
    upload_finished = QtCore.pyqtSignal()

    def run(self):
        asyncio.run(self.upload_posts())

    async def upload_posts(self):
        status_label.setText("Запуск выполнения запроса...")
        await asyncio.sleep(3)
        url = "https://jsonplaceholder.typicode.com/posts"
        allposts = requests.get(url)
        posts = allposts.json()
        status_label.setText("Запрос выполнен")
        await self.insert_posts_to_db_async(posts)

    async def insert_posts_to_db_async(self, posts):
        status_label.setText("Данные получены. Выполняется загрузка...")
        total_posts = len(posts)
        connection = sqlite3.connect('posts.db')
        cursor = connection.cursor()
        for index, onepost in enumerate(posts):
            await asyncio.sleep(0.1)
            cursor.execute("INSERT INTO posts(user_id, title, body) VALUES (?, ?, ?)",
                           (onepost["userId"], onepost["title"], onepost["body"]))
            connection.commit()
            self.progress_updated.emit(index + 1)

        connection.close()
        status_label.setText("Загрузка данных завершена!")
        self.upload_finished.emit()
        main_model.select()
        
class UpdateWorker(QtCore.QThread):
    update_finished = QtCore.pyqtSignal()
    def run(self):
        asyncio.run(self.check_for_updates_async())

    async def check_for_updates_async(self):
        url = "https://jsonplaceholder.typicode.com/posts"
        await asyncio.sleep(2)
        new_posts = requests.get(url).json()
        connection = sqlite3.connect('posts.db')
        cursor = connection.cursor()
        cursor.execute("SELECT user_id, title, body FROM posts")
        existing_posts = cursor.fetchall()

        
        for post in new_posts:
            if (post["userId"], post["title"], post["body"]) not in existing_posts:
                cursor.execute(
                    "INSERT INTO posts(user_id, title, body) VALUES (?, ?, ?)",
                    (post["userId"], post["title"], post["body"]),
                )
                connection.commit()
                
        connection.close()
    
        self.update_finished.emit()
        

# Настройка интерфейса
app = QtWidgets.QApplication(sys.argv)
window = QtWidgets.QWidget()

window.setWindowTitle("Laba4")
window.resize(800, 600)

search_line = QtWidgets.QLineEdit()
search_line.setPlaceholderText("Поиск...")
main_table = QtWidgets.QTableView()

postUserID_text = QtWidgets.QLineEdit()
postTitle_text = QtWidgets.QLineEdit()
postBody_text = QtWidgets.QLineEdit()

postUserID_text.setPlaceholderText("UserID")
postTitle_text.setPlaceholderText("Title")
postBody_text.setPlaceholderText("Body")

upload_btn = QtWidgets.QPushButton("Загрузить данные")
add_btn = QtWidgets.QPushButton("Добавить")
update_btn = QtWidgets.QPushButton("Обновить")
del_btn = QtWidgets.QPushButton("Удалить")

main_box = QtWidgets.QVBoxLayout()
btn_box = QtWidgets.QHBoxLayout()
text_box = QtWidgets.QHBoxLayout()

progress_bar = QtWidgets.QProgressBar()
status_label = QtWidgets.QLabel("")

btn_box.addWidget(add_btn)
btn_box.addWidget(update_btn)
btn_box.addWidget(del_btn)

text_box.addWidget(postUserID_text)
text_box.addWidget(postTitle_text)
text_box.addWidget(postBody_text)

main_box.addWidget(upload_btn)
main_box.addWidget(search_line)
main_box.addWidget(main_table)
main_box.addLayout(text_box)
main_box.addLayout(btn_box)
main_box.addWidget(progress_bar)
main_box.addWidget(status_label)

window.setLayout(main_box)

connection = create_connection()
main_model = QtSql.QSqlTableModel()
main_model.setTable("posts")
main_model.setEditStrategy(QtSql.QSqlTableModel.OnFieldChange)
main_model.select()

main_model.setHeaderData(0, QtCore.Qt.Horizontal, "ID")
main_model.setHeaderData(1, QtCore.Qt.Horizontal, "User ID")
main_model.setHeaderData(2, QtCore.Qt.Horizontal, "Title")
main_model.setHeaderData(3, QtCore.Qt.Horizontal, "Body")

upload_worker = UploadWorker()
upload_worker.progress_updated.connect(progress_bar.setValue)

upload_btn.clicked.connect(lambda: upload_worker.start())
add_btn.clicked.connect(add_record)
update_btn.clicked.connect(lambda: update_record(selection_model.currentIndex()))
del_btn.clicked.connect(delete_record)
search_line.textChanged.connect(search_post)

main_table.setModel(main_model)
selection_model = main_table.selectionModel()

update_timer = QTimer()
update_timer.setInterval(10000)  
update_timer.start()

update_worker = UpdateWorker()

update_worker.update_finished.connect(main_model.select) 
update_timer.timeout.connect(lambda: update_worker.start())

window.show()
sys.exit(app.exec())
