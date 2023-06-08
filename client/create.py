import requests


login = requests.post(
    "http://127.0.0.1:8000/accounts/login/",
    json={"username": "Abdusamad", "email": "abdusamad@gmail.com", "password": "20051205"}
)
print(login.status_code)
request = requests.post(
    "http://127.0.0.1:8000/blogs/create/",
    json={"title": "asdasd", "content": "lorem ipsum", "image": "posters/Blank_diagram.png", "category": 2},
    headers={"Authorization": "Token 9bdf051a2b3be4690180f504a2bd171565ed2f26"},
)
print(request.status_code)
