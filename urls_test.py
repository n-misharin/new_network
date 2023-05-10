import requests


def index():
    res = requests.get(
        "http://localhost:8000/",
        headers={"Authorization": "Token 08297b19db8d994e6edd5df4f30499153e8cb1d0"}
    )
    print(res.json())


def register():
    res = requests.post(
        "http://localhost:8000/register/",
        json={
            "username": "nikita2",
            "password": "Cooler09-",
        }
    )
    print(res.status_code)
    print(res)


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


register()
