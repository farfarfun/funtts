# Azure TTS引擎

## 概述

Azure TTS是基于微软Azure认知服务的企业级文本转语音引擎。它提供了高质量的神经网络语音合成技术，支持丰富的语音选择、SSML标记、自定义语音模型和多种语言，适合商业和企业级应用。

## 特性

- ✅ **企业级质量** - 基于Azure云服务的高质量语音合成
- ✅ **丰富语音库** - 支持400+种语音和140+种语言
- ✅ **SSML支持** - 完整的语音合成标记语言支持
- ✅ **自定义语音** - 支持训练和部署自定义语音模型
- ✅ **情感和风格** - 支持多种语音情感和说话风格
- ✅ **批量处理** - 支持大规模批量语音合成
- ✅ **流式合成** - 支持实时流式语音生成
- ✅ **多格式输出** - 支持多种音频格式和质量
- ❌ **付费服务** - 需要Azure订阅和API密钥

## 依赖要求

### Python包依赖

```bash
pip install azure-cognitiveservices-speech>=1.30.0
```

### Azure服务配置

1. **创建Azure账户**
   - 访问 [Azure Portal](https://portal.azure.com/)
   - 创建免费账户或使用现有账户

2. **创建语音服务资源**
   ```bash
   # 使用Azure CLI创建资源组和语音服务
   az group create --name myResourceGroup --location eastus
   az cognitiveservices account create \
     --name mySpeechService \
     --resource-group myResourceGroup \
     --kind SpeechServices \
     --sku F0 \
     --location eastus
   ```

3. **获取API密钥和区域**
   - 在Azure Portal中找到语音服务资源
   - 复制"密钥和终结点"中的密钥和区域

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

### 环境变量配置

```bash
# 设置Azure语音服务配置
export AZURE_SPEECH_KEY="your-speech-service-key"
export AZURE_SPEECH_REGION="your-service-region"  # 如: eastus, westus2
```

### 程序化配置

```python
from funtts import TTSFactory

# 方式1: 通过参数配置
tts = TTSFactory.create_tts(
    "azure", 
    "zh-CN-XiaoxiaoNeural",
    speech_key="your-speech-service-key",
    service_region="eastus"
)

# 方式2: 通过全局配置
from funtts import get_config
config = get_config()
config.set_engine_config("azure", {
    "speech_key": "your-speech-service-key",
    "service_region": "eastus"
})
```

### 高级配置

```python
from funtts.models import TTSRequest

request = TTSRequest(
    text="你好，世界！",
    voice_name="zh-CN-XiaoxiaoNeural",
    voice_rate=1.2,                    # 语音速率
    voice_pitch=1.0,                   # 音调（通过SSML）
    voice_volume=1.0,                  # 音量（通过SSML）
    output_format="wav",               # 输出格式
    generate_subtitles=True,           # 生成字幕
    subtitle_format="srt"              # 字幕格式
)
```

## 使用示例

### 基本使用

```python
from funtts import TTSFactory, TTSRequest

# 创建引擎实例
tts = TTSFactory.create_tts(
    "azure", 
    "zh-CN-XiaoxiaoNeural",
    speech_key="your-key",
    service_region="eastus"
)

# 合成语音
request = TTSRequest(
    text="欢迎使用Azure TTS引擎！",
    voice_name="zh-CN-XiaoxiaoNeural",
    output_file="output.wav"
)
response = tts.synthesize(request)

if response.success:
    print(f"✅ 合成成功: {response.audio_file}")
    print(f"⏱️ 音频时长: {response.duration:.2f}秒")
    print(f"🔧 处理时间: {response.processing_time:.2f}秒")
else:
    print(f"❌ 合成失败: {response.error_message}")
```

### SSML高级语音控制

```python
# 使用SSML控制语音参数
ssml_text = """
<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="zh-CN">
    <voice name="zh-CN-XiaoxiaoNeural">
        <prosody rate="1.2" pitch="high" volume="loud">
            这是一个SSML示例。
        </prosody>
        <break time="1s"/>
        <prosody rate="0.8" pitch="low">
            语音速度变慢，音调变低。
        </prosody>
    </voice>
</speak>
"""

request = TTSRequest(
    text=ssml_text,
    voice_name="zh-CN-XiaoxiaoNeural",
    output_file="ssml_demo.wav"
)
```

### 情感语音合成

```python
# 使用支持情感的语音
emotional_requests = [
    # 开心的语音
    TTSRequest(
        text="今天天气真好！我们去公园玩吧！",
        voice_name="zh-CN-XiaoxiaoNeural",
        output_file="happy.wav"
    ),
    
    # 新闻播报风格
    TTSRequest(
        text="这里是新闻播报，今天的主要新闻如下。",
        voice_name="zh-CN-YunyangNeural",  # 新闻播报语音
        output_file="news.wav"
    ),
    
    # 客服风格
    TTSRequest(
        text="您好，很高兴为您服务，请问有什么可以帮助您的吗？",
        voice_name="zh-CN-XiaoyiNeural",
        output_file="service.wav"
    )
]
```

### 多语言语音合成

```python
# 中文语音
chinese_request = TTSRequest(
    text="你好，我是中文语音助手。",
    voice_name="zh-CN-XiaoxiaoNeural",
    output_file="chinese.wav"
)

# 英文语音
english_request = TTSRequest(
    text="Hello, I am your English voice assistant.",
    voice_name="en-US-AriaNeural",
    output_file="english.wav"
)

# 日文语音
japanese_request = TTSRequest(
    text="こんにちは、私はあなたの日本語音声アシスタントです。",
    voice_name="ja-JP-NanamiNeural",
    output_file="japanese.wav"
)

# 批量处理
requests = [chinese_request, english_request, japanese_request]
for req in requests:
    response = tts.synthesize(req)
    if response.success:
        print(f"✅ {req.output_file} 合成完成")
```

### 长文本处理

```python
# Azure支持较长的文本（最大50,000字符）
long_text = """
这是一个很长的文本示例。Azure TTS可以处理较长的文本内容，
支持多段落、多句子的复杂文本结构。它会自动处理标点符号，
并生成自然流畅的语音效果。

在处理长文本时，Azure TTS会智能地处理语音的节奏和停顿，
确保生成的语音听起来自然和易于理解。
"""

request = TTSRequest(
    text=long_text,
    voice_name="zh-CN-XiaoxiaoNeural",
    voice_rate=1.1,
    output_file="long_text.wav",
    generate_subtitles=True
)

response = tts.synthesize(request)
if response.success:
    print(f"📝 长文本合成完成: {response.audio_file}")
    print(f"📋 字幕文件: {response.subtitle_file}")
```

## 可用语音

### 中文语音（部分）

| 语音名称 | 显示名称 | 性别 | 风格特点 |
|---------|---------|------|---------|
| zh-CN-XiaoxiaoNeural | 晓晓 | 女性 | 通用，支持多种情感 |
| zh-CN-YunxiNeural | 云希 | 男性 | 通用，温和 |
| zh-CN-YunyangNeural | 云扬 | 男性 | 新闻播报 |
| zh-CN-XiaoyiNeural | 晓伊 | 女性 | 通用，亲和 |
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
| en-US-JasonNeural | Jason | 男性 | 美国 |
| en-GB-SoniaNeural | Sonia | 女性 | 英国 |
| en-GB-RyanNeural | Ryan | 男性 | 英国 |
| en-AU-NatashaNeural | Natasha | 女性 | 澳大利亚 |
| en-AU-WilliamNeural | William | 男性 | 澳大利亚 |

### 获取完整语音列表

```python
# 获取所有语音
voices = tts.list_voices()
print(f"共有 {len(voices)} 个语音可用")

# 按语言分组显示
from collections import defaultdict
voices_by_lang = defaultdict(list)
for voice in voices:
    voices_by_lang[voice.language].append(voice)

for lang, lang_voices in voices_by_lang.items():
    print(f"\n🌍 {lang} 语音 ({len(lang_voices)}个):")
    for voice in lang_voices[:5]:  # 显示前5个
        print(f"  🎤 {voice.display_name} ({voice.name}) - {voice.gender}")
```

## 定价和限制

### 定价模式

- **免费层**: 每月500,000字符
- **标准层**: 按字符计费，详见[Azure定价页面](https://azure.microsoft.com/pricing/details/cognitive-services/speech-services/)
- **自定义语音**: 额外收费

### 使用限制

- **文本长度**: 单次合成最大50,000字符
- **并发限制**: 根据定价层不同
- **语音速率**: 支持0.5x到2.0x速度调节
- **音频格式**: 支持多种格式和采样率
- **区域限制**: 某些语音仅在特定区域可用

## 故障排除

### 常见问题

**Q: 提示"Azure SDK未安装"**
```bash
A: 安装Azure语音SDK
pip install azure-cognitiveservices-speech>=1.30.0
```

**Q: 认证失败**
```
A: 检查API密钥和区域配置
- 确认AZURE_SPEECH_KEY环境变量正确
- 确认AZURE_SPEECH_REGION环境变量正确
- 检查Azure Portal中的密钥是否有效
- 确认服务区域名称正确（如eastus，不是East US）
```

**Q: 某些语音不可用**
```
A: 语音可用性因区域而异
- 使用 tts.list_voices() 获取当前区域可用语音
- 尝试切换到其他Azure区域
- 检查语音名称拼写是否正确
```

**Q: 合成速度慢**
```
A: 优化网络和配置
- 选择距离较近的Azure区域
- 检查网络连接质量
- 考虑使用批量处理API
- 优化文本长度和复杂度
```

**Q: 音频质量不佳**
```
A: 调整音频参数
- 使用Neural语音（名称包含"Neural"）
- 调整输出格式和采样率
- 使用SSML精确控制语音参数
- 检查文本格式和标点符号
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
tts = TTSFactory.create_tts("azure", "zh-CN-XiaoxiaoNeural")
# 多次使用同一个实例，避免重复认证

# 3. 选择合适的区域
# 选择地理位置较近的Azure区域以减少延迟
tts = TTSFactory.create_tts(
    "azure", 
    "zh-CN-XiaoxiaoNeural",
    service_region="eastasia"  # 亚洲用户选择eastasia
)

# 4. 优化文本格式
# 使用适当的标点符号和段落分隔
text = """
第一段内容。

第二段内容。
"""
```

## 技术细节

### 音频格式支持

- **WAV**: PCM 8kHz/16kHz/24kHz/48kHz
- **MP3**: 各种比特率
- **OGG**: Opus编码
- **WEBM**: Opus编码

### SSML功能

```xml
<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="zh-CN">
    <voice name="zh-CN-XiaoxiaoNeural">
        <!-- 语音速率 -->
        <prosody rate="1.2">快速语音</prosody>
        
        <!-- 音调 -->
        <prosody pitch="high">高音调</prosody>
        
        <!-- 音量 -->
        <prosody volume="loud">大音量</prosody>
        
        <!-- 停顿 -->
        <break time="2s"/>
        
        <!-- 重音 -->
        <emphasis level="strong">重要内容</emphasis>
        
        <!-- 拼音 -->
        <phoneme alphabet="sapi" ph="n i3 h ao3">你好</phoneme>
    </voice>
</speak>
```

### API限制

- **请求频率**: 根据定价层限制
- **并发连接**: 标准层支持更多并发
- **文本长度**: 最大50,000字符
- **音频时长**: 最大10分钟

## 相关链接

- **官方网站**: [Microsoft Azure认知服务](https://azure.microsoft.com/services/cognitive-services/)
- **Azure Speech服务**: [https://azure.microsoft.com/services/cognitive-services/speech-services/](https://azure.microsoft.com/services/cognitive-services/speech-services/)
- **Azure Speech SDK**: [https://docs.microsoft.com/azure/cognitive-services/speech-service/](https://docs.microsoft.com/azure/cognitive-services/speech-service/)
- **Azure Speech Python SDK**: [https://pypi.org/project/azure-cognitiveservices-speech/](https://pypi.org/project/azure-cognitiveservices-speech/)
- **Azure Speech定价**: [https://azure.microsoft.com/pricing/details/cognitive-services/speech-services/](https://azure.microsoft.com/pricing/details/cognitive-services/speech-services/)
- **SSML参考文档**: [https://docs.microsoft.com/azure/cognitive-services/speech-service/speech-synthesis-markup](https://docs.microsoft.com/azure/cognitive-services/speech-service/speech-synthesis-markup)
- **Azure门户**: [https://portal.azure.com/](https://portal.azure.com/)

## 更新日志

### v1.0.0
- 初始版本
- 支持基本语音合成
- 支持SSML标记
- 支持多语言语音
- 支持语音速率调节
- 支持字幕生成（估算）
- 支持Azure认证和区域配置
