from pathlib import Path
from .api import get_audio_query, get_wav_data

def text_to_speech(speaker_id: int, text_file_path: str, audio_file_path: str):
    text_file_path = Path(text_file_path)
    audio_file_path = Path(audio_file_path)

    # テキストファイルの内容を読み込む
    text = text_file_path.read_text(encoding="utf-8")

    # 音声ファイルのパスの末尾に[.wav]が付いていない場合は付与する
    if not audio_file_path.suffix == ".wav":
        audio_file_path = audio_file_path.with_suffix(".wav")

    # 音声データを取得する
    audio_query = get_audio_query(speaker_id, text)
    wav_data = get_wav_data(speaker_id, audio_query)

    # 音声データを保存する
    audio_file_path.write_bytes(wav_data)
