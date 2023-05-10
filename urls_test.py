import requests


def index():
    res = requests.get(
        "http://localhost:8000/",
        headers={"Authorization": "Token c507de5ee53d9dc4257f9f517712aba477ba0048"}
    )
    print(res.json())


def register():
    res = requests.post(
        "http://localhost:8000/register/",
        json={
            "username": "nikita6",
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
            "username": "nikita2",
            "password": "Cooler09-",
        }
    )
    print(res.status_code)
    print(res.json())


def friends():
    res = requests.get(
        "http://localhost:8000/friends",
        headers={"Authorization": "Token 3c29de187f60d3a7201a53e5a8003c5aada4de71"}
    )
    print(res)
    print(res.json())


def add_friend():
    res = requests.get(
        "http://localhost:8000/friend/nikita3/",
        headers={"Authorization": "Token 3c29de187f60d3a7201a53e5a8003c5aada4de71"}
    )
    print(res.json())


add_friend()
# friends()
# login()
# register()
