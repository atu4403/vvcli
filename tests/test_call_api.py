import json
import requests
import pytest
import sys
import pprint
from vvcli.api import call_api, get_audio_query, get_wav_data

expected_error_msg = "422 Client Error: Unprocessable Entity for url"


class TestAudioQuery:
    def test_01(self, audio_query_sample):
        response = call_api(
            "audio_query", {"speaker": 1, "text": "test text"}, http_method="POST"
        )
        assert response.status_code == 200
        expected_json = audio_query_sample
        assert response.json() == expected_json

    def test_02(self):
        # リクエストボディに不正なデータが含まれている場合、422エラーが発生することを確認する
        with pytest.raises(requests.exceptions.HTTPError, match=expected_error_msg):
            response = call_api(
                "audio_query",
                data={"speaker": 1, "text": "test text"},
                http_method="POST",
            )

    def test_03(self, audio_query_sample):
        assert get_audio_query(1, "test text") == audio_query_sample


class TestSynthesis:
    def test_01(self, audio_query_sample):
        # speakerはurlに含める必要があり、audio_queryはリクエストボディに含める必要がある
        response = call_api(
            "synthesis",
            {"speaker": 1},
            data=audio_query_sample,
            http_method="POST",
        )
        assert response.status_code == 200

    def test_02(self, audio_query_sample):
        # リクエストボディにspeakerが含まれている場合、422エラーが発生することを確認する
        data = audio_query_sample
        data["speaker"] = 1
        with pytest.raises(requests.exceptions.HTTPError, match=expected_error_msg):
            response = call_api("synthesis", data=data, http_method="POST")
