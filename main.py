from PySide6 import QtWidgets, QtSql, QtCore  # Импорт модуля QtWidgets из библиотеки PySide6

import sys  
#подключение к БД
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
    main_model.setFilter(filter_str)  # Установка фильтра для поиска по названию
    main_model.select()  # Обновляем таблицу после применения фильтра


    
        
app = QtWidgets.QApplication(sys.argv)
window = QtWidgets.QWidget()


window.setWindowTitle("Laba4")
window.resize(800, 600)

search_line = QtWidgets.QLineEdit() #поиск
main_table = QtWidgets.QTableView() #таблица

postUserID_text = QtWidgets.QLineEdit()
postTitle_text = QtWidgets.QLineEdit()
postBody_text = QtWidgets.QLineEdit()

add_btn = QtWidgets.QPushButton("Добавить")
update_btn = QtWidgets.QPushButton("Обновить")
del_btn = QtWidgets.QPushButton("Удалить")

main_box = QtWidgets.QVBoxLayout()
btn_box = QtWidgets.QHBoxLayout()
text_box = QtWidgets.QHBoxLayout()


btn_box.addWidget(add_btn)
btn_box.addWidget(update_btn)
btn_box.addWidget(del_btn)

text_box.addWidget(postUserID_text)
text_box.addWidget(postTitle_text)
text_box.addWidget(postBody_text)

main_box.addWidget(search_line)
main_box.addWidget(main_table)
main_box.addLayout(text_box)
main_box.addLayout(btn_box)


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

add_btn.clicked.connect(add_record)
update_btn.clicked.connect(lambda: update_record(selection_model.currentIndex()))
del_btn.clicked.connect(delete_record)
search_line.textChanged.connect(search_post)


main_table.setModel(main_model)
selection_model = main_table.selectionModel()
selection_model.currentChanged.connect(display_selected_row)

window.show()
sys.exit(app.exec())  # После завершения цикла приложение выходит из программы