from wyze_sdk import Client
from wyze_sdk.errors import WyzeApiError

username = "email@example.com"
password = "password"

try:
    data = Client().login(email=username, password=password)
    print(data)
    start_token = data["access_token"]
    print(start_token)
except WyzeApiError as e:
    print(f'Got an error: {e}')