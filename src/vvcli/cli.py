import fire
from .tools import text_to_speech


def hello(name="World"):
    print("Hello %s!" % name)
    return


def tts(speaker_id, text_file_path, audio_file_dir, max_length=1000, silent=False):
    return text_to_speech(
        speaker_id, text_file_path, audio_file_dir, max_length, silent
    )


def main():
    fire.Fire({"hello": hello, "tts": tts, "text_to_speech": tts})
