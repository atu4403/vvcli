from .call import call_api
from PIL import Image
import base64
import io
import json
import re
import os
from jinja2 import Environment, FileSystemLoader
from pydub import AudioSegment


class Speakers:
    def __init__(self):
        self.speakers = self.get_speakers()
        self.styles = self.get_styles()

    def get_speakers(self):
        speakers = call_api("speakers").json()
        for speaker in speakers:
            speaker["speaker_info"] = call_api(
                "speaker_info", {"speaker_uuid": speaker["speaker_uuid"]}
            ).json()
        return speakers

    def get_styles(self):
        styles = []
        for speaker in self.speakers:
            for style in speaker["styles"]:
                style_info = next(
                    (
                        x
                        for x in speaker["speaker_info"]["style_infos"]
                        if x["id"] == style["id"]
                    ),
                    None,
                )
                if style_info:
                    style.update(style_info)
                styles.append(style)
        return styles

    def reformat_media(self):
        save_dir = os.path.join(os.environ["VVCLI_ROOT"], "site", "resources")
        os.makedirs(save_dir, exist_ok=True)

        styles_data = []
        for style in self.styles:
            style_data = {"id": style["id"]}
            if "icon" in style and style["icon"] is not None:
                icon_path = self._save_image(
                    style["icon"], f"icon_{style['id']}_.webp", save_dir
                )
                style_data["icon_path"] = icon_path
            if "portrait" in style and style["portrait"] is not None:
                portrait_path = self._save_image(
                    style["portrait"], f"portrait_{style['id']}_.webp", save_dir
                )
                style_data["portrait_path"] = portrait_path
            if "voice_samples" in style:
                voices = []
                for i, sample in enumerate(style["voice_samples"]):
                    if sample is not None:
                        voice_path = self._save_audio(
                            sample, f"voice_{style['id']}_{i}_.mp3", save_dir
                        )
                        voices.append(voice_path)
                if voices:
                    style_data["voices"] = voices
            styles_data.append(style_data)

        with open(os.path.join(save_dir, "styles.json"), "w") as f:
            json.dump(styles_data, f, ensure_ascii=False, indent=2)

        speakers_resources_data = []
        for speaker in self.speakers:
            speaker_resource_data = {"speaker_uuid": speaker["speaker_uuid"]}
            if (
                "portrait" in speaker["speaker_info"]
                and speaker["speaker_info"]["portrait"] is not None
            ):
                portrait_path = self._save_image(
                    speaker["speaker_info"]["portrait"],
                    f"portrait_{speaker['speaker_uuid']}_.webp",
                    save_dir,
                )
                speaker_resource_data["portrait_path"] = portrait_path
            speakers_resources_data.append(speaker_resource_data)

        with open(os.path.join(save_dir, "speakers_resources.json"), "w") as f:
            json.dump(speakers_resources_data, f, ensure_ascii=False, indent=2)

    def _save_image(self, data, filename, save_dir):
        filepath = os.path.join(save_dir, filename)
        if os.path.exists(filepath):
            return filepath
        img_data = base64.b64decode(data)
        img = Image.open(io.BytesIO(img_data))
        img.save(filepath, "WEBP")
        return filepath

    def _save_audio(self, data, filename, save_dir):
        filepath = os.path.join(save_dir, filename)
        if os.path.exists(filepath):
            return filepath
        audio_data = base64.b64decode(data)
        audio = AudioSegment.from_file(io.BytesIO(audio_data), format="wav")
        audio.export(filepath, format="mp3")
        return filepath

    def generate_html(self):
        template_dir = os.path.join(os.environ["VVCLI_ROOT"], "site", "templates")
        env = Environment(loader=FileSystemLoader(template_dir))
        template = env.get_template("speakers_template.html")

        with open(
            os.path.join(os.environ["VVCLI_ROOT"], "site", "resources", "styles.json")
        ) as f:
            styles_data = json.load(f)

        with open(
            os.path.join(
                os.environ["VVCLI_ROOT"], "site", "resources", "speakers_resources.json"
            )
        ) as f:
            speakers_resources_data = json.load(f)

        speakers_data = []
        for speaker in self.speakers:
            speaker_data = speaker.copy()
            policy_parts = self._split_text_with_urls(speaker["speaker_info"]["policy"])
            speaker_data["policy_parts"] = policy_parts
            speakers_data.append(speaker_data)

        html = template.render(
            speakers=speakers_data,
            styles_data=styles_data,
            speakers_resources_data=speakers_resources_data,
        )

        with open(
            os.path.join(os.environ["VVCLI_ROOT"], "site", "speakers.html"), "w"
        ) as f:
            f.write(html)

    def _split_text_with_urls(self, text):
        url_pattern = re.compile(
            r"\b(https?|ftp|file)://[-A-Z0-9+&@#/%?=~_|!:,.;]*[-A-Z0-9+&@#/%=~_|]",
            re.IGNORECASE,
        )
        parts = []
        last_end = 0
        for match in url_pattern.finditer(text):
            if match.start() > last_end:
                parts.append({"type": "text", "text": text[last_end : match.start()]})
            parts.append({"type": "url", "text": match.group(), "url": match.group()})
            last_end = match.end()
        if last_end < len(text):
            parts.append({"type": "text", "text": text[last_end:]})
        return parts
