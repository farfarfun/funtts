#!/usr/bin/env python3
"""
FunTTS 综合示例 - 展示所有TTS引擎的使用方法

这个示例展示了如何使用FunTTS支持的所有TTS引擎，
包括基础用法、高级功能和最佳实践。

运行前请确保安装了相应的依赖：
pip install funtts-plus[all]
"""

import os
import time
from pathlib import Path
from funtts.models import TTSRequest
from funtts import create_tts, get_available_engines


def setup_output_directory():
    """创建输出目录"""
    output_dir = Path("./tts_output")
    output_dir.mkdir(exist_ok=True)
    return output_dir


def demo_edge_tts():
    """演示Edge TTS - 免费推荐引擎"""
    print("\n🔊 Edge TTS 演示")
    print("=" * 50)

    try:
        from funtts.tts.edge import EdgeTTS

        tts = EdgeTTS()

        # 基础用法
        request = TTSRequest(
            text="你好！这是微软Edge TTS的中文语音合成演示。",
            voice_name="zh-CN-XiaoxiaoNeural",
            output_dir="./tts_output/edge",
        )

        print("正在生成语音...")
        start_time = time.time()
        response = tts.synthesize(request)
        end_time = time.time()

        print("✅ 生成完成！")
        print(f"📁 音频文件: {response.audio_file}")
        print(f"⏱️  生成时间: {end_time - start_time:.2f}秒")
        print(f"🎵 音频时长: {response.duration:.2f}秒")

        # 获取可用语音
        voices = tts.list_voices(language="zh-CN")
        print(f"🎭 可用中文语音数量: {len(voices)}")

    except ImportError:
        print("❌ Edge TTS未安装，跳过演示")
    except Exception as e:
        print(f"❌ Edge TTS演示失败: {e}")


def demo_azure_tts():
    """演示Azure TTS - 企业级引擎"""
    print("\n🔊 Azure TTS 演示")
    print("=" * 50)

    try:
        from funtts.tts.azure import AzureTTS

        # 注意：需要设置Azure API密钥
        if not os.getenv("AZURE_SPEECH_KEY"):
            print("⚠️  需要设置AZURE_SPEECH_KEY环境变量")
            return

        tts = AzureTTS()

        # 使用SSML进行高级控制
        ssml_text = """
        <speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="zh-CN">
            <voice name="zh-CN-XiaoxiaoNeural">
                <prosody rate="medium" pitch="medium">
                    这是Azure TTS的SSML演示。
                </prosody>
                <break time="500ms"/>
                <prosody rate="slow" pitch="low">
                    我可以调整语速和音调。
                </prosody>
            </voice>
        </speak>
        """

        request = TTSRequest(
            text=ssml_text,
            voice_name="zh-CN-XiaoxiaoNeural",
            output_dir="./tts_output/azure",
            subtitle_format="srt",
        )

        print("正在生成SSML语音...")
        response = tts.synthesize(request)
        print(f"✅ Azure TTS生成完成: {response.audio_file}")

    except ImportError:
        print("❌ Azure TTS未安装，跳过演示")
    except Exception as e:
        print(f"❌ Azure TTS演示失败: {e}")


def demo_coqui_tts():
    """演示Coqui TTS - 深度学习引擎"""
    print("\n🔊 Coqui TTS 演示")
    print("=" * 50)

    try:
        from funtts.tts.coqui import CoquiTTS

        tts = CoquiTTS()

        # 基础语音合成
        request = TTSRequest(
            text="Hello! This is Coqui TTS, a powerful deep learning text-to-speech engine.",
            voice_name="tts_models/en/ljspeech/tacotron2-DDC",
            output_dir="./tts_output/coqui",
        )

        print("正在生成Coqui TTS语音...")
        response = tts.synthesize(request)
        print(f"✅ Coqui TTS生成完成: {response.audio_file}")

        # 演示语音克隆（需要参考音频）
        print("💡 Coqui TTS支持语音克隆功能（需要参考音频文件）")

    except ImportError:
        print("❌ Coqui TTS未安装，跳过演示")
    except Exception as e:
        print(f"❌ Coqui TTS演示失败: {e}")


def demo_bark_tts():
    """演示Bark TTS - 特效音效引擎"""
    print("\n🔊 Bark TTS 演示")
    print("=" * 50)

    try:
        from funtts.tts.bark import BarkTTS

        tts = BarkTTS()

        # 基础语音合成
        request = TTSRequest(
            text="Hello! This is Bark TTS speaking.",
            voice_name="v2/en_speaker_6",
            output_dir="./tts_output/bark",
        )

        print("正在生成Bark TTS语音...")
        response = tts.synthesize(request)
        print(f"✅ Bark TTS基础生成完成: {response.audio_file}")

        # 演示特效功能
        print("🎭 演示特效功能...")
        effects_response = tts.generate_with_effects(
            text="That's really funny! [laughter] Welcome to our show! ♪ This is amazing ♪",
            output_path="./tts_output/bark/effects_demo.wav",
            effects=["laughter", "music"],
        )
        print(f"✅ 特效语音生成完成: {effects_response}")

    except ImportError:
        print("❌ Bark TTS未安装，跳过演示")
    except Exception as e:
        print(f"❌ Bark TTS演示失败: {e}")


def demo_tortoise_tts():
    """演示Tortoise TTS - 高质量语音克隆引擎"""
    print("\n🔊 Tortoise TTS 演示")
    print("=" * 50)

    try:
        from funtts.tts.tortoise import TortoiseTTS

        # 使用快速预设进行演示
        tts = TortoiseTTS(preset="fast")

        request = TTSRequest(
            text="This is Tortoise TTS, known for its incredibly high-quality voice synthesis.",
            voice_name="angie",
            output_dir="./tts_output/tortoise",
        )

        print("正在生成Tortoise TTS语音（快速模式）...")
        response = tts.synthesize(request)
        print(f"✅ Tortoise TTS生成完成: {response.audio_file}")

        print("💡 Tortoise TTS支持高质量语音克隆（需要参考音频文件）")

    except ImportError:
        print("❌ Tortoise TTS未安装，跳过演示")
    except Exception as e:
        print(f"❌ Tortoise TTS演示失败: {e}")


def demo_indextts2():
    """演示IndexTTS2 - 情感控制引擎"""
    print("\n🔊 IndexTTS2 演示")
    print("=" * 50)

    try:
        from funtts.tts.indextts2 import IndexTTS2

        tts = IndexTTS2()

        request = TTSRequest(
            text="这是IndexTTS2的演示，支持精确的情感控制和时长控制。",
            voice_name="zh-CN-XiaoxiaoNeural",
            output_dir="./tts_output/indextts2",
        )

        print("正在生成IndexTTS2语音...")
        response = tts.synthesize(request)
        print(f"✅ IndexTTS2生成完成: {response.audio_file}")

    except ImportError:
        print("❌ IndexTTS2未安装，跳过演示")
    except Exception as e:
        print(f"❌ IndexTTS2演示失败: {e}")


def demo_kitten_tts():
    """演示KittenTTS - 神经网络引擎"""
    print("\n🔊 KittenTTS 演示")
    print("=" * 50)

    try:
        from funtts.tts.kitten import KittenTTS

        tts = KittenTTS()

        request = TTSRequest(
            text="Hello from KittenTTS, a neural network based text-to-speech engine.",
            voice_name="default",
            output_dir="./tts_output/kitten",
        )

        print("正在生成KittenTTS语音...")
        response = tts.synthesize(request)
        print(f"✅ KittenTTS生成完成: {response.audio_file}")

    except ImportError:
        print("❌ KittenTTS未安装，跳过演示")
    except Exception as e:
        print(f"❌ KittenTTS演示失败: {e}")


def demo_espeak_tts():
    """演示eSpeak TTS - 轻量级引擎"""
    print("\n🔊 eSpeak TTS 演示")
    print("=" * 50)

    try:
        from funtts.tts.espeak import EspeakTTS

        tts = EspeakTTS()

        request = TTSRequest(
            text="This is eSpeak TTS, a lightweight and fast text-to-speech engine.",
            voice_name="en",
            output_dir="./tts_output/espeak",
        )

        print("正在生成eSpeak TTS语音...")
        response = tts.synthesize(request)
        print(f"✅ eSpeak TTS生成完成: {response.audio_file}")

    except ImportError:
        print("❌ eSpeak TTS未安装，跳过演示")
    except Exception as e:
        print(f"❌ eSpeak TTS演示失败: {e}")


def demo_pyttsx3_tts():
    """演示pyttsx3 TTS - 跨平台本地引擎"""
    print("\n🔊 pyttsx3 TTS 演示")
    print("=" * 50)

    try:
        from funtts.tts.pyttsx3 import Pyttsx3TTS

        tts = Pyttsx3TTS()

        request = TTSRequest(
            text="This is pyttsx3 TTS, a cross-platform offline text-to-speech engine.",
            voice_name="default",
            output_dir="./tts_output/pyttsx3",
        )

        print("正在生成pyttsx3 TTS语音...")
        response = tts.synthesize(request)
        print(f"✅ pyttsx3 TTS生成完成: {response.audio_file}")

    except ImportError:
        print("❌ pyttsx3 TTS未安装，跳过演示")
    except Exception as e:
        print(f"❌ pyttsx3 TTS演示失败: {e}")


def demo_factory_pattern():
    """演示工厂模式使用"""
    print("\n🏭 工厂模式演示")
    print("=" * 50)

    # 获取可用引擎
    available_engines = get_available_engines()
    print(f"📋 可用引擎: {available_engines}")

    # 使用工厂模式创建TTS实例
    if "edge" in available_engines:
        tts = create_tts(engine_name="edge")
        print(f"✅ 通过工厂模式创建Edge TTS实例: {type(tts).__name__}")

    if "azure" in available_engines and os.getenv("AZURE_SPEECH_KEY"):
        tts = create_tts(engine_name="azure")
        print(f"✅ 通过工厂模式创建Azure TTS实例: {type(tts).__name__}")


def demo_batch_processing():
    """演示批量处理"""
    print("\n📦 批量处理演示")
    print("=" * 50)

    try:
        from funtts.tts.edge import EdgeTTS

        tts = EdgeTTS()

        texts = ["这是第一段文本。", "这是第二段文本。", "这是第三段文本。"]

        print("正在批量生成语音...")
        for i, text in enumerate(texts):
            request = TTSRequest(
                text=text,
                voice_name="zh-CN-XiaoxiaoNeural",
                output_dir=f"./tts_output/batch/item_{i}",
            )
            response = tts.synthesize(request)
            print(f"  ✅ 批量项目 {i + 1}: {response.audio_file}")

    except Exception as e:
        print(f"❌ 批量处理演示失败: {e}")


def demo_subtitle_generation():
    """演示字幕生成"""
    print("\n📝 字幕生成演示")
    print("=" * 50)

    try:
        from funtts.tts.edge import EdgeTTS

        tts = EdgeTTS()

        request = TTSRequest(
            text="这是一个字幕生成的演示。我们可以同时生成SRT和FRT格式的字幕文件。",
            voice_name="zh-CN-XiaoxiaoNeural",
            output_dir="./tts_output/subtitles",
            subtitle_format="srt,frt",
        )

        print("正在生成带字幕的语音...")
        response = tts.synthesize(request)
        print(f"✅ 音频文件: {response.audio_file}")
        print(f"📝 SRT字幕: {response.subtitle_file}")
        print(f"📝 FRT字幕: {response.frt_subtitle_file}")

    except Exception as e:
        print(f"❌ 字幕生成演示失败: {e}")


def performance_comparison():
    """性能对比演示"""
    print("\n⚡ 性能对比演示")
    print("=" * 50)

    test_text = "这是一个性能测试文本，用于比较不同TTS引擎的生成速度。"

    engines_to_test = [
        ("Edge TTS", "funtts.tts.edge", "EdgeTTS"),
        ("eSpeak TTS", "funtts.tts.espeak", "EspeakTTS"),
        ("pyttsx3 TTS", "funtts.tts.pyttsx3", "Pyttsx3TTS"),
    ]

    results = []

    for engine_name, module_name, class_name in engines_to_test:
        try:
            module = __import__(module_name, fromlist=[class_name])
            tts_class = getattr(module, class_name)
            tts = tts_class()

            request = TTSRequest(
                text=test_text,
                output_dir=f"./tts_output/performance/{engine_name.lower().replace(' ', '_')}",
            )

            start_time = time.time()
            response = tts.synthesize(request)
            end_time = time.time()

            duration = end_time - start_time
            results.append((engine_name, duration, response.duration))

        except Exception as e:
            print(f"❌ {engine_name} 测试失败: {e}")

    # 显示结果
    print("\n📊 性能对比结果:")
    print("-" * 60)
    print(f"{'引擎名称':<15} {'生成时间(秒)':<12} {'音频时长(秒)':<12} {'实时率':<10}")
    print("-" * 60)

    for engine_name, gen_time, audio_duration in results:
        real_time_factor = audio_duration / gen_time if gen_time > 0 else 0
        print(
            f"{engine_name:<15} {gen_time:<12.2f} {audio_duration:<12.2f} {real_time_factor:<10.2f}x"
        )


def main():
    """主函数"""
    print("🎉 FunTTS 综合演示")
    print("=" * 80)
    print("这个演示将展示FunTTS支持的所有TTS引擎的功能")
    print("请确保已安装相应的依赖包")
    print("=" * 80)

    # 创建输出目录
    output_dir = setup_output_directory()
    print(f"📁 输出目录: {output_dir.absolute()}")

    # 演示各个TTS引擎
    demo_edge_tts()
    demo_azure_tts()
    demo_coqui_tts()
    demo_bark_tts()
    demo_tortoise_tts()
    demo_indextts2()
    demo_kitten_tts()
    demo_espeak_tts()
    demo_pyttsx3_tts()

    # 演示高级功能
    demo_factory_pattern()
    demo_batch_processing()
    demo_subtitle_generation()

    # 性能对比
    performance_comparison()

    print("\n🎊 演示完成！")
    print("=" * 80)
    print("查看输出目录中生成的音频文件和字幕文件")
    print("更多详细信息请参考各个引擎的README文档")


if __name__ == "__main__":
    main()
