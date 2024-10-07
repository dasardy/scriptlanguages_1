import sqlite3
import requests
import json

#СОЗДАНИЕ БД
connection = sqlite3.connect('posts.db')
cursor = connection.cursor()
cursor.execute("DROP TABLE IF EXISTS Posts")
cursor.execute(
    ''' CREATE TABLE IF NOT EXISTS Posts(
        id INTEGER PRIMARY KEY,
        user_id INTEGER, 
        title TEXT, 
        body TEXT
    )
    '''
)
#ВНЕСЕНИЕ ПОСТОВ В БД
url = "https://jsonplaceholder.typicode.com/posts"
allposts = requests.get(url)
posts = allposts.json()
for post in posts:
    cursor.execute("INSERT INTO posts(user_id, title, body) VALUES (?, ?, ?)", (post["userId"], post["title"], post["body"]))
connection.commit()

#ВЫВОД ВСЕХ ПОСТОВ
cursor.execute('SELECT * FROM Posts')
postlist1 = cursor.fetchall()
for post in postlist1:
  print(post)

#ВЫВОД ПОСТОВ С ОПРЕДЕЛЁННЫМ ID
userId = input("Введите ID пользователя: ")
cursor.execute("SELECT user_id, body FROM Posts WHERE user_id = ?", (userId,))
postlist1 = cursor.fetchall()
for post in postlist1:
  print(post)
connection.close()
