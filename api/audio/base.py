import os
import uuid
from pathlib import Path

import requests


class Audio:
    audio_mode_dict = {
        "Nanami": {"gender": "Female", "shortName": "ja-JP-NanamiNeural"},
        "Aoi": {"gender": "Femail", "shortName": "ja-JP-AoiNeural"},
        "Daichi": {"gender": "Male", "shortName": "ja-JP-DaichiNeural"},
        "Keita": {"gender": "Male", "shortName": "ja-JP-KeitaNeural"},
        "Mayu": {"gender": "Female", "shortName": "ja-JP-MayuNeural"},
        "Naoki": {"gender": "Mail", "shortName": "ja-JP-NaokiNeural"},
        "Shiori": {"gender": "Femail", "shortName": "ja-JP-ShioriNeural"},
    }

    def __init__(self, token: uuid, mode: str = "Nanami") -> None:
        """
        mode: Nanami, Aoi, Daichi, Keita, Mayu, Naoki, Shiori
        """
        self.mode = mode
        self.url = "https://japaneast.tts.speech.microsoft.com/cognitiveservices/v1"
        self.headers = {
            "Ocp-Apim-Subscription-Key": os.getenv("AUDIO_OCPKEY"),
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/"
            "537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
            "Ocp-Apim-Subscription-Region": "japaneast",
            "Content-Type": "application/ssml+xml",
            "X-Microsoft-OutputFormat": "riff-24khz-16bit-mono-pcm",
            "Authorization": f"Bearer {os.getenv('AUDIO_AUTH')}",
        }
        self.token = token

    def azure(self, text: str):
        # text = text.encode('utf-8')
        resp = requests.post(
            url=self.url,
            headers=self.headers,
            data=f"""<speak version='1.0' xml:lang='ja-JP'><voice xml:lang='ja-JP'
                xml:gender='{self.audio_mode_dict[self.mode]['gender']}'
                name='{self.audio_mode_dict[self.mode]['shortName']}'>
                    {text}
                </voice> </speak>""".encode(),
        )

        Path("assets/audio").mkdir(parents=True, exist_ok=True)
        filename = f"assets/audio/{self.token}.mp3"
        with open(filename, mode="wb") as f:
            f.write(resp.content)
            f.close()
        return True


# Audio().azure("hello how are you?")
