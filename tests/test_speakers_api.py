import json
from pathlib import Path
from vvcli.api import Speakers
import pprint


class TestSpeakers:
    def test_01(self, save_json, speakers_sample, resources_dir):
        s = Speakers()
        s.reformat_media()
        s.generate_html()

        # html = s.generate_html()
        # html_path = resources_dir / ".." / "index.html"
        # html_path.write_text(html)
        print("===================")
        # for ss in s.speakers:
        #     print(
        #         ss["speaker_info"]["policy"],
        #         ss["name"],
        #     )
        # assert 1 == 0
        # save_json(s, "speaker_info.json")

    # def test_02(self, save_json):
    #     si = speaker_info("388f246b-8c41-4ac1-8e2d-5d79f3ff56d9")
    #     print(si)
    #     save_json(si, "speaker_info.json")


"""
```
site_dir = Path('site')
resources_dir = site_dir / 'resources'
sp = Speakers().reformat_media(resources_dir)
```
Speakersクラスのインスタンスからdataを取得できます。
このdataを使って、speakerの一覧を表示するhtmlを作成するメソッド`generate_html`を作って下さい。
修正が容易になるように、jinja2を使いたいと思います。
よろしくお願いします。
"""
