# eSpeak TTS引擎

## 概述

eSpeak是一个开源的多语言语音合成器，支持100多种语言。它是一个轻量级的TTS引擎，完全免费使用，适合对资源占用有要求或需要离线语音合成的场景。虽然语音质量相比商业引擎较为机械，但胜在开源免费且支持语言众多。

## 特性

- ✅ **完全免费** - 开源软件，无任何使用限制
- ✅ **多语言支持** - 支持100+种语言和方言
- ✅ **轻量级** - 资源占用少，适合嵌入式设备
- ✅ **离线工作** - 无需网络连接
- ✅ **跨平台** - 支持Windows、Linux、macOS
- ✅ **参数可调** - 支持语音速度、音调、音量调节
- ✅ **SSML支持** - 部分支持SSML标记
- ❌ **语音质量** - 相比神经网络语音较为机械
- ❌ **字幕生成** - 不支持自动字幕生成

## 依赖要求

### 系统依赖

eSpeak需要在系统级别安装：

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install espeak espeak-data

# CentOS/RHEL/Fedora
sudo yum install espeak espeak-devel
# 或者 (较新版本)
sudo dnf install espeak espeak-devel

# macOS
brew install espeak

# Windows
# 1. 从 http://espeak.sourceforge.net/download.html 下载安装包
# 2. 或者使用 Chocolatey: choco install espeak
# 3. 或者使用 Scoop: scoop install espeak
```

### Python包依赖

eSpeak引擎不需要额外的Python包，直接调用系统命令。

### 可选依赖

- **FFmpeg** (用于音频时长检测)
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

eSpeak无需特殊配置，安装后即可使用：

```python
# 默认配置
config = {
    "espeak_path": "espeak"  # eSpeak可执行文件路径
}
```

### 自定义eSpeak路径

如果eSpeak安装在非标准位置：

```python
from funtts import TTSFactory

tts = TTSFactory.create_tts(
    "espeak", 
    "zh",
    espeak_path="/usr/local/bin/espeak"  # 自定义路径
)
```

### 语音参数配置

```python
from funtts.models import TTSRequest

request = TTSRequest(
    text="你好，世界！",
    voice_name="zh",                     # 语言代码
    voice_rate=1.2,                      # 语音速率
    voice_pitch=1.1,                     # 音调（如果支持）
    voice_volume=0.8,                    # 音量（如果支持）
    output_format="wav",                 # 输出格式
    output_file="output.wav"
)
```

## 使用示例

### 基本使用

```python
from funtts import TTSFactory, TTSRequest

# 创建引擎实例
tts = TTSFactory.create_tts("espeak", "zh")

# 合成语音
request = TTSRequest(
    text="欢迎使用eSpeak TTS引擎！",
    voice_name="zh",
    output_file="output.wav"
)
response = tts.synthesize(request)

if response.success:
    print(f"✅ 合成成功: {response.audio_file}")
    print(f"⏱️ 音频时长: {response.duration:.2f}秒")
else:
    print(f"❌ 合成失败: {response.error_message}")
```

### 多语言语音合成

```python
# 中文语音
chinese_request = TTSRequest(
    text="你好，这是中文语音。",
    voice_name="zh",
    output_file="chinese.wav"
)

# 英文语音
english_request = TTSRequest(
    text="Hello, this is English voice.",
    voice_name="en",
    output_file="english.wav"
)

# 西班牙语语音
spanish_request = TTSRequest(
    text="Hola, esta es la voz en español.",
    voice_name="es",
    output_file="spanish.wav"
)

# 法语语音
french_request = TTSRequest(
    text="Bonjour, c'est la voix française.",
    voice_name="fr",
    output_file="french.wav"
)

# 批量处理
requests = [chinese_request, english_request, spanish_request, french_request]
for req in requests:
    response = tts.synthesize(req)
    if response.success:
        print(f"✅ {req.output_file} 合成完成")
```

### 语音参数调节

```python
# 慢速语音
slow_request = TTSRequest(
    text="这是慢速语音示例。",
    voice_name="zh",
    voice_rate=0.7,  # 70%速度
    output_file="slow.wav"
)

# 快速语音
fast_request = TTSRequest(
    text="这是快速语音示例。",
    voice_name="zh",
    voice_rate=1.5,  # 150%速度
    output_file="fast.wav"
)

# 高音调语音
high_pitch_request = TTSRequest(
    text="这是高音调语音示例。",
    voice_name="zh",
    voice_pitch=1.3,  # 130%音调
    output_file="high_pitch.wav"
)

# 低音量语音
low_volume_request = TTSRequest(
    text="这是低音量语音示例。",
    voice_name="zh",
    voice_volume=0.5,  # 50%音量
    output_file="low_volume.wav"
)
```

### 检查eSpeak安装

```python
import subprocess

def check_espeak_installation():
    """检查eSpeak是否正确安装"""
    try:
        result = subprocess.run(
            ["espeak", "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            print(f"✅ eSpeak已安装: {result.stdout.strip()}")
            return True
        else:
            print("❌ eSpeak未正确安装")
            return False
    except FileNotFoundError:
        print("❌ 找不到eSpeak命令，请检查安装")
        return False
    except Exception as e:
        print(f"❌ 检查eSpeak时出错: {e}")
        return False

# 检查安装
if check_espeak_installation():
    tts = TTSFactory.create_tts("espeak", "zh")
```

## 可用语音

### 主要语言支持

| 语言代码 | 语言名称 | 示例文本 |
|---------|---------|---------|
| zh | 中文 | 你好，世界！ |
| en | English | Hello, world! |
| es | Español | ¡Hola, mundo! |
| fr | Français | Bonjour le monde! |
| de | Deutsch | Hallo Welt! |
| it | Italiano | Ciao mondo! |
| pt | Português | Olá mundo! |
| ru | Русский | Привет мир! |
| ja | 日本語 | こんにちは世界！ |
| ko | 한국어 | 안녕하세요 세계! |
| ar | العربية | مرحبا بالعالم! |
| hi | हिन्दी | नमस्ते दुनिया! |
| th | ไทย | สวัสดีชาวโลก! |
| vi | Tiếng Việt | Chào thế giới! |

### 获取完整语音列表

```python
# 获取所有可用语音
voices = tts.list_voices()
print(f"共有 {len(voices)} 个语音可用")

# 显示语音信息
for voice in voices[:10]:  # 显示前10个
    print(f"🌍 {voice.display_name} ({voice.name}) - {voice.language}")

# 按语言过滤
chinese_voices = tts.list_voices(language="zh")
english_voices = tts.list_voices(language="en")

print(f"中文语音: {len(chinese_voices)}个")
print(f"英文语音: {len(english_voices)}个")
```

### 语音变体

某些语言有多个变体：

```python
# 英语变体
variants = [
    ("en", "英语（通用）"),
    ("en-gb", "英语（英国）"),
    ("en-us", "英语（美国）"),
    ("en-au", "英语（澳大利亚）"),
    ("en-ca", "英语（加拿大）"),
]

for code, name in variants:
    request = TTSRequest(
        text="This is a test of English variants.",
        voice_name=code,
        output_file=f"english_{code.replace('-', '_')}.wav"
    )
    response = tts.synthesize(request)
```

## 限制说明

- **语音质量**: 机械感较强，不如神经网络语音自然
- **语音选择**: 每种语言通常只有一个基础语音
- **字幕支持**: 不支持自动字幕生成
- **文本长度**: 建议单次合成不超过10,000字符
- **音频格式**: 主要支持WAV格式
- **SSML支持**: 仅支持部分SSML标记

## 故障排除

### 常见问题

**Q: 提示"eSpeak程序不可用"**
```bash
A: 安装eSpeak系统程序
# Ubuntu/Debian
sudo apt-get install espeak espeak-data

# macOS
brew install espeak

# Windows
# 下载安装包或使用包管理器安装
```

**Q: 找不到eSpeak命令**
```
A: 检查PATH环境变量
- 确认eSpeak已正确安装
- 检查eSpeak是否在系统PATH中
- 尝试使用完整路径：/usr/bin/espeak
```

**Q: 中文语音效果不佳**
```
A: eSpeak的中文支持有限
- 尝试调整语音速率和音调
- 考虑使用其他引擎（如Edge TTS）处理中文
- 将复杂句子分解为简单句子
```

**Q: 合成的音频文件为空**
```
A: 检查文本和参数
- 确认文本内容不为空
- 检查语音代码是否正确
- 验证输出文件路径可写
- 查看eSpeak错误信息
```

**Q: 语音速度太快或太慢**
```
A: 调整voice_rate参数
request.voice_rate = 1.2  # 120%速度
request.voice_rate = 0.8  # 80%速度
```

### 性能优化

```python
# 1. 批量处理优化
texts = ["文本1", "文本2", "文本3"]
for i, text in enumerate(texts):
    request = TTSRequest(
        text=text,
        voice_name="zh",
        output_file=f"batch_{i}.wav"
    )
    response = tts.synthesize(request)

# 2. 重用TTS实例
tts = TTSFactory.create_tts("espeak", "zh")
# 多次使用同一个实例

# 3. 文本预处理
def preprocess_text(text):
    """预处理文本以提高eSpeak效果"""
    # 移除特殊字符
    import re
    text = re.sub(r'[^\w\s\u4e00-\u9fff.,!?;:]', '', text)
    
    # 添加适当的停顿
    text = text.replace('。', '。 ')
    text = text.replace('！', '！ ')
    text = text.replace('？', '？ ')
    
    return text.strip()

# 使用预处理
processed_text = preprocess_text("你好！这是一个测试。")
request = TTSRequest(text=processed_text, voice_name="zh", output_file="output.wav")
```

## 技术细节

### eSpeak命令参数

FunTTS使用的主要eSpeak参数：

```bash
espeak -v zh          # 指定语音/语言
       -s 150         # 语音速度 (words per minute)
       -p 50          # 音调 (0-99)
       -a 100         # 音量 (0-200)
       -w output.wav  # 输出到文件
       "文本内容"      # 要合成的文本
```

### 音频格式

- **默认格式**: WAV, 22kHz, 16-bit, 单声道
- **文件大小**: 约44KB/秒
- **质量**: 标准质量，适合语音提示

### 语言代码

eSpeak使用ISO语言代码：
- `zh`: 中文
- `en`: 英语
- `es`: 西班牙语
- `fr`: 法语
- `de`: 德语
- `it`: 意大利语
- `pt`: 葡萄牙语
- `ru`: 俄语
- `ja`: 日语
- `ko`: 韩语

## 使用场景

### 适合的场景

- **系统提示音**: 简单的语音提示
- **嵌入式设备**: 资源受限的环境
- **离线应用**: 无网络连接的场景
- **多语言支持**: 需要支持多种语言
- **开发测试**: 快速原型和测试
- **教育项目**: 学习语音合成技术

### 不适合的场景

- **高质量语音**: 需要自然流畅的语音
- **商业应用**: 对语音质量要求高的场景
- **长文本**: 需要处理大量文本内容
- **实时应用**: 对延迟要求极低的场景

## 相关链接

- **官方网站**: [eSpeak官网](http://espeak.sourceforge.net/)
- **eSpeak SourceForge**: [https://sourceforge.net/projects/espeak/](https://sourceforge.net/projects/espeak/)
- **eSpeak-ng GitHub**: [https://github.com/espeak-ng/espeak-ng](https://github.com/espeak-ng/espeak-ng)
- **eSpeak文档**: [http://espeak.sourceforge.net/commands.html](http://espeak.sourceforge.net/commands.html)
- **eSpeak语音列表**: [http://espeak.sourceforge.net/languages.html](http://espeak.sourceforge.net/languages.html)
- **Ubuntu eSpeak包**: [https://packages.ubuntu.com/search?keywords=espeak](https://packages.ubuntu.com/search?keywords=espeak)
- **Debian eSpeak包**: [https://packages.debian.org/search?keywords=espeak](https://packages.debian.org/search?keywords=espeak)

## 更新日志

### v1.0.0
- 初始版本
- 支持基本语音合成
- 支持多语言
- 支持语音参数调节
- 支持语音列表获取
- 支持系统eSpeak程序调用
