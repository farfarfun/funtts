"""
eSpeak TTS引擎封装
eSpeak是一个开源的语音合成器，支持多种语言
"""

import os
import subprocess
import tempfile
import time
from typing import List, Dict, Any, Optional

from funtts.base import BaseTTS
from funtts.base.models import TTSRequest, TTSResponse, AudioSegment, SubtitleMaker
from funutil import getLogger

logger = getLogger("funtts.espeak")


class EspeakTTS(BaseTTS):
    """eSpeak TTS引擎实现"""

    def __init__(self, voice_name: str = "zh", *args, **kwargs):
        """初始化eSpeak TTS

        Args:
            voice_name: 语音名称，默认为中文
        """
        super().__init__(voice_name, *args, **kwargs)
        self.espeak_path = self._find_espeak_executable()

    def _find_espeak_executable(self) -> str:
        """查找eSpeak可执行文件路径"""
        possible_paths = [
            "espeak",
            "/usr/bin/espeak",
            "/usr/local/bin/espeak",
            "/opt/homebrew/bin/espeak",
        ]

        for path in possible_paths:
            try:
                result = subprocess.run(
                    [path, "--version"], capture_output=True, text=True, timeout=5
                )
                if result.returncode == 0:
                    logger.info(f"找到eSpeak: {path}")
                    return path
            except (subprocess.TimeoutExpired, FileNotFoundError):
                continue

        raise RuntimeError("未找到eSpeak可执行文件，请确保已安装eSpeak")

    def synthesize(self, request: TTSRequest) -> TTSResponse:
        """使用eSpeak进行语音合成

        Args:
            request: TTS请求对象

        Returns:
            TTS响应对象
        """
        start_time = time.time()

        try:
            # 生成临时文件
            if not request.output_file:
                temp_file = tempfile.mktemp(suffix=f".{request.output_format}")
            else:
                temp_file = request.output_file

            # 计算eSpeak的速度参数 (80-450 wpm)
            speed = int(150 * request.voice_rate)  # 默认150 wpm
            speed = max(80, min(450, speed))

            # 构建eSpeak命令
            cmd = [
                self.espeak_path,
                "-v",
                request.voice_name or self.default_voice,  # 语音
                "-s",
                str(speed),  # 速度
                "-w",
                temp_file,  # 输出文件
                request.text,  # 文本
            ]

            # 执行eSpeak命令
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)

            if result.returncode != 0:
                return TTSResponse(
                    success=False,
                    request=request,
                    error_message=f"eSpeak执行失败: {result.stderr}",
                    error_code="ESPEAK_ERROR",
                    processing_time=time.time() - start_time,
                )

            # 检查输出文件是否存在
            if not os.path.exists(temp_file):
                return TTSResponse(
                    success=False,
                    request=request,
                    error_message=f"音频文件生成失败: {temp_file}",
                    error_code="FILE_ERROR",
                    processing_time=time.time() - start_time,
                )

            logger.info(f"eSpeak合成完成: {temp_file}")

            # 创建字幕（如果需要）
            subtitle_maker = None
            if request.generate_subtitles:
                # eSpeak不支持时间戳，创建简单字幕
                audio_duration = self._get_audio_duration(temp_file)
                subtitle_maker = SubtitleMaker()
                subtitle_maker.add_segment(
                    AudioSegment(
                        text=request.text,
                        start_time=0.0,
                        end_time=audio_duration,
                        duration=audio_duration,
                    )
                )

            return TTSResponse(
                success=True,
                request=request,
                audio_file=temp_file,
                subtitle_maker=subtitle_maker,
                processing_time=time.time() - start_time,
                engine_info=self.get_engine_info(),
            )

        except subprocess.TimeoutExpired:
            return TTSResponse(
                success=False,
                request=request,
                error_message="eSpeak执行超时",
                error_code="TIMEOUT_ERROR",
                processing_time=time.time() - start_time,
            )
        except Exception as e:
            logger.error(f"eSpeak TTS失败: {str(e)}")
            return TTSResponse(
                success=False,
                request=request,
                error_message=str(e),
                error_code="UNKNOWN_ERROR",
                processing_time=time.time() - start_time,
            )

    def _get_audio_duration(self, audio_file: str) -> float:
        """获取音频文件时长"""
        try:
            # 使用ffprobe获取音频时长
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

        # 如果ffprobe不可用，返回估算值
        file_size = os.path.getsize(audio_file)
        # 粗略估算：16kHz WAV，16位，单声道 = 32KB/s
        return file_size / 32000

    def get_available_voices(
        self, language: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """获取可用的语音列表

        Args:
            language: 语言代码（可选）

        Returns:
            语音信息列表
        """
        try:
            result = subprocess.run(
                [self.espeak_path, "--voices"],
                capture_output=True,
                text=True,
                timeout=10,
            )

            if result.returncode != 0:
                logger.error(f"获取语音列表失败: {result.stderr}")
                return []

            voices = []
            lines = result.stdout.strip().split("\n")[1:]  # 跳过标题行

            for line in lines:
                if not line.strip():
                    continue

                parts = line.split()
                if len(parts) >= 4:
                    voice_info = {
                        "name": parts[1],
                        "language": parts[1],
                        "gender": parts[2] if len(parts) > 2 else "unknown",
                        "age": parts[3] if len(parts) > 3 else "unknown",
                        "description": " ".join(parts[4:]) if len(parts) > 4 else "",
                    }

                    # 语言过滤
                    if language and not voice_info["language"].startswith(language):
                        continue

                    voices.append(voice_info)

            return voices

        except Exception as e:
            logger.error(f"获取eSpeak语音列表失败: {str(e)}")
            return []

    def is_voice_available(self, voice_name: str) -> bool:
        """检查指定语音是否可用

        Args:
            voice_name: 语音名称

        Returns:
            是否可用
        """
        voices = self.get_available_voices()
        return any(voice["name"] == voice_name for voice in voices)

    def validate_config(self) -> bool:
        """验证配置是否有效

        Returns:
            配置是否有效
        """
        try:
            # 检查eSpeak是否可用
            result = subprocess.run(
                [self.espeak_path, "--version"], capture_output=True, timeout=5
            )
            return result.returncode == 0
        except Exception:
            return False
