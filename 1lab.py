import requests
import json

#task1
url = "https://jsonplaceholder.typicode.com/posts"
allposts = requests.get(url)
posts = allposts.json()
for onepost in posts:
    if onepost["userId"] % 2 == 0:
        print(onepost["userId"], onepost["title"], onepost["body"])
print(posts)
#task2

userId = 1
title = "Тестовый пост"
body = "Это тело поста, очень важное"
newpost = requests.post(url, data={"userId": userId, "title": title, "body": body})
print("Сформированный JSON: ", requests.Response.json(newpost))

#task3
url = "https://jsonplaceholder.typicode.com/posts/100"
title = "Обновленный пост"
body = "Новое тело поста"
updatepost = requests.put(url, data={"userId": userId, "title": title, "body": body})
print("Сформированный JSON: ", requests.Response.json(updatepost))