#!/usr/bin/env python3
"""
FunTTS高级使用示例
演示配置管理、批量处理、自定义引擎等高级功能
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from funtts import TTSFactory, TTSConfig, get_config, create_tts, get_available_engines


def demo_config_management():
    """演示配置管理功能"""
    print("=== 配置管理示例 ===")

    # 获取全局配置
    config = get_config()

    # 显示当前配置
    print(f"默认引擎: {config.get_default_engine()}")
    print(f"默认语音: {config.get_default_voice()}")
    print(f"默认速率: {config.get_default_rate()}")

    # 修改配置
    config.set_default_engine("edge")
    config.set_default_voice("zh-CN-XiaoxiaoNeural")
    config.set_default_rate(1.2)

    # 设置引擎特定配置
    config.set_engine_config("pyttsx3", {"volume": 0.8, "rate": 180})

    # 保存配置
    config.save_config()
    print("配置已保存")
    print()


def demo_voice_management():
    """演示语音管理功能"""
    print("=== 语音管理示例 ===")

    engines = get_available_engines()

    for engine_name in engines[:2]:  # 只测试前两个引擎
        try:
            print(f"\n--- {engine_name} 引擎 ---")

            # 创建TTS实例
            tts = TTSFactory.create_tts(engine_name, "default")

            # 获取可用语音
            voices = tts.get_available_voices()
            print(f"可用语音数量: {len(voices)}")

            # 显示前5个语音
            for i, voice in enumerate(voices[:5]):
                print(f"  {i + 1}. {voice}")

            # 检查特定语音是否可用
            test_voices = ["zh-CN-XiaoxiaoNeural", "zh", "0"]
            for voice in test_voices:
                available = tts.is_voice_available(voice)
                print(f"语音 '{voice}' 可用: {available}")

        except Exception as e:
            print(f"处理 {engine_name} 引擎时出错: {e}")

    print()


def demo_batch_processing():
    """演示批量处理功能"""
    print("=== 批量处理示例 ===")

    # 准备测试文本
    texts = [
        "这是第一段测试文本，用于演示批量TTS处理。",
        "这是第二段文本，展示了如何处理多个文本片段。",
        "最后一段文本，演示批量生成语音文件的功能。",
    ]

    output_dir = "batch_output"
    os.makedirs(output_dir, exist_ok=True)

    try:
        # 使用默认配置创建TTS实例
        tts = create_tts()

        print(f"使用引擎: {tts.__class__.__name__}")
        print(f"输出目录: {output_dir}")

        for i, text in enumerate(texts, 1):
            audio_file = os.path.join(output_dir, f"batch_{i}.wav")
            subtitle_file = os.path.join(output_dir, f"batch_{i}.srt")

            print(f"正在处理第 {i} 段文本...")

            # 生成语音
            tts.create_tts(
                text=text,
                voice_rate=1.0,
                voice_file=audio_file,
                subtitle_file=subtitle_file,
            )

            if os.path.exists(audio_file):
                size = os.path.getsize(audio_file)
                print(f"  ✓ 生成成功: {audio_file} ({size} bytes)")
            else:
                print(f"  ✗ 生成失败: {audio_file}")

        print("批量处理完成")

    except Exception as e:
        print(f"批量处理失败: {e}")

    print()


def demo_engine_comparison():
    """演示不同引擎的对比"""
    print("=== 引擎对比示例 ===")

    test_text = "这是一个用于对比不同TTS引擎效果的测试文本。"
    output_dir = "comparison_output"
    os.makedirs(output_dir, exist_ok=True)

    engines = get_available_engines()
    results = {}

    for engine_name in engines:
        try:
            print(f"\n测试 {engine_name} 引擎:")

            # 选择合适的语音
            voice_map = {
                "edge": "zh-CN-XiaoxiaoNeural",
                "azure": "zh-CN-XiaoxiaoNeural",
                "espeak": "zh",
                "pyttsx3": "0",
            }
            voice_name = voice_map.get(engine_name, "default")

            # 创建TTS实例
            tts = TTSFactory.create_tts(engine_name, voice_name)

            # 生成音频
            audio_file = os.path.join(output_dir, f"comparison_{engine_name}.wav")

            import time

            start_time = time.time()

            sub_maker = tts.create_tts(
                text=test_text, voice_rate=1.0, voice_file=audio_file
            )

            end_time = time.time()
            processing_time = end_time - start_time

            # 收集结果
            if os.path.exists(audio_file):
                file_size = os.path.getsize(audio_file)
                duration = tts.get_audio_duration() if sub_maker else 0

                results[engine_name] = {
                    "success": True,
                    "file_size": file_size,
                    "duration": duration,
                    "processing_time": processing_time,
                    "supports_subtitles": sub_maker is not None,
                }

                print(f"  ✓ 成功")
                print(f"    文件大小: {file_size} bytes")
                print(f"    音频时长: {duration:.2f} 秒")
                print(f"    处理时间: {processing_time:.2f} 秒")
                print(f"    字幕支持: {'是' if sub_maker else '否'}")
            else:
                results[engine_name] = {"success": False}
                print(f"  ✗ 失败")

        except Exception as e:
            results[engine_name] = {"success": False, "error": str(e)}
            print(f"  ✗ 错误: {e}")

    # 显示对比结果
    print("\n=== 对比结果 ===")
    print(
        f"{'引擎':<10} {'状态':<6} {'文件大小':<10} {'时长':<8} {'处理时间':<10} {'字幕':<6}"
    )
    print("-" * 60)

    for engine, result in results.items():
        if result["success"]:
            status = "成功"
            size = f"{result['file_size']}B"
            duration = f"{result['duration']:.1f}s"
            proc_time = f"{result['processing_time']:.1f}s"
            subtitles = "是" if result["supports_subtitles"] else "否"
        else:
            status = "失败"
            size = duration = proc_time = subtitles = "-"

        print(
            f"{engine:<10} {status:<6} {size:<10} {duration:<8} {proc_time:<10} {subtitles:<6}"
        )

    print()


def demo_custom_engine():
    """演示如何注册自定义TTS引擎"""
    print("=== 自定义引擎示例 ===")

    from funtts.base import BaseTTS
    from typing import List, Dict, Any, Optional

    class DemoTTS(BaseTTS):
        """演示用的自定义TTS引擎"""

        def _tts(self, text, voice_rate, voice_file, *args, **kwargs):
            # 这里只是演示，实际应该实现真正的TTS逻辑
            print(f"DemoTTS: 正在处理文本 '{text[:20]}...'")
            print(f"DemoTTS: 语音速率 {voice_rate}")
            print(f"DemoTTS: 输出文件 {voice_file}")

            # 创建一个空的音频文件作为演示
            with open(voice_file, "wb") as f:
                f.write(b"\x00" * 1024)  # 写入1KB的空数据

            return None  # 不支持字幕

        def get_available_voices(self, language=None):
            return [
                {"name": "demo_voice_1", "language": "zh-CN", "gender": "female"},
                {"name": "demo_voice_2", "language": "en-US", "gender": "male"},
            ]

        def is_voice_available(self, voice_name):
            return voice_name in ["demo_voice_1", "demo_voice_2"]

    # 注册自定义引擎
    TTSFactory.register_engine("demo", DemoTTS)

    print("已注册自定义引擎: demo")
    print(f"当前可用引擎: {get_available_engines()}")

    # 测试自定义引擎
    try:
        demo_tts = TTSFactory.create_tts("demo", "demo_voice_1")

        output_file = "demo_output.wav"
        demo_tts.create_tts(
            text="这是自定义TTS引擎的测试", voice_rate=1.0, voice_file=output_file
        )

        if os.path.exists(output_file):
            print(f"✓ 自定义引擎测试成功: {output_file}")
            os.remove(output_file)  # 清理测试文件
        else:
            print("✗ 自定义引擎测试失败")

    except Exception as e:
        print(f"自定义引擎测试出错: {e}")

    print()


def main():
    """主函数"""
    print("=== FunTTS 高级使用示例 ===\n")

    # 演示各种高级功能
    demo_config_management()
    demo_voice_management()
    demo_batch_processing()
    demo_engine_comparison()
    demo_custom_engine()

    print("=== 所有示例演示完成 ===")


if __name__ == "__main__":
    main()
