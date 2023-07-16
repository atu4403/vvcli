from .call import call_api


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
    response = call_api(
        f"synthesis?speaker={speaker_id}", data=data, http_method="POST"
    )
    wav_data = response.content
    return wav_data
