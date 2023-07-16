from datetime import datetime
from pathlib import Path
import time
from alive_progress import alive_bar
from .api import get_audio_query, get_wav_data
from .util import split_text


def text_to_speech(
    speaker_id: int,
    text_file_path: str,
    audio_file_dir: str,
    max_length=1000,
    silent=False,
):
    text_file_path = Path(text_file_path)
    audio_file_dir = Path(audio_file_dir)

    # テキストファイルの内容を読み込む
    text = text_file_path.read_text(encoding="utf-8")

    # テキストを分割する
    segments = split_text(text, max_length=max_length)

    # タイムスタンプを取得する
    now = datetime.now()
    timestamp = now.strftime("%y%m%d_%H%M%S")

    # 出力ディレクトリが存在しない場合は作成する
    audio_file_dir.mkdir(parents=True, exist_ok=True)

    # 分割されたテキストごとに音声データを取得して保存する
    with alive_bar(len(segments), manual=True, disable=silent) as bar:
        for i, segment in enumerate(segments):
            time.sleep(0.5)
            # 音声データを取得する
            audio_query = get_audio_query(speaker_id, segment)
            wav_data = get_wav_data(speaker_id, audio_query)

            # 音声データを保存する
            audio_file_name = f"{timestamp}_{i+1}.wav"
            audio_file_path = audio_file_dir / audio_file_name
            audio_file_path.write_bytes(wav_data)

            bar(i + 1)

    return
