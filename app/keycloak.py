import requests

def get_access_token():
    response = requests.post(
        "http://auth_infra:8080/realms/master/protocol/openid-connect/token",
        data={
            "client_id": "admin-cli",
            "username": "admin",
            "password": "password",
            "grant_type": "password",
        },
    )
    return response.json()["access_token"]
