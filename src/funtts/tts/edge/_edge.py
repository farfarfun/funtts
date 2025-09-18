import asyncio
import time
from typing import List, Optional

from edge_tts import Communicate, list_voices
from edge_tts import SubMaker as EdgeSubMaker
from funutil import getLogger, deep_get
from funutil.util.retrying import retry

from funtts.base import BaseTTS
from funtts.models import TTSRequest, TTSResponse, VoiceInfo, SubtitleMaker

logger = getLogger("funtts")


def convert_rate_to_percent(rate: float) -> str:
    if rate == 1.0:
        return "+0%"
    percent = round((rate - 1.0) * 100)
    if percent > 0:
        return f"+{percent}%"
    else:
        return f"{percent}%"


class EdgeTTS(BaseTTS):
    """Microsoft Edge TTS引擎实现"""

    def __init__(self, voice_name: str = "zh-CN-XiaoxiaoNeural", *args, **kwargs):
        """初始化Edge TTS

        Args:
            voice_name: 语音名称
        """
        super().__init__(voice_name, *args, **kwargs)

    def list_voices(self, language: Optional[str] = None) -> List[VoiceInfo]:
        """获取可用的语音列表

        Args:
            language: 语言代码过滤（如 'zh-CN'）

        Returns:
            语音信息列表
        """
        try:
            voice_list = asyncio.run(list_voices())
            result = []

            for voice in voice_list:
                locale = deep_get(voice, "Locale", "")
                if language and not locale.startswith(language):
                    continue

                voice_info = VoiceInfo(
                    name=deep_get(voice, "Name", ""),
                    display_name=deep_get(voice, "DisplayName", ""),
                    language=deep_get(voice, "Language", ""),
                    gender=deep_get(voice, "Gender", "").lower(),
                    region=locale.split("-")[1] if "-" in locale else "unknown",
                    engine="edge",
                    sample_rate=24000,
                    quality="high",
                    metadata={
                        "locale": locale,
                        "local_name": deep_get(voice, "LocalName", ""),
                        "short_name": deep_get(voice, "ShortName", ""),
                        "voice_tag": deep_get(voice, "VoiceTag", {}),
                    },
                )
                result.append(voice_info)

            return result

        except Exception as e:
            logger.error(f"获取Edge TTS语音列表失败: {str(e)}")
            return []

    @retry(4)
    def _synthesize(self, request: TTSRequest) -> TTSResponse:
        """Edge TTS语音合成核心方法

        Args:
            request: TTS请求对象

        Returns:
            TTS响应对象
        """
        start_time = time.time()
        text = request.text.strip()
        voice_file = request.output_file

        if not voice_file:
            import tempfile

            voice_file = tempfile.mktemp(suffix=f".{request.output_format}")

        try:
            rate_str = convert_rate_to_percent(request.voice_rate)
            voice_name = request.voice_name or self.default_voice
            communicate = Communicate(text, voice_name, rate=rate_str)
            edge_sub_maker = EdgeSubMaker()

            # 创建我们自己的字幕制作器
            subtitle_maker = SubtitleMaker() if request.generate_subtitles else None

            with open(voice_file, "wb") as file:
                for chunk in communicate.stream_sync():
                    if chunk["type"] == "audio":
                        file.write(chunk["data"])
                    elif chunk["type"] == "WordBoundary" and subtitle_maker:
                        edge_sub_maker.create_sub(
                            (chunk["offset"], chunk["duration"]), chunk["text"]
                        )
                        # 同时添加到我们的字幕制作器
                        subtitle_maker.add_segment_from_offset(
                            (chunk["offset"], chunk["duration"]), chunk["text"]
                        )

            # 获取音频时长
            duration = (
                subtitle_maker.get_total_duration()
                if subtitle_maker
                else self._get_audio_duration(voice_file)
            )

            logger.success(
                f"Edge TTS合成完成: voice={voice_name}, file={voice_file}, duration={duration:.2f}s"
            )

            return TTSResponse(
                success=True,
                request=request,
                audio_file=voice_file,
                subtitle_maker=subtitle_maker,
                duration=duration,
                voice_used=voice_name,
                processing_time=time.time() - start_time,
                engine_info=self.get_engine_info(),
            )

        except Exception as e:
            logger.error(f"Edge TTS处理失败: {str(e)}")
            return TTSResponse(
                success=False,
                request=request,
                error_message=str(e),
                error_code="EDGE_ERROR",
                processing_time=time.time() - start_time,
            )

    def _get_audio_duration(self, audio_file: str) -> float:
        """获取音频文件时长"""
        try:
            import subprocess

            result = subprocess.run(
                [
                    "ffprobe",
                    "-v",
                    "quiet",
                    "-show_entries",
                    "format=duration",
                    "-of",
                    "csv=p=0",
                    audio_file,
                ],
                capture_output=True,
                text=True,
                timeout=10,
            )

            if result.returncode == 0:
                return float(result.stdout.strip())
        except Exception:
            pass

        # 估算时长
        try:
            import os

            file_size = os.path.getsize(audio_file)
            # MP3文件大约16KB/s (24kHz)
            return file_size / 16000
        except Exception:
            return 0.0

    def get_engine_info(self) -> dict:
        """获取引擎信息"""
        return {
            "engine_name": "EdgeTTS",
            "version": "1.0",
            "default_voice": self.default_voice,
            "supported_formats": ["wav", "mp3"],
            "max_text_length": 10000,
            "supports_ssml": True,
            "supports_subtitles": True,
            "free_tier": True,
        }
