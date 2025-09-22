# IndexTTS2 TTS引擎

IndexTTS2是一个工业级可控制的文本转语音模型，具有高质量的语音合成能力和精确的时长控制功能。该引擎支持情感控制和自然语言指令，适用于需要高质量语音输出的应用场景。

## 概述

IndexTTS2基于先进的神经网络架构，提供了工业级的语音合成解决方案。与传统的自回归TTS模型相比，IndexTTS2能够精确控制合成语音的时长，并支持通过自然语言描述来控制语音的情感表达。

## 主要特性

- **🎯 精确时长控制**: 能够精确控制合成语音的持续时间
- **😊 情感控制**: 支持多种情感表达，如开心、悲伤、愤怒等
- **📝 自然语言指令**: 通过文本描述控制语音风格和情感
- **🌍 多语言支持**: 支持中文、英文、日文、韩文等多种语言
- **🎵 高音质**: 提供工业级的高质量语音合成
- **⚡ 高效推理**: 优化的推理速度，适合实时应用
- **🔧 灵活配置**: 支持多种参数调节和自定义配置

## 依赖要求

### Python版本
- Python >= 3.8

### 核心依赖
```bash
torch>=1.9.0
torchaudio>=0.9.0
transformers>=4.20.0
numpy>=1.20.0
soundfile>=0.10.0
```

### 可选依赖
```bash
# GPU加速支持
torch>=1.9.0+cu118  # CUDA版本
# 或
torch>=1.9.0+cpu    # CPU版本

# 音频处理增强
librosa>=0.9.0
```

## 安装

### 基础安装
```bash
# 安装FunTTS和IndexTTS2支持
pip install funtts-plus[indextts2]
```

### 完整安装
```bash
# 安装所有TTS引擎
pip install funtts-plus[all]
```

### 手动安装依赖
```bash
# 安装PyTorch (根据你的CUDA版本选择)
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu118

# 安装其他依赖
pip install transformers soundfile numpy
```

## 配置

### 环境变量
```bash
# 可选：设置模型缓存目录
export INDEXTTS2_CACHE_DIR="/path/to/cache"

# 可选：设置默认设备
export INDEXTTS2_DEVICE="cuda"  # 或 "cpu", "mps"
```

### 配置参数

| 参数 | 类型 | 默认值 | 描述 |
|------|------|--------|------|
| `model_path` | str | None | 模型路径，None时使用默认模型 |
| `device` | str | "auto" | 计算设备 (cpu/cuda/mps/auto) |
| `sample_rate` | int | 22050 | 音频采样率 |
| `temperature` | float | 1.0 | 生成温度，控制随机性 |
| `top_k` | int | 50 | Top-K采样参数 |
| `top_p` | float | 0.9 | Top-P采样参数 |
| `emotion_strength` | float | 1.0 | 情感强度 (0.0-2.0) |
| `speed_factor` | float | 1.0 | 语速倍数 (0.5-2.0) |

## 使用示例

### 基础使用
```python
from funtts.tts.indextts2 import IndexTTS2
from funtts.models import TTSRequest

# 初始化引擎
tts = IndexTTS2()

# 创建合成请求
request = TTSRequest(
    text="你好，这是IndexTTS2语音合成测试",
    voice_name="zh-CN-XiaoxiaoNeural",
    output_dir="./output"
)

# 执行语音合成
response = tts.synthesize(request)
print(f"音频文件: {response.audio_file}")
print(f"音频时长: {response.duration:.2f}秒")
```

### 情感控制
```python
from funtts.tts.indextts2 import IndexTTS2
from funtts.models import TTSRequest

# 初始化引擎，设置情感强度
tts = IndexTTS2(emotion_strength=1.5)

# 带情感的合成请求
request = TTSRequest(
    text="今天天气真好，心情特别开心！",
    voice_name="zh-CN-XiaoxiaoNeural",
    emotion="happy",  # 情感类型
    emotion_strength=1.2  # 情感强度
)

response = tts.synthesize(request)
```

### 语速控制
```python
# 调整语速
request = TTSRequest(
    text="这段话会以较快的语速播放",
    voice_name="zh-CN-YunxiNeural",
    speed=1.5  # 1.5倍速
)

response = tts.synthesize(request)
```

### 生成字幕
```python
# 同时生成音频和字幕
request = TTSRequest(
    text="这是一段需要生成字幕的文本",
    voice_name="zh-CN-XiaoxiaoNeural",
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
    "第一段文本内容",
    "第二段文本内容", 
    "第三段文本内容"
]

responses = []
for i, text in enumerate(texts):
    request = TTSRequest(
        text=text,
        voice_name="zh-CN-XiaoxiaoNeural",
        output_dir=f"./output/batch_{i}"
    )
    response = tts.synthesize(request)
    responses.append(response)
```

### 高级配置
```python
# 使用自定义配置初始化
tts = IndexTTS2(
    device="cuda",
    sample_rate=44100,
    temperature=0.8,
    top_k=40,
    top_p=0.85,
    emotion_strength=1.2,
    speed_factor=1.1
)

# 获取引擎信息
info = tts.get_engine_info()
print(f"引擎: {info['name']} v{info['version']}")
print(f"支持的语言: {info['supported_languages']}")
```

## 可用语音

### 中文语音
| 语音名称 | 显示名称 | 性别 | 描述 |
|----------|----------|------|------|
| zh-CN-XiaoxiaoNeural | 晓晓 (女声) | Female | 自然流畅，支持情感控制 |
| zh-CN-YunxiNeural | 云希 (男声) | Male | 沉稳大气，支持情感控制 |

### 英文语音
| 语音名称 | 显示名称 | 性别 | 描述 |
|----------|----------|------|------|
| en-US-AriaNeural | Aria (Female) | Female | 自然英语女声，情感丰富 |
| en-US-GuyNeural | Guy (Male) | Male | 专业英语男声，适合商务 |

### 获取完整语音列表
```python
# 获取所有可用语音
voices = tts.list_voices()
for voice in voices:
    print(f"{voice.name}: {voice.display_name} ({voice.language})")

# 按语言过滤
zh_voices = tts.list_voices(language="zh-CN")
en_voices = tts.list_voices(language="en-US")
```

## 性能优化

### GPU加速
```python
# 使用GPU加速
tts = IndexTTS2(device="cuda")

# 检查GPU可用性
import torch
if torch.cuda.is_available():
    print(f"GPU设备: {torch.cuda.get_device_name()}")
    print(f"GPU内存: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f}GB")
```

### 内存优化
```python
# 对于内存受限的环境
tts = IndexTTS2(
    device="cpu",
    # 降低采样率以节省内存
    sample_rate=16000
)
```

### 批处理优化
```python
# 批量处理时重用引擎实例
tts = IndexTTS2()

# 处理多个文本
for text in text_list:
    request = TTSRequest(text=text, voice_name="zh-CN-XiaoxiaoNeural")
    response = tts.synthesize(request)
    # 处理响应...
```

## 限制说明

### 文本长度
- **单次合成**: 建议不超过1000个字符
- **长文本**: 建议分段处理后合并

### 硬件要求
- **最低配置**: 4GB RAM, CPU
- **推荐配置**: 8GB+ RAM, GPU (4GB+ VRAM)
- **GPU支持**: NVIDIA GPU with CUDA 11.0+

### 语言支持
- 主要支持中文和英文
- 其他语言支持可能有限

## 故障排除

### 常见问题

#### 1. 模型加载失败
```bash
错误: 无法加载IndexTTS2模型
解决: 检查网络连接，确保能访问模型仓库
```

#### 2. GPU内存不足
```bash
错误: CUDA out of memory
解决: 降低batch_size或使用CPU模式
```

#### 3. 音频质量问题
```bash
问题: 合成音频质量不佳
解决: 调整temperature和采样参数
```

### 调试模式
```python
import logging
logging.basicConfig(level=logging.DEBUG)

# 启用详细日志
tts = IndexTTS2()
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

### 1. 文本预处理
```python
# 清理文本中的特殊字符
import re

def clean_text(text):
    # 移除多余空格
    text = re.sub(r'\s+', ' ', text.strip())
    # 处理标点符号
    text = re.sub(r'[^\w\s\u4e00-\u9fff，。！？；：]', '', text)
    return text

request = TTSRequest(
    text=clean_text("原始文本..."),
    voice_name="zh-CN-XiaoxiaoNeural"
)
```

### 2. 错误处理
```python
try:
    response = tts.synthesize(request)
except RuntimeError as e:
    print(f"合成失败: {e}")
    # 实施备用方案
except Exception as e:
    print(f"未知错误: {e}")
```

### 3. 资源管理
```python
# 使用上下文管理器
class TTSManager:
    def __init__(self):
        self.tts = None
    
    def __enter__(self):
        self.tts = IndexTTS2()
        return self.tts
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        # 清理资源
        if self.tts:
            del self.tts

# 使用方式
with TTSManager() as tts:
    response = tts.synthesize(request)
```

## 版本历史

### v2.0.0 (当前版本)
- 支持情感控制和自然语言指令
- 改进的时长控制精度
- 优化的推理性能
- 扩展的多语言支持

### v1.0.0
- 初始版本发布
- 基础语音合成功能
- 多语言支持

## 相关链接

### 官方资源
- **GitHub仓库**: [https://github.com/index-tts/index-tts](https://github.com/index-tts/index-tts)
- **官方组织**: [https://github.com/index-tts](https://github.com/index-tts)
- **演示页面**: [https://index-tts.github.io/index-tts2.github.io/](https://index-tts.github.io/index-tts2.github.io/)
- **论文**: [IndexTTS2: Controllable Industrial-Level Text-to-Speech](https://arxiv.org/abs/2024.xxxxx)

### 技术文档
- **模型架构**: 基于Transformer的神经网络TTS
- **训练数据**: 大规模多语言语音数据集
- **技术博客**: [IndexTTS2技术解析](https://blog.example.com/indextts2)

### 社区资源
- **讨论区**: [GitHub Discussions](https://github.com/iszhanjiawei/indexTTS2/discussions)
- **问题反馈**: [GitHub Issues](https://github.com/iszhanjiawei/indexTTS2/issues)
- **贡献指南**: [Contributing Guide](https://github.com/iszhanjiawei/indexTTS2/blob/main/CONTRIBUTING.md)

### 相关项目
- **IndexTTS v1**: [https://github.com/index-tts/index-tts](https://github.com/index-tts/index-tts)
- **其他Fork**: [https://github.com/tabortao/index-tts2](https://github.com/tabortao/index-tts2)

---

如需更多帮助，请参考 [FunTTS主文档](../../README.md) 或访问 [IndexTTS2官方仓库](https://github.com/iszhanjiawei/indexTTS2)。
