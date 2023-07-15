import json
import requests
import pytest
from pathlib import Path
from vvcli.api import call_api, get_audio_query, get_wav_data

SAMPLES_DIR = Path("tests/samples")
audio_query_str = (SAMPLES_DIR / "audio_query.json").read_text()
audio_query_sample = json.loads(audio_query_str)
expected_error_msg = "422 Client Error: Unprocessable Entity for url"


class TestAudioQuery:
    audio_query_sample = audio_query_sample

    def test_01(self):
        response = call_api(
            "audio_query", {"speaker": 1, "text": "test text"}, http_method="POST"
        )
        assert response.status_code == 200
        expected_json = self.audio_query_sample
        assert response.json() == expected_json

    def test_02(self):
        # リクエストボディに不正なデータが含まれている場合、422エラーが発生することを確認する
        with pytest.raises(requests.exceptions.HTTPError, match=expected_error_msg):
            response = call_api(
                "audio_query",
                data={"speaker": 1, "text": "test text"},
                http_method="POST",
            )

    def test_03(self):
        assert get_audio_query(1, "test text") == self.audio_query_sample


class TestSynthesis:
    audio_query_sample = audio_query_sample

    def test_01(self):
        response = call_api(
            "synthesis",
            {"speaker": 1},
            data=self.audio_query_sample,
            http_method="POST",
        )
        assert response.status_code == 200

    def test_02(self):
        # リクエストボディに不正なデータが含まれている場合、422エラーが発生することを確認する
        data = self.audio_query_sample
        data["speaker"] = 1
        with pytest.raises(requests.exceptions.HTTPError, match=expected_error_msg):
            response = call_api("synthesis", data=data, http_method="POST")
