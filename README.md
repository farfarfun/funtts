# FunTTS - 统一TTS接口库

FunTTS是一个Python文本转语音(TTS)库，提供统一的接口来无缝切换不同的开源TTS引擎。通过简单的配置，你可以在多个TTS引擎之间轻松切换，而无需修改代码。

## 特性

- 🎯 **统一接口**: 所有TTS引擎使用相同的API接口
- 🔄 **无缝切换**: 通过配置轻松切换不同的TTS引擎
- 🎵 **多引擎支持**: 支持Edge TTS、Azure TTS、eSpeak、pyttsx3等
- ⚙️ **灵活配置**: 支持全局配置和引擎特定配置
- 📝 **字幕生成**: 支持自动生成SRT字幕文件
- 🌍 **多语言支持**: 支持多种语言和语音

## 支持的TTS引擎

| 引擎 | 状态 | 字幕支持 | 描述 |
|------|------|----------|------|
| Edge TTS | ✅ | ✅ | 微软Edge浏览器的TTS引擎，免费且高质量 |
| Azure TTS | ✅ | ✅ | 微软Azure认知服务TTS，需要API密钥 |
| eSpeak | ✅ | ❌ | 开源的多语言语音合成器 |
| pyttsx3 | ✅ | ❌ | 跨平台的Python TTS库 |

## 安装

```bash
pip install funtts
```

### 可选依赖

根据需要安装特定TTS引擎的依赖：

```bash
# Edge TTS (推荐)
pip install edge-tts

# Azure TTS
pip install azure-cognitiveservices-speech

# eSpeak (需要系统安装eSpeak)
# Ubuntu/Debian: sudo apt-get install espeak
# macOS: brew install espeak
# Windows: 下载并安装eSpeak

# pyttsx3
pip install pyttsx3
```

## 快速开始

### 基本使用

```python
from funtts import create_tts

# 使用默认配置创建TTS实例
tts = create_tts()

# 生成语音
tts.create_tts(
    text="你好，这是一个TTS测试。",
    voice_rate=1.0,
    voice_file="output.wav",
    subtitle_file="output.srt"  # 可选，生成字幕文件
)
```

### 指定TTS引擎

```python
from funtts import TTSFactory

# 使用Edge TTS
edge_tts = TTSFactory.create_tts(
    engine_name="edge",
    voice_name="zh-CN-XiaoxiaoNeural"
)

# 使用eSpeak
espeak_tts = TTSFactory.create_tts(
    engine_name="espeak", 
    voice_name="zh"
)

# 使用pyttsx3
pyttsx3_tts = TTSFactory.create_tts(
    engine_name="pyttsx3",
    voice_name="0"  # 使用第一个可用语音
)
```

### 配置管理

```python
from funtts import get_config

# 获取全局配置
config = get_config()

# 设置默认引擎
config.set_default_engine("edge")
config.set_default_voice("zh-CN-XiaoxiaoNeural")
config.set_default_rate(1.2)

# 设置引擎特定配置
config.set_engine_config("azure", {
    "subscription_key": "your-api-key",
    "region": "eastus"
})

# 保存配置
config.save_config()
```

### 获取可用语音

```python
from funtts import TTSFactory

# 创建TTS实例
tts = TTSFactory.create_tts("edge", "zh-CN-XiaoxiaoNeural")

# 获取所有可用语音
voices = tts.get_available_voices()

# 获取中文语音
chinese_voices = tts.get_available_voices(language="zh-CN")

# 检查语音是否可用
is_available = tts.is_voice_available("zh-CN-XiaoxiaoNeural")
```

## 高级用法

### 工厂模式

```python
from funtts import TTSFactory, get_available_engines

# 查看所有可用引擎
engines = get_available_engines()
print(f"可用引擎: {engines}")

# 批量创建不同引擎的实例
tts_instances = {}
for engine in engines:
    try:
        tts_instances[engine] = TTSFactory.create_tts(
            engine_name=engine,
            voice_name="default"
        )
    except Exception as e:
        print(f"创建{engine}引擎失败: {e}")
```

### 自定义配置

```python
from funtts import TTSFactory

# 使用自定义配置
custom_config = {
    "volume": 0.8,
    "pitch": 1.1
}

tts = TTSFactory.create_tts(
    engine_name="pyttsx3",
    voice_name="0",
    config=custom_config
)
```

### 批量处理

```python
from funtts import create_tts
import os

# 批量处理文本文件
texts = [
    "第一段文本内容",
    "第二段文本内容", 
    "第三段文本内容"
]

tts = create_tts(engine_name="edge")

for i, text in enumerate(texts):
    audio_file = f"output_{i+1}.wav"
    subtitle_file = f"output_{i+1}.srt"
    
    tts.create_tts(
        text=text,
        voice_rate=1.0,
        voice_file=audio_file,
        subtitle_file=subtitle_file
    )
    
    print(f"生成完成: {audio_file}")
```

## 配置文件

FunTTS使用JSON格式的配置文件，默认位置为 `~/.funtts/config.json`：

```json
{
  "default_engine": "edge",
  "default_voice": "zh-CN-XiaoxiaoNeural",
  "default_rate": 1.0,
  "engines": {
    "edge": {
      "enabled": true,
      "config": {}
    },
    "azure": {
      "enabled": true,
      "config": {
        "subscription_key": "",
        "region": "eastus"
      }
    },
    "espeak": {
      "enabled": true,
      "config": {
        "executable_path": "espeak"
      }
    },
    "pyttsx3": {
      "enabled": true,
      "config": {
        "volume": 1.0
      }
    }
  }
}
```

## 示例

查看 `examples/` 目录获取更多使用示例：

- `basic_usage.py` - 基本使用示例
- `advanced_usage.py` - 高级功能示例
- `batch_processing.py` - 批量处理示例

## 开发

### 添加新的TTS引擎

1. 继承 `BaseTTS` 基类
2. 实现必要的抽象方法
3. 在工厂类中注册新引擎

```python
from funtts.base import BaseTTS
from funtts.factory import TTSFactory

class MyCustomTTS(BaseTTS):
    def _tts(self, text, voice_rate, voice_file, *args, **kwargs):
        # 实现TTS逻辑
        pass
    
    def get_available_voices(self, language=None):
        # 返回可用语音列表
        pass
    
    def is_voice_available(self, voice_name):
        # 检查语音是否可用
        pass

# 注册新引擎
TTSFactory.register_engine("mycustom", MyCustomTTS)
```

## 许可证

MIT License

## 贡献

欢迎提交Issue和Pull Request！