import json
import requests

# APIのurlを定数化する
API_URL = "http://localhost:50021"

def get_audio_query(speaker_id: int, text: str):
    # パラメータ付きのURLを作成する
    url = f"{API_URL}/audio_query?text={text}&speaker={speaker_id}"
    # POSTリクエストを送信する
    response = requests.post(url)
    response.raise_for_status()
    audio_query = response.json()
    assert type(audio_query) is dict
    return audio_query

def get_wav_data(speaker_id: int, audio_query):
    # リクエストボディにaudio_queryとspeaker_idを設定する
    data = json.dumps(audio_query)
    headers = {"Content-Type": "application/json; charset=utf-8"}
    # POSTリクエストを送信する
    response = requests.post(f"{API_URL}/synthesis?speaker={speaker_id}", data=data, headers=headers)
    response.raise_for_status()
    wav_data = response.content
    return wav_data
