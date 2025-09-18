"""
pyttsx3 TTS引擎封装
pyttsx3是一个跨平台的Python文本转语音库
"""

import os
import time
import tempfile
from typing import List, Optional
import pyttsx3


from funutil import getLogger

from funtts.base import BaseTTS
from funtts.models import (
    TTSRequest,
    TTSResponse,
    VoiceInfo,
    SubtitleMaker,
    AudioSegment,
)

logger = getLogger("funtts")


class Pyttsx3TTS(BaseTTS):
    """pyttsx3 TTS引擎实现"""

    def __init__(self, voice_name: str = "default", *args, **kwargs):
        """初始化pyttsx3 TTS

        Args:
            voice_name: 语音名称或ID
        """
        super().__init__(voice_name, *args, **kwargs)
        self.engine = None
        self._init_engine()

    def _init_engine(self):
        """初始化pyttsx3引擎"""
        try:
            self.engine = pyttsx3.init()

            # 设置语音
            voices = self.engine.getProperty("voices")
            if voices:
                # 如果voice_name是数字，按索引选择
                if self.voice_name.isdigit():
                    voice_index = int(self.voice_name)
                    if 0 <= voice_index < len(voices):
                        self.engine.setProperty("voice", voices[voice_index].id)
                else:
                    # 按名称或ID匹配
                    for voice in voices:
                        if self.voice_name in voice.name or self.voice_name == voice.id:
                            self.engine.setProperty("voice", voice.id)
                            break

            logger.info(f"pyttsx3引擎初始化成功，语音: {self.voice_name}")

        except Exception as e:
            logger.error(f"pyttsx3引擎初始化失败: {str(e)}")
            raise

    def _synthesize(self, request: TTSRequest) -> TTSResponse:
        """pyttsx3语音合成核心方法

        Args:
            request: TTS请求对象

        Returns:
            TTS响应对象
        """
        start_time = time.time()
        try:
            if not self.engine:
                self._init_engine()

            # 准备输出文件
            output_file = request.output_file
            if not output_file:
                output_file = tempfile.mktemp(suffix=f".{request.output_format}")

            # 设置语音速率 (pyttsx3默认速率约200)
            rate = int(200 * request.voice_rate)
            rate = max(50, min(400, rate))  # 限制在合理范围内
            self.engine.setProperty("rate", rate)

            # 设置音量
            volume = 1.0  # 默认音量
            self.engine.setProperty("volume", volume)

            # 保存到文件
            self.engine.save_to_file(request.text, output_file)
            self.engine.runAndWait()

            # 检查文件是否生成成功
            if not os.path.exists(output_file):
                return TTSResponse(
                    success=False,
                    request=request,
                    error_message=f"音频文件生成失败: {output_file}",
                    error_code="FILE_ERROR",
                    processing_time=time.time() - start_time,
                )

            logger.success(f"pyttsx3合成完成: {output_file}")

            # 创建简单字幕（如果需要）
            subtitle_maker = None
            if request.generate_subtitles:
                duration = self._get_audio_duration(output_file)
                subtitle_maker = SubtitleMaker()
                segment = AudioSegment(
                    start_time=0.0,
                    end_time=duration,
                    text=request.text,
                    voice_name=request.voice_name or self.default_voice,
                )
                subtitle_maker.add_segment(segment)

            # 获取音频时长
            duration = self._get_audio_duration(output_file)

            return TTSResponse(
                success=True,
                request=request,
                audio_file=output_file,
                subtitle_maker=subtitle_maker,
                duration=duration,
                voice_used=request.voice_name or self.default_voice,
                processing_time=time.time() - start_time,
                engine_info=self.get_engine_info(),
            )

        except Exception as e:
            logger.error(f"pyttsx3 TTS失败: {str(e)}")
            return TTSResponse(
                success=False,
                request=request,
                error_message=str(e),
                error_code="PYTTSX3_ERROR",
                processing_time=time.time() - start_time,
            )

    def list_voices(self, language: Optional[str] = None) -> List[VoiceInfo]:
        """获取可用的语音列表

        Args:
            language: 语言代码过滤

        Returns:
            语音信息列表
        """
        try:
            if not self.engine:
                self._init_engine()

            voices = self.engine.getProperty("voices")
            if not voices:
                return []

            result = []
            for i, voice in enumerate(voices):
                voice_languages = getattr(voice, "languages", [])

                # 语言过滤
                if language:
                    if not any(lang.startswith(language) for lang in voice_languages):
                        continue

                # 解析语言信息
                primary_language = voice_languages[0] if voice_languages else "unknown"

                voice_info = VoiceInfo(
                    name=voice.id,
                    display_name=voice.name,
                    language=primary_language,
                    gender=getattr(voice, "gender", "unknown").lower(),
                    region="unknown",
                    engine="pyttsx3",
                    sample_rate=22050,  # pyttsx3默认采样率
                    quality="medium",
                    metadata={
                        "index": i,
                        "languages": voice_languages,
                        "age": getattr(voice, "age", "unknown"),
                    },
                )
                result.append(voice_info)

            return result

        except Exception as e:
            logger.error(f"获取pyttsx3语音列表失败: {str(e)}")
            return []

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
            file_size = os.path.getsize(audio_file)
            # WAV文件大约44KB/s (22kHz, 16bit, mono)
            return file_size / 44000
        except Exception:
            return 0.0

    def get_engine_info(self) -> dict:
        """获取引擎信息"""
        return {
            "engine_name": "Pyttsx3TTS",
            "version": "1.0",
            "default_voice": self.default_voice,
            "supported_formats": ["wav"],
            "max_text_length": 10000,
            "supports_ssml": False,
            "supports_subtitles": True,  # 简单字幕支持
            "platform_dependent": True,
        }

    def __del__(self):
        """析构函数，清理资源"""
        if hasattr(self, "engine") and self.engine:
            try:
                self.engine.stop()
            except Exception:
                pass
