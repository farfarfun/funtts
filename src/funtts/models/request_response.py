"""
TTS请求和响应数据结构
统一的请求响应模型
"""

from typing import Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class TTSRequest:
    """TTS请求数据结构"""

    text: str  # 要转换的文本
    voice_name: Optional[str] = None  # 语音名称，None使用默认语音
    voice_rate: float = 1.0  # 语音速率 (0.5-2.0)
    voice_pitch: float = 1.0  # 语音音调 (0.5-2.0)
    voice_volume: float = 1.0  # 语音音量 (0.0-1.0)
    output_format: str = "wav"  # 输出格式
    sample_rate: int = 16000  # 采样率
    output_file: Optional[str] = None  # 输出文件路径，None则不保存文件
    output_dir: Optional[str] = None  # 输出目录路径，用于某些引擎
    generate_subtitles: bool = False  # 是否生成字幕
    subtitle_format: str = "srt"  # 字幕格式 (srt/vtt/frt)
    language: Optional[str] = None  # 语言代码，用于语音选择

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "text": self.text,
            "voice_name": self.voice_name,
            "voice_rate": self.voice_rate,
            "voice_pitch": self.voice_pitch,
            "voice_volume": self.voice_volume,
            "output_format": self.output_format,
            "sample_rate": self.sample_rate,
            "output_file": self.output_file,
            "output_dir": self.output_dir,
            "generate_subtitles": self.generate_subtitles,
            "subtitle_format": self.subtitle_format,
            "language": self.language,
        }

    def validate(self) -> bool:
        """验证请求参数是否有效"""
        if not self.text or not self.text.strip():
            return False
        if not (0.5 <= self.voice_rate <= 2.0):
            return False
        if not (0.5 <= self.voice_pitch <= 2.0):
            return False
        if not (0.0 <= self.voice_volume <= 1.0):
            return False
        if self.output_format not in ["wav", "mp3", "ogg", "flac"]:
            return False
        if self.subtitle_format not in ["srt", "vtt", "frt"]:
            return False
        return True


@dataclass
class TTSResponse:
    """TTS响应数据结构"""

    success: bool  # 是否成功
    request: Optional["TTSRequest"] = None  # 原始请求（用于追踪）
    audio_file: Optional[str] = None  # 音频文件路径
    subtitle_maker: Optional[Any] = None  # 字幕制作器
    subtitle_file: Optional[str] = None  # 标准格式字幕文件路径（SRT/VTT）
    frt_subtitle_file: Optional[str] = None  # FRT格式字幕文件路径
    duration: float = 0.0  # 音频时长（秒）
    voice_used: Optional[str] = None  # 实际使用的语音名称
    engine_info: Dict[str, Any] = None  # 引擎信息
    error_message: str = ""  # 错误信息
    error_code: Optional[str] = None  # 错误代码
    processing_time: float = 0.0  # 处理时间（秒）

    def __post_init__(self):
        if self.engine_info is None:
            self.engine_info = {}

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "success": self.success,
            "audio_file": self.audio_file,
            "subtitle_file": self.subtitle_file,
            "frt_subtitle_file": self.frt_subtitle_file,
            "duration": self.duration,
            "voice_used": self.voice_used,
            "error_message": self.error_message,
            "error_code": self.error_code,
            "processing_time": self.processing_time,
            "has_subtitles": self.subtitle_maker is not None
            and bool(self.subtitle_maker),
            "engine_info": self.engine_info,
        }

    def save_subtitles(self, file_path: str, format_type: str = "srt") -> bool:
        """保存字幕到文件"""
        if not self.subtitle_maker:
            return False
        try:
            self.subtitle_maker.save_to_file(file_path, format_type)
            self.subtitle_file = file_path
            return True
        except Exception:
            return False
