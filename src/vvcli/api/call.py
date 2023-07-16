import json
import requests

# APIのurlを定数化する
API_URL = "http://localhost:50021"


def call_api(
    endpoint: str, params: dict = None, data: dict = None, http_method: str = "GET"
) -> requests.Response:
    # パラメータ付きのURLを作成する
    url = f"{API_URL}/{endpoint}"
    if params:
        url += "?" + "&".join([f"{key}={value}" for key, value in params.items()])
    headers = {"Content-Type": "application/json; charset=utf-8"}
    # リクエストを送信する
    response = requests.request(
        http_method, url, data=json.dumps(data), headers=headers
    )
    response.raise_for_status()
    return response
