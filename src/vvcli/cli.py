import fire
from pathlib import Path
from .tools import text_to_speech
from .api import Speakers


def hello(name="World"):
    print("Hello %s!" % name)
    return


def tts(speaker_id, text_file_path, audio_file_dir, max_length=1000, silent=False):
    return text_to_speech(
        speaker_id, text_file_path, audio_file_dir, max_length, silent
    )


def generate__speakers_html():
    sp = Speakers()
    sp.reformat_media()
    sp.generate_html()


def main():
    fire.Fire(
        {
            "hello": hello,
            "tts": tts,
            "text_to_speech": tts,
            "generate__speakers_html": generate__speakers_html,
        }
    )
