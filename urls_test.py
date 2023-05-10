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
            "username": "nikita",
            "password": "Cooler09-",
        }
    )
    print(res.status_code)
    print(res.json())


def friends():
    res = requests.get(
        "http://localhost:8000/friends",
        headers={"Authorization": "Token c507de5ee53d9dc4257f9f517712aba477ba0048"}
    )
    print(res)
    print(res.json())


def add_friend():
    res = requests.get(
        "http://localhost:8000/friend/nikita2/",
        headers={"Authorization": "Token c507de5ee53d9dc4257f9f517712aba477ba0048"}
    )
    print(res.json())


add_friend()
# friends()
# login()
# register()
