import json
import requests

# APIのurlを定数化する
API_URL = "http://localhost:50021"

def call_api(endpoint: str, params: dict = None, data: dict = None, http_method: str = "GET") -> requests.Response:
    # パラメータ付きのURLを作成する
    url = f"{API_URL}/{endpoint}"
    if params:
        url += "?" + "&".join([f"{key}={value}" for key, value in params.items()])
    headers = {"Content-Type": "application/json; charset=utf-8"}
    # リクエストを送信する
    response = requests.request(http_method, url, data=json.dumps(data), headers=headers)
    response.raise_for_status()
    return response

def get_audio_query(speaker_id: int, text: str):
    # パラメータを設定する
    params = {"text": text, "speaker": speaker_id}
    # APIを呼び出す
    response = call_api("audio_query", params=params, http_method="POST")
    audio_query = response.json()
    return audio_query

def get_wav_data(speaker_id: int, audio_query):
    # リクエストボディにaudio_queryとspeaker_idを設定する
    data = audio_query
    # APIを呼び出す
    response = call_api(f"synthesis?speaker={speaker_id}", data=data, http_method="POST")
    wav_data = response.content
    return wav_data
