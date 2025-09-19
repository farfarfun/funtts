# Coqui TTS引擎

Coqui TTS是一个功能强大的深度学习文本转语音工具包，支持多种先进的TTS模型架构。该引擎提供高质量的语音合成、语音克隆功能，并支持多种语言和自定义模型训练。

## 概述

Coqui TTS（原Mozilla TTS）是目前最受欢迎的开源TTS工具包之一，由Coqui AI开发维护。它集成了多种最先进的TTS模型，包括Tacotron、VITS、GlowTTS、Bark等，为用户提供了丰富的选择和强大的功能。

## 主要特性

- **🎯 多模型支持**: 集成Tacotron、VITS、GlowTTS、Bark等多种TTS架构
- **🎭 语音克隆**: 支持零样本和少样本语音克隆
- **🌍 多语言支持**: 支持17+种语言的高质量语音合成
- **🔧 可训练**: 支持自定义数据集训练专属模型
- **⚡ 高性能**: 优化的推理速度，支持实时合成
- **🎵 音质优秀**: 提供接近人声的自然语音效果
- **📱 易于集成**: 简单的API接口，易于集成到应用中

## 依赖要求

### Python版本
- Python >= 3.8, < 3.12

### 核心依赖
```bash
TTS>=0.22.0
torch>=1.9.0
torchaudio>=0.9.0
numpy>=1.20.0
librosa>=0.9.0
soundfile>=0.10.0
```

### 可选依赖
```bash
# GPU加速支持
torch>=1.9.0+cu118  # CUDA版本

# 音频处理增强
espeak-ng  # 用于某些模型的音素处理
```

## 安装

### 基础安装
```bash
# 安装FunTTS和Coqui TTS支持
pip install funtts-plus[coqui]
```

### 完整安装
```bash
# 安装所有TTS引擎
pip install funtts-plus[all]
```

### 手动安装依赖
```bash
# 安装Coqui TTS
pip install TTS

# 安装PyTorch (根据你的CUDA版本选择)
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu118

# 安装其他依赖
pip install librosa soundfile numpy
```

### 系统依赖
```bash
# Ubuntu/Debian
sudo apt-get install espeak-ng

# macOS
brew install espeak

# Windows
# 下载并安装 eSpeak NG from: https://github.com/espeak-ng/espeak-ng/releases
```

## 配置

### 环境变量
```bash
# 可选：设置模型缓存目录
export COQUI_CACHE_DIR="/path/to/cache"

# 可选：设置默认设备
export COQUI_DEVICE="cuda"  # 或 "cpu"
```

### 配置参数

| 参数 | 类型 | 默认值 | 描述 |
|------|------|--------|------|
| `model_name` | str | "tts_models/en/ljspeech/tacotron2-DDC" | 使用的TTS模型 |
| `device` | str | "auto" | 计算设备 (cpu/cuda/auto) |
| `sample_rate` | int | 22050 | 音频采样率 |
| `vocoder_name` | str | None | 声码器名称 |
| `speaker_wav` | str | None | 语音克隆参考音频 |
| `language` | str | "en" | 默认语言 |
| `emotion` | str | "neutral" | 默认情感 |
| `speed` | float | 1.0 | 语速倍数 |

## 使用示例

### 基础使用
```python
from funtts.tts.coqui import CoquiTTS
from funtts.models import TTSRequest

# 初始化引擎
tts = CoquiTTS()

# 创建合成请求
request = TTSRequest(
    text="Hello, this is Coqui TTS speaking!",
    voice_name="default",
    output_dir="./output"
)

# 执行语音合成
response = tts.synthesize(request)
print(f"音频文件: {response.audio_file}")
print(f"音频时长: {response.duration:.2f}秒")
```

### 使用特定模型
```python
# 使用VITS模型
tts = CoquiTTS(model_name="tts_models/en/ljspeech/vits")

# 使用多语言模型
tts = CoquiTTS(model_name="tts_models/multilingual/multi-dataset/your_tts")

# 查看可用模型
available_models = tts.list_available_models()
print("可用模型:")
for model in available_models[:10]:  # 显示前10个
    print(f"  - {model}")
```

### 多说话人模型
```python
# 使用多说话人模型
tts = CoquiTTS(model_name="tts_models/en/vctk/vits")

# 获取可用说话人
voices = tts.list_voices()
for voice in voices[:5]:  # 显示前5个
    print(f"{voice.name}: {voice.display_name}")

# 指定说话人合成
request = TTSRequest(
    text="This is a multi-speaker TTS model.",
    voice_name="p225",  # VCTK数据集中的说话人ID
    output_dir="./output"
)

response = tts.synthesize(request)
```

### 语音克隆
```python
# 使用语音克隆功能
tts = CoquiTTS(model_name="tts_models/multilingual/multi-dataset/your_tts")

# 方法1: 通过TTSRequest
request = TTSRequest(
    text="This is voice cloning with Coqui TTS.",
    speaker_wav="path/to/reference_voice.wav",  # 参考语音文件
    language="en",
    output_dir="./output"
)

response = tts.synthesize(request)

# 方法2: 直接调用克隆方法
cloned_audio = tts.clone_voice(
    text="Hello, this is my cloned voice!",
    speaker_wav="path/to/reference_voice.wav",
    output_path="./output/cloned_voice.wav",
    language="en"
)
```

### 多语言合成
```python
# 中文合成
tts_zh = CoquiTTS(model_name="tts_models/zh-CN/baker/tacotron2-DDC-GST")

request = TTSRequest(
    text="你好，这是Coqui TTS中文语音合成。",
    output_dir="./output"
)

response = tts_zh.synthesize(request)

# 西班牙语合成
tts_es = CoquiTTS(model_name="tts_models/es/mai/tacotron2-DDC")

request = TTSRequest(
    text="Hola, esto es síntesis de voz en español.",
    output_dir="./output"
)

response = tts_es.synthesize(request)
```

### 生成字幕
```python
# 同时生成音频和字幕
request = TTSRequest(
    text="This text will be converted to speech with subtitles.",
    voice_name="default",
    subtitle_format="srt,frt",  # 生成SRT和FRT格式字幕
    output_dir="./output"
)

response = tts.synthesize(request)
print(f"音频文件: {response.audio_file}")
print(f"SRT字幕: {response.subtitle_file}")
print(f"FRT字幕: {response.frt_subtitle_file}")
```

### 批量处理
```python
texts = [
    "First sentence to synthesize.",
    "Second sentence for batch processing.",
    "Third and final sentence."
]

responses = []
for i, text in enumerate(texts):
    request = TTSRequest(
        text=text,
        voice_name="default",
        output_dir=f"./output/batch_{i}"
    )
    response = tts.synthesize(request)
    responses.append(response)

print(f"批量处理完成，生成了 {len(responses)} 个音频文件")
```

### 高级配置
```python
# 使用自定义配置初始化
tts = CoquiTTS(
    model_name="tts_models/en/ljspeech/vits",
    device="cuda",
    sample_rate=44100,
    language="en",
    emotion="happy"
)

# 获取引擎信息
info = tts.get_engine_info()
print(f"引擎: {info['name']} v{info['version']}")
print(f"当前模型: {info['model_name']}")
print(f"支持的语言: {info['supported_languages']}")
```

## 可用模型

### 英语模型
| 模型名称 | 架构 | 特点 | 适用场景 |
|----------|------|------|----------|
| tts_models/en/ljspeech/tacotron2-DDC | Tacotron2 | 经典模型，稳定可靠 | 通用英语合成 |
| tts_models/en/ljspeech/vits | VITS | 快速高质量 | 实时应用 |
| tts_models/en/vctk/vits | VITS | 多说话人 | 需要不同声音 |
| tts_models/en/ljspeech/glow-tts | GlowTTS | 并行生成 | 快速合成 |

### 多语言模型
| 模型名称 | 支持语言 | 特点 |
|----------|----------|------|
| tts_models/multilingual/multi-dataset/your_tts | 17种语言 | 语音克隆 |
| tts_models/multilingual/multi-dataset/bark | 多语言 | 支持音效 |

### 中文模型
| 模型名称 | 特点 | 数据集 |
|----------|------|--------|
| tts_models/zh-CN/baker/tacotron2-DDC-GST | 情感控制 | Baker数据集 |

### 获取完整模型列表
```python
# 获取所有可用模型
models = tts.list_available_models()

# 按语言筛选
en_models = [m for m in models if '/en/' in m]
zh_models = [m for m in models if '/zh/' in m]

print(f"英语模型数量: {len(en_models)}")
print(f"中文模型数量: {len(zh_models)}")
```

## 性能优化

### GPU加速
```python
# 使用GPU加速
tts = CoquiTTS(
    model_name="tts_models/en/ljspeech/vits",
    device="cuda"
)

# 检查GPU状态
import torch
if torch.cuda.is_available():
    print(f"GPU设备: {torch.cuda.get_device_name()}")
    print(f"GPU内存: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f}GB")
```

### 模型选择建议
```python
# 实时应用 - 选择VITS模型
tts_realtime = CoquiTTS(model_name="tts_models/en/ljspeech/vits")

# 高质量应用 - 选择Tacotron2模型
tts_quality = CoquiTTS(model_name="tts_models/en/ljspeech/tacotron2-DDC")

# 语音克隆 - 选择YourTTS模型
tts_clone = CoquiTTS(model_name="tts_models/multilingual/multi-dataset/your_tts")
```

### 内存优化
```python
# 对于内存受限的环境
tts = CoquiTTS(
    model_name="tts_models/en/ljspeech/speedy-speech",  # 轻量级模型
    device="cpu"
)
```

## 限制说明

### 文本长度
- **单次合成**: 建议不超过500个单词
- **长文本**: 建议分段处理后合并

### 硬件要求
- **最低配置**: 4GB RAM, CPU
- **推荐配置**: 8GB+ RAM, GPU (6GB+ VRAM)
- **GPU支持**: NVIDIA GPU with CUDA 11.0+

### 模型限制
- 某些模型仅支持特定语言
- 语音克隆需要多语言模型
- 情感控制仅部分模型支持

## 故障排除

### 常见问题

#### 1. 模型下载失败
```bash
错误: 无法下载模型
解决: 检查网络连接，或手动下载模型到缓存目录
```

#### 2. GPU内存不足
```bash
错误: CUDA out of memory
解决: 使用CPU模式或选择更小的模型
```

#### 3. 音频质量问题
```bash
问题: 合成音频有杂音
解决: 尝试不同的模型或调整采样率
```

#### 4. 语音克隆效果差
```bash
问题: 克隆的声音不像参考音频
解决: 确保参考音频质量好，时长3-10秒，使用YourTTS模型
```

### 调试模式
```python
import logging
logging.basicConfig(level=logging.DEBUG)

# 启用详细日志
tts = CoquiTTS(model_name="tts_models/en/ljspeech/vits")
```

### 性能监控
```python
import time

start_time = time.time()
response = tts.synthesize(request)
synthesis_time = time.time() - start_time

print(f"合成耗时: {synthesis_time:.2f}秒")
print(f"音频时长: {response.duration:.2f}秒")
print(f"实时率: {response.duration/synthesis_time:.2f}x")
```

## 最佳实践

### 1. 模型选择
```python
# 根据需求选择合适的模型
def choose_model(use_case):
    if use_case == "realtime":
        return "tts_models/en/ljspeech/vits"
    elif use_case == "quality":
        return "tts_models/en/ljspeech/tacotron2-DDC"
    elif use_case == "multilingual":
        return "tts_models/multilingual/multi-dataset/your_tts"
    elif use_case == "voice_cloning":
        return "tts_models/multilingual/multi-dataset/your_tts"
    else:
        return "tts_models/en/ljspeech/vits"

model_name = choose_model("realtime")
tts = CoquiTTS(model_name=model_name)
```

### 2. 文本预处理
```python
import re

def preprocess_text(text):
    # 清理特殊字符
    text = re.sub(r'[^\w\s.,!?;:]', '', text)
    # 处理数字
    text = re.sub(r'\d+', lambda m: num2words(int(m.group())), text)
    # 规范化空格
    text = re.sub(r'\s+', ' ', text.strip())
    return text

request = TTSRequest(
    text=preprocess_text("原始文本..."),
    voice_name="default"
)
```

### 3. 错误处理
```python
def safe_synthesize(tts, request, max_retries=3):
    for attempt in range(max_retries):
        try:
            return tts.synthesize(request)
        except RuntimeError as e:
            if attempt == max_retries - 1:
                raise
            print(f"合成失败，重试 {attempt + 1}/{max_retries}: {e}")
            time.sleep(1)

# 使用方式
try:
    response = safe_synthesize(tts, request)
except Exception as e:
    print(f"最终合成失败: {e}")
```

### 4. 资源管理
```python
class TTSManager:
    def __init__(self, model_name):
        self.model_name = model_name
        self.tts = None
    
    def __enter__(self):
        self.tts = CoquiTTS(model_name=self.model_name)
        return self.tts
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        # 清理资源
        if self.tts and hasattr(self.tts, 'tts_model'):
            del self.tts.tts_model
        del self.tts

# 使用方式
with TTSManager("tts_models/en/ljspeech/vits") as tts:
    response = tts.synthesize(request)
```

## 版本历史

### v0.22.0 (当前版本)
- 支持最新的VITS和YourTTS模型
- 改进的语音克隆功能
- 优化的推理性能
- 扩展的多语言支持

### v0.21.0
- 添加Bark模型支持
- 改进的情感控制
- 新的多语言模型

### v0.20.0
- 重构的API接口
- 改进的模型管理
- 性能优化

## 相关链接

### 官方资源
- **GitHub仓库**: [https://github.com/coqui-ai/TTS](https://github.com/coqui-ai/TTS)
- **官方文档**: [https://tts.readthedocs.io/](https://tts.readthedocs.io/)
- **PyPI页面**: [https://pypi.org/project/TTS/](https://pypi.org/project/TTS/)
- **模型列表**: [https://github.com/coqui-ai/TTS/blob/dev/TTS/.models.json](https://github.com/coqui-ai/TTS/blob/dev/TTS/.models.json)

### 技术文档
- **论文集合**: [Coqui TTS Papers](https://github.com/coqui-ai/TTS#papers)
- **模型架构**: [TTS Models](https://tts.readthedocs.io/en/latest/models/)
- **训练指南**: [Training Guide](https://tts.readthedocs.io/en/latest/tutorial_for_nervous_beginners.html)

### 社区资源
- **讨论区**: [GitHub Discussions](https://github.com/coqui-ai/TTS/discussions)
- **问题反馈**: [GitHub Issues](https://github.com/coqui-ai/TTS/issues)
- **Discord社区**: [Coqui Discord](https://discord.gg/5eXr5seRrv)

### 相关项目
- **Coqui STT**: [https://github.com/coqui-ai/STT](https://github.com/coqui-ai/STT)
- **Mozilla DeepSpeech**: [https://github.com/mozilla/DeepSpeech](https://github.com/mozilla/DeepSpeech)

### 预训练模型
- **Hugging Face Models**: [https://huggingface.co/coqui](https://huggingface.co/coqui)
- **模型下载**: 模型会自动下载到 `~/.local/share/tts/`

---

如需更多帮助，请参考 [FunTTS主文档](../../README.md) 或访问 [Coqui TTS官方仓库](https://github.com/coqui-ai/TTS)。
