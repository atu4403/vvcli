import argparse

from src.vvcli import text_to_speech

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("speaker_id", type=int, help="speakerのID")
    parser.add_argument("text_file_path", type=str, help="テキストファイルのパス")
    parser.add_argument("audio_file_path", type=str, help="音声ファイルのパス")
    args = parser.parse_args()

    text_to_speech(args.speaker_id, args.text_file_path, args.audio_file_path)
