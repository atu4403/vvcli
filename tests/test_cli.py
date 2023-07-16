import sys
import pytest
from vvcli.cli import hello, main


def test_main_hello(mocker, argv):
    sys.argv = ["vv", "hello", "--name=John"]
    mock_hello = mocker.patch("vvcli.cli.hello")
    mock_hello.return_value = True
    main()
    mock_hello.assert_called_with(name="John")


def test_main_tts(mocker, argv):
    txt_path, audio_dir_path = "test.txt", "audio_dir_path"
    sys.argv = ["vv", "tts", "1", txt_path, audio_dir_path]
    mock_tts = mocker.patch("vvcli.cli.tts")
    mock_tts.return_value = True
    main()
    mock_tts.assert_called_with(1, txt_path, audio_dir_path)
