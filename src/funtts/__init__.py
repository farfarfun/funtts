from .base import BaseTTS
from .models import SubtitleMaker, VoiceInfo, TTSRequest, TTSResponse, AudioSegment
from .factory import TTSFactory, TTSEngine
from .config import TTSConfig, get_config
from .utils import merge_audio_files, merge_subtitle_makers, merge_tts_responses

# 导入各个TTS引擎（可选，按需导入）
try:
    from funtts.tts.edge import EdgeTTS
except ImportError:
    EdgeTTS = None

try:
    from funtts.tts.azure import AzureTTS
except ImportError:
    AzureTTS = None

try:
    from funtts.tts.espeak import EspeakTTS
except ImportError:
    EspeakTTS = None

try:
    from funtts.tts.pyttsx3 import Pyttsx3TTS
except ImportError:
    Pyttsx3TTS = None

# Coqui TTS暂时注释掉，因为对Python版本有严格要求
# try:
#     from funtts.tts.coqui import CoquiTTS
# except ImportError:
#     CoquiTTS = None
CoquiTTS = None

try:
    from funtts.tts.bark import BarkTTS
except ImportError:
    BarkTTS = None

try:
    from funtts.tts.tortoise import TortoiseTTS
except ImportError:
    TortoiseTTS = None

try:
    from funtts.tts.indextts2 import IndexTTS2
except ImportError:
    IndexTTS2 = None

try:
    from funtts.tts.kitten import KittenTTS
except ImportError:
    KittenTTS = None

__all__ = [
    "BaseTTS",
    "TTSFactory",
    "TTSEngine",
    "TTSConfig",
    "get_config",
    "EdgeTTS",
    "AzureTTS",
    "EspeakTTS",
    "Pyttsx3TTS",
    "CoquiTTS",
    "BarkTTS",
    "TortoiseTTS",
    "IndexTTS2",
    "KittenTTS",
    "create_tts",
    "get_available_engines",
    "merge_audio_files",
    "merge_subtitle_makers",
    "merge_tts_responses",
]


# 便捷函数
def create_tts(engine_name=None, voice_name=None, config=None, **kwargs):
    """创建TTS实例的便捷函数

    Args:
        engine_name: TTS引擎名称，默认使用配置中的默认引擎
        voice_name: 语音名称，默认使用配置中的默认语音
        config: 配置字典
        **kwargs: 其他参数

    Returns:
        TTS实例
    """
    global_config = get_config()

    if engine_name is None:
        engine_name = global_config.get_default_engine()

    if voice_name is None:
        voice_name = global_config.get_default_voice()

    if config is None:
        config = global_config.get_engine_config(engine_name)

    return TTSFactory.create_tts(engine_name, voice_name, config, **kwargs)


def get_available_engines():
    """获取可用的TTS引擎列表

    Returns:
        引擎名称列表
    """
    return TTSFactory.get_available_engines()
