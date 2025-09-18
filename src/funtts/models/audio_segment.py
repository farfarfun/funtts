"""
音频片段数据结构
支持多角色场景的音频片段定义
"""

from typing import Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class AudioSegment:
    """音频片段数据结构 - 支持多角色场景"""

    start_time: float  # 开始时间（秒）
    end_time: float  # 结束时间（秒）
    text: str  # 对应的文本

    # 角色信息
    speaker_id: Optional[str] = None  # 说话者ID（如: "narrator", "character1"）
    speaker_name: Optional[str] = None  # 说话者名称（如: "旁白", "小明"）
    voice_name: Optional[str] = None  # 使用的语音名称

    # 样式信息
    emotion: Optional[str] = None  # 情感（如: "neutral", "happy", "sad"）
    style: Optional[str] = None  # 风格（如: "formal", "casual"）

    # 元数据
    segment_id: Optional[str] = None  # 片段唯一标识
    metadata: Dict[str, Any] = None  # 额外元数据

    def __post_init__(self):
        """初始化后处理"""
        if self.metadata is None:
            self.metadata = {}

    @property
    def duration(self) -> float:
        """获取片段时长"""
        return self.end_time - self.start_time

    def get_display_speaker(self) -> str:
        """获取显示用的说话者名称"""
        return self.speaker_name or self.speaker_id or "未知说话者"

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "start_time": self.start_time,
            "end_time": self.end_time,
            "text": self.text,
            "duration": self.duration,
            "speaker_id": self.speaker_id,
            "speaker_name": self.speaker_name,
            "voice_name": self.voice_name,
            "emotion": self.emotion,
            "style": self.style,
            "segment_id": self.segment_id,
            "metadata": self.metadata,
            "display_speaker": self.get_display_speaker(),
        }
