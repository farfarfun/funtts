# Edge TTS引擎

## 概述

Edge TTS是基于微软Edge浏览器的免费高质量文本转语音引擎。它提供了神经网络语音合成技术，支持多种语言和自然的语音效果，无需API密钥即可使用。

## 特性

- ✅ **免费使用** - 无需API密钥或付费订阅
- ✅ **高质量语音** - 基于神经网络的自然语音合成
- ✅ **多语言支持** - 支持40+种语言和200+种语音
- ✅ **SSML支持** - 支持语音合成标记语言
- ✅ **字幕生成** - 自动生成时间同步字幕
- ✅ **语音调节** - 支持语音速率调节
- ✅ **流式处理** - 支持音频流式生成
- ❌ **商业使用限制** - 可能存在使用条款限制

## 依赖要求

### Python包依赖

```bash
pip install edge-tts>=6.1.0
```

### 系统依赖

- **可选**: FFmpeg（用于音频时长检测）
  ```bash
  # Ubuntu/Debian
  sudo apt-get install ffmpeg
  
  # macOS
  brew install ffmpeg
  
  # Windows
  # 从 https://ffmpeg.org/download.html 下载安装
  ```

## 配置说明

### 基本配置

Edge TTS无需特殊配置，开箱即用：

```python
# 无需配置，直接使用
config = {}
```

### 高级配置

可以通过TTSRequest参数进行细粒度控制：

```python
from funtts.models import TTSRequest

request = TTSRequest(
    text="你好，世界！",
    voice_name="zh-CN-XiaoxiaoNeural",  # 指定语音
    voice_rate=1.2,                      # 语音速率 (0.5-2.0)
    output_format="wav",                 # 输出格式
    generate_subtitles=True,             # 生成字幕
    subtitle_format="srt"                # 字幕格式
)
```

## 使用示例

### 基本使用

```python
from funtts import TTSFactory, TTSRequest

# 创建引擎实例
tts = TTSFactory.create_tts("edge", "zh-CN-XiaoxiaoNeural")

# 合成语音
request = TTSRequest(
    text="欢迎使用FunTTS Edge引擎！",
    voice_name="zh-CN-XiaoxiaoNeural",
    output_file="output.wav"
)
response = tts.synthesize(request)

if response.success:
    print(f"✅ 合成成功: {response.audio_file}")
    print(f"⏱️ 音频时长: {response.duration:.2f}秒")
else:
    print(f"❌ 合成失败: {response.error_message}")
```

### 带字幕生成

```python
from funtts import TTSFactory, TTSRequest

tts = TTSFactory.create_tts("edge", "zh-CN-XiaoxiaoNeural")

request = TTSRequest(
    text="这是一个带字幕的语音合成示例。",
    voice_name="zh-CN-XiaoxiaoNeural",
    output_file="demo.wav",
    generate_subtitles=True,
    subtitle_format="srt"
)

response = tts.synthesize(request)
if response.success:
    print(f"🎵 音频文件: {response.audio_file}")
    print(f"📝 SRT字幕: {response.subtitle_file}")
    print(f"🎯 FRT字幕: {response.frt_subtitle_file}")
```

### 多语言语音

```python
# 中文语音
chinese_request = TTSRequest(
    text="你好，我是中文语音。",
    voice_name="zh-CN-XiaoxiaoNeural",
    output_file="chinese.wav"
)

# 英文语音
english_request = TTSRequest(
    text="Hello, I am an English voice.",
    voice_name="en-US-AriaNeural",
    output_file="english.wav"
)

# 日文语音
japanese_request = TTSRequest(
    text="こんにちは、私は日本語の音声です。",
    voice_name="ja-JP-NanamiNeural",
    output_file="japanese.wav"
)
```

### 语音速率调节

```python
# 慢速语音
slow_request = TTSRequest(
    text="这是慢速语音示例。",
    voice_name="zh-CN-XiaoxiaoNeural",
    voice_rate=0.7,  # 70%速度
    output_file="slow.wav"
)

# 快速语音
fast_request = TTSRequest(
    text="这是快速语音示例。",
    voice_name="zh-CN-XiaoxiaoNeural",
    voice_rate=1.5,  # 150%速度
    output_file="fast.wav"
)
```

## 可用语音

### 中文语音（部分）

| 语音名称 | 显示名称 | 性别 | 风格 |
|---------|---------|------|------|
| zh-CN-XiaoxiaoNeural | 晓晓 | 女性 | 通用 |
| zh-CN-YunxiNeural | 云希 | 男性 | 通用 |
| zh-CN-YunyangNeural | 云扬 | 男性 | 新闻播报 |
| zh-CN-XiaoyiNeural | 晓伊 | 女性 | 通用 |
| zh-CN-YunjianNeural | 云健 | 男性 | 体育解说 |
| zh-CN-XiaochenNeural | 晓辰 | 女性 | 通用 |
| zh-CN-XiaohanNeural | 晓涵 | 女性 | 通用 |
| zh-CN-XiaomengNeural | 晓梦 | 女性 | 通用 |
| zh-CN-XiaomoNeural | 晓墨 | 女性 | 通用 |
| zh-CN-XiaoqiuNeural | 晓秋 | 女性 | 通用 |

### 英文语音（部分）

| 语音名称 | 显示名称 | 性别 | 地区 |
|---------|---------|------|------|
| en-US-AriaNeural | Aria | 女性 | 美国 |
| en-US-JennyNeural | Jenny | 女性 | 美国 |
| en-US-GuyNeural | Guy | 男性 | 美国 |
| en-GB-SoniaNeural | Sonia | 女性 | 英国 |
| en-AU-NatashaNeural | Natasha | 女性 | 澳大利亚 |

### 获取完整语音列表

```python
# 获取所有语音
voices = tts.list_voices()
print(f"共有 {len(voices)} 个语音可用")

# 获取中文语音
chinese_voices = tts.list_voices(language="zh-CN")
for voice in chinese_voices:
    print(f"🎤 {voice.display_name} ({voice.name}) - {voice.gender}")

# 获取英文语音
english_voices = tts.list_voices(language="en-US")
for voice in english_voices:
    print(f"🎤 {voice.display_name} ({voice.name}) - {voice.gender}")
```

## 限制说明

- **文本长度**: 单次合成最大10,000字符
- **语音速率**: 支持0.5x到2.0x速度调节
- **网络依赖**: 需要互联网连接访问微软服务
- **使用条款**: 遵守微软Edge TTS使用条款
- **商业使用**: 商业使用可能需要额外授权

## 故障排除

### 常见问题

**Q: 提示"edge-tts包未安装"**
```bash
A: 安装依赖包
pip install edge-tts>=6.1.0
```

**Q: 合成失败，提示网络错误**
```
A: 检查网络连接，确保可以访问微软服务
- 检查防火墙设置
- 尝试使用代理
- 检查DNS设置
```

**Q: 某些语音不可用**
```
A: 语音可用性可能会变化
- 使用 tts.list_voices() 获取当前可用语音
- 选择其他相似语音作为替代
```

**Q: 音频质量不佳**
```
A: 尝试以下优化
- 使用Neural语音（名称包含"Neural"）
- 调整语音速率到合适范围
- 检查文本格式和标点符号
```

**Q: 字幕时间不准确**
```
A: Edge TTS提供词级时间戳
- 确保使用generate_subtitles=True
- 检查文本中的标点符号
- 长文本可能需要分段处理
```

### 性能优化

```python
# 1. 批量处理优化
texts = ["文本1", "文本2", "文本3"]
for i, text in enumerate(texts):
    request = TTSRequest(
        text=text,
        voice_name="zh-CN-XiaoxiaoNeural",
        output_file=f"batch_{i}.wav"
    )
    response = tts.synthesize(request)

# 2. 重用TTS实例
tts = TTSFactory.create_tts("edge", "zh-CN-XiaoxiaoNeural")
# 多次使用同一个实例，避免重复初始化

# 3. 合理设置语音速率
# 过快或过慢的语音速率可能影响质量
request.voice_rate = 1.2  # 推荐范围: 0.8-1.5
```

## 技术细节

### 音频格式
- **默认格式**: WAV (PCM 24kHz 16-bit)
- **支持格式**: WAV, MP3
- **采样率**: 24000 Hz
- **声道**: 单声道

### 字幕格式
- **SRT**: 标准字幕格式
- **VTT**: WebVTT格式
- **FRT**: FunTTS扩展格式（包含完整元数据）

### API限制
- **并发限制**: 建议控制并发请求数量
- **频率限制**: 避免过于频繁的请求
- **文本限制**: 单次请求不超过10,000字符

## 相关链接

- **官方网站**: [Microsoft Edge](https://www.microsoft.com/edge)
- **Edge TTS GitHub**: [https://github.com/rany2/edge-tts](https://github.com/rany2/edge-tts)
- **Microsoft Speech服务**: [https://azure.microsoft.com/services/cognitive-services/speech-services/](https://azure.microsoft.com/services/cognitive-services/speech-services/)
- **Edge TTS PyPI**: [https://pypi.org/project/edge-tts/](https://pypi.org/project/edge-tts/)
- **Edge TTS文档**: [https://github.com/rany2/edge-tts/blob/master/README.md](https://github.com/rany2/edge-tts/blob/master/README.md)

## 更新日志

### v1.0.0
- 初始版本
- 支持基本语音合成
- 支持字幕生成
- 支持多语言语音
- 支持语音速率调节
