import requests


def index():
    res = requests.get(
        "http://localhost:8000/",
        headers={"Authorization": "Token 7673d33fec0893db4bb18cc3243fc576da4c37e0"}
    )
    print(res.json())


def register():
    res = requests.post(
        "http://localhost:8000/register/",
        json={
            "username": "nikita5",
            "password": "Cooler09-",
            "email": "test2@test.ru",
        }
    )
    print(res.status_code)
    print(res.json())


def login():
    res = requests.post(
        "http://localhost:8000/token/",
        json={
            "username": "nikita",
            "password": "123",
        }
    )
    print(res.status_code)
    print(res.json())


def friends():
    res = requests.get(
        "http://localhost:8000/friends",
        headers={"Authorization": "Token 7673d33fec0893db4bb18cc3243fc576da4c37e0"}
    )
    print(res.text)


def add_friend():
    res = requests.get(
        "http://localhost:8000/friend/add/1",
        headers={"Authorization": "Token 7673d33fec0893db4bb18cc3243fc576da4c37e0"}
    )
    print(res)


add_friend()
