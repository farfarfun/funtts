import os
import time
from datetime import datetime
from typing import List, Optional

from funutil import getLogger
import azure.cognitiveservices.speech as speechsdk
from funtts.base import BaseTTS
from funtts.models import (
    TTSRequest,
    TTSResponse,
    VoiceInfo,
    SubtitleMaker,
    AudioSegment,
)

logger = getLogger("funtts.azure")


class AzureTTS(BaseTTS):
    """Azure认知服务TTS引擎实现"""

    def __init__(self, voice_name: str = "zh-CN-XiaoxiaoNeural", *args, **kwargs):
        """初始化Azure TTS

        Args:
            voice_name: 语音名称
        """
        super().__init__(voice_name, *args, **kwargs)
        self.speech_key = kwargs.get("speech_key") or os.getenv("AZURE_SPEECH_KEY", "")
        self.service_region = kwargs.get("service_region") or os.getenv(
            "AZURE_SPEECH_REGION", ""
        )

        if not self.speech_key or not self.service_region:
            logger.warning("Azure语音服务密钥或区域未配置")

    def list_voices(self, language: Optional[str] = None) -> List[VoiceInfo]:
        """获取可用的语音列表

        Args:
            language: 语言代码过滤（如 'zh-CN'）

        Returns:
            语音信息列表
        """
        if language is None:
            filter_locals = ["zh-CN", "en-US", "zh-HK", "zh-TW", "vi-VN"]
        else:
            filter_locals = [language]
        voices_str = """
        Name: af-ZA-AdriNeural
        Gender: Female
        
        Name: af-ZA-WillemNeural
        Gender: Male
        
        Name: am-ET-AmehaNeural
        Gender: Male
        
        Name: am-ET-MekdesNeural
        Gender: Female
        
        Name: ar-AE-FatimaNeural
        Gender: Female
        
        Name: ar-AE-HamdanNeural
        Gender: Male
        
        Name: ar-BH-AliNeural
        Gender: Male
        
        Name: ar-BH-LailaNeural
        Gender: Female
        
        Name: ar-DZ-AminaNeural
        Gender: Female
        
        Name: ar-DZ-IsmaelNeural
        Gender: Male
        
        Name: ar-EG-SalmaNeural
        Gender: Female
        
        Name: ar-EG-ShakirNeural
        Gender: Male
        
        Name: ar-IQ-BasselNeural
        Gender: Male
        
        Name: ar-IQ-RanaNeural
        Gender: Female
        
        Name: ar-JO-SanaNeural
        Gender: Female
        
        Name: ar-JO-TaimNeural
        Gender: Male
        
        Name: ar-KW-FahedNeural
        Gender: Male
        
        Name: ar-KW-NouraNeural
        Gender: Female
        
        Name: ar-LB-LaylaNeural
        Gender: Female
        
        Name: ar-LB-RamiNeural
        Gender: Male
        
        Name: ar-LY-ImanNeural
        Gender: Female
        
        Name: ar-LY-OmarNeural
        Gender: Male
        
        Name: ar-MA-JamalNeural
        Gender: Male
        
        Name: ar-MA-MounaNeural
        Gender: Female
        
        Name: ar-OM-AbdullahNeural
        Gender: Male
        
        Name: ar-OM-AyshaNeural
        Gender: Female
        
        Name: ar-QA-AmalNeural
        Gender: Female
        
        Name: ar-QA-MoazNeural
        Gender: Male
        
        Name: ar-SA-HamedNeural
        Gender: Male
        
        Name: ar-SA-ZariyahNeural
        Gender: Female
        
        Name: ar-SY-AmanyNeural
        Gender: Female
        
        Name: ar-SY-LaithNeural
        Gender: Male
        
        Name: ar-TN-HediNeural
        Gender: Male
        
        Name: ar-TN-ReemNeural
        Gender: Female
        
        Name: ar-YE-MaryamNeural
        Gender: Female
        
        Name: ar-YE-SalehNeural
        Gender: Male
        
        Name: az-AZ-BabekNeural
        Gender: Male
        
        Name: az-AZ-BanuNeural
        Gender: Female
        
        Name: bg-BG-BorislavNeural
        Gender: Male
        
        Name: bg-BG-KalinaNeural
        Gender: Female
        
        Name: bn-BD-NabanitaNeural
        Gender: Female
        
        Name: bn-BD-PradeepNeural
        Gender: Male
        
        Name: bn-IN-BashkarNeural
        Gender: Male
        
        Name: bn-IN-TanishaaNeural
        Gender: Female
        
        Name: bs-BA-GoranNeural
        Gender: Male
        
        Name: bs-BA-VesnaNeural
        Gender: Female
        
        Name: ca-ES-EnricNeural
        Gender: Male
        
        Name: ca-ES-JoanaNeural
        Gender: Female
        
        Name: cs-CZ-AntoninNeural
        Gender: Male
        
        Name: cs-CZ-VlastaNeural
        Gender: Female
        
        Name: cy-GB-AledNeural
        Gender: Male
        
        Name: cy-GB-NiaNeural
        Gender: Female
        
        Name: da-DK-ChristelNeural
        Gender: Female
        
        Name: da-DK-JeppeNeural
        Gender: Male
        
        Name: de-AT-IngridNeural
        Gender: Female
        
        Name: de-AT-JonasNeural
        Gender: Male
        
        Name: de-CH-JanNeural
        Gender: Male
        
        Name: de-CH-LeniNeural
        Gender: Female
        
        Name: de-DE-AmalaNeural
        Gender: Female
        
        Name: de-DE-ConradNeural
        Gender: Male
        
        Name: de-DE-FlorianMultilingualNeural
        Gender: Male
        
        Name: de-DE-KatjaNeural
        Gender: Female
        
        Name: de-DE-KillianNeural
        Gender: Male
        
        Name: de-DE-SeraphinaMultilingualNeural
        Gender: Female
        
        Name: el-GR-AthinaNeural
        Gender: Female
        
        Name: el-GR-NestorasNeural
        Gender: Male
        
        Name: en-AU-NatashaNeural
        Gender: Female
        
        Name: en-AU-WilliamNeural
        Gender: Male
        
        Name: en-CA-ClaraNeural
        Gender: Female
        
        Name: en-CA-LiamNeural
        Gender: Male
        
        Name: en-GB-LibbyNeural
        Gender: Female
        
        Name: en-GB-MaisieNeural
        Gender: Female
        
        Name: en-GB-RyanNeural
        Gender: Male
        
        Name: en-GB-SoniaNeural
        Gender: Female
        
        Name: en-GB-ThomasNeural
        Gender: Male
        
        Name: en-HK-SamNeural
        Gender: Male
        
        Name: en-HK-YanNeural
        Gender: Female
        
        Name: en-IE-ConnorNeural
        Gender: Male
        
        Name: en-IE-EmilyNeural
        Gender: Female
        
        Name: en-IN-NeerjaExpressiveNeural
        Gender: Female
        
        Name: en-IN-NeerjaNeural
        Gender: Female
        
        Name: en-IN-PrabhatNeural
        Gender: Male
        
        Name: en-KE-AsiliaNeural
        Gender: Female
        
        Name: en-KE-ChilembaNeural
        Gender: Male
        
        Name: en-NG-AbeoNeural
        Gender: Male
        
        Name: en-NG-EzinneNeural
        Gender: Female
        
        Name: en-NZ-MitchellNeural
        Gender: Male
        
        Name: en-NZ-MollyNeural
        Gender: Female
        
        Name: en-PH-JamesNeural
        Gender: Male
        
        Name: en-PH-RosaNeural
        Gender: Female
        
        Name: en-SG-LunaNeural
        Gender: Female
        
        Name: en-SG-WayneNeural
        Gender: Male
        
        Name: en-TZ-ElimuNeural
        Gender: Male
        
        Name: en-TZ-ImaniNeural
        Gender: Female
        
        Name: en-US-AnaNeural
        Gender: Female
        
        Name: en-US-AndrewNeural
        Gender: Male
        
        Name: en-US-AriaNeural
        Gender: Female
        
        Name: en-US-AvaNeural
        Gender: Female
        
        Name: en-US-BrianNeural
        Gender: Male
        
        Name: en-US-ChristopherNeural
        Gender: Male
        
        Name: en-US-EmmaNeural
        Gender: Female
        
        Name: en-US-EricNeural
        Gender: Male
        
        Name: en-US-GuyNeural
        Gender: Male
        
        Name: en-US-JennyNeural
        Gender: Female
        
        Name: en-US-MichelleNeural
        Gender: Female
        
        Name: en-US-RogerNeural
        Gender: Male
        
        Name: en-US-SteffanNeural
        Gender: Male
        
        Name: en-ZA-LeahNeural
        Gender: Female
        
        Name: en-ZA-LukeNeural
        Gender: Male
        
        Name: es-AR-ElenaNeural
        Gender: Female
        
        Name: es-AR-TomasNeural
        Gender: Male
        
        Name: es-BO-MarceloNeural
        Gender: Male
        
        Name: es-BO-SofiaNeural
        Gender: Female
        
        Name: es-CL-CatalinaNeural
        Gender: Female
        
        Name: es-CL-LorenzoNeural
        Gender: Male
        
        Name: es-CO-GonzaloNeural
        Gender: Male
        
        Name: es-CO-SalomeNeural
        Gender: Female
        
        Name: es-CR-JuanNeural
        Gender: Male
        
        Name: es-CR-MariaNeural
        Gender: Female
        
        Name: es-CU-BelkysNeural
        Gender: Female
        
        Name: es-CU-ManuelNeural
        Gender: Male
        
        Name: es-DO-EmilioNeural
        Gender: Male
        
        Name: es-DO-RamonaNeural
        Gender: Female
        
        Name: es-EC-AndreaNeural
        Gender: Female
        
        Name: es-EC-LuisNeural
        Gender: Male
        
        Name: es-ES-AlvaroNeural
        Gender: Male
        
        Name: es-ES-ElviraNeural
        Gender: Female
        
        Name: es-ES-XimenaNeural
        Gender: Female
        
        Name: es-GQ-JavierNeural
        Gender: Male
        
        Name: es-GQ-TeresaNeural
        Gender: Female
        
        Name: es-GT-AndresNeural
        Gender: Male
        
        Name: es-GT-MartaNeural
        Gender: Female
        
        Name: es-HN-CarlosNeural
        Gender: Male
        
        Name: es-HN-KarlaNeural
        Gender: Female
        
        Name: es-MX-DaliaNeural
        Gender: Female
        
        Name: es-MX-JorgeNeural
        Gender: Male
        
        Name: es-NI-FedericoNeural
        Gender: Male
        
        Name: es-NI-YolandaNeural
        Gender: Female
        
        Name: es-PA-MargaritaNeural
        Gender: Female
        
        Name: es-PA-RobertoNeural
        Gender: Male
        
        Name: es-PE-AlexNeural
        Gender: Male
        
        Name: es-PE-CamilaNeural
        Gender: Female
        
        Name: es-PR-KarinaNeural
        Gender: Female
        
        Name: es-PR-VictorNeural
        Gender: Male
        
        Name: es-PY-MarioNeural
        Gender: Male
        
        Name: es-PY-TaniaNeural
        Gender: Female
        
        Name: es-SV-LorenaNeural
        Gender: Female
        
        Name: es-SV-RodrigoNeural
        Gender: Male
        
        Name: es-US-AlonsoNeural
        Gender: Male
        
        Name: es-US-PalomaNeural
        Gender: Female
        
        Name: es-UY-MateoNeural
        Gender: Male
        
        Name: es-UY-ValentinaNeural
        Gender: Female
        
        Name: es-VE-PaolaNeural
        Gender: Female
        
        Name: es-VE-SebastianNeural
        Gender: Male
        
        Name: et-EE-AnuNeural
        Gender: Female
        
        Name: et-EE-KertNeural
        Gender: Male
        
        Name: fa-IR-DilaraNeural
        Gender: Female
        
        Name: fa-IR-FaridNeural
        Gender: Male
        
        Name: fi-FI-HarriNeural
        Gender: Male
        
        Name: fi-FI-NooraNeural
        Gender: Female
        
        Name: fil-PH-AngeloNeural
        Gender: Male
        
        Name: fil-PH-BlessicaNeural
        Gender: Female
        
        Name: fr-BE-CharlineNeural
        Gender: Female
        
        Name: fr-BE-GerardNeural
        Gender: Male
        
        Name: fr-CA-AntoineNeural
        Gender: Male
        
        Name: fr-CA-JeanNeural
        Gender: Male
        
        Name: fr-CA-SylvieNeural
        Gender: Female
        
        Name: fr-CA-ThierryNeural
        Gender: Male
        
        Name: fr-CH-ArianeNeural
        Gender: Female
        
        Name: fr-CH-FabriceNeural
        Gender: Male
        
        Name: fr-FR-DeniseNeural
        Gender: Female
        
        Name: fr-FR-EloiseNeural
        Gender: Female
        
        Name: fr-FR-HenriNeural
        Gender: Male
        
        Name: fr-FR-RemyMultilingualNeural
        Gender: Male
        
        Name: fr-FR-VivienneMultilingualNeural
        Gender: Female
        
        Name: ga-IE-ColmNeural
        Gender: Male
        
        Name: ga-IE-OrlaNeural
        Gender: Female
        
        Name: gl-ES-RoiNeural
        Gender: Male
        
        Name: gl-ES-SabelaNeural
        Gender: Female
        
        Name: gu-IN-DhwaniNeural
        Gender: Female
        
        Name: gu-IN-NiranjanNeural
        Gender: Male
        
        Name: he-IL-AvriNeural
        Gender: Male
        
        Name: he-IL-HilaNeural
        Gender: Female
        
        Name: hi-IN-MadhurNeural
        Gender: Male
        
        Name: hi-IN-SwaraNeural
        Gender: Female
        
        Name: hr-HR-GabrijelaNeural
        Gender: Female
        
        Name: hr-HR-SreckoNeural
        Gender: Male
        
        Name: hu-HU-NoemiNeural
        Gender: Female
        
        Name: hu-HU-TamasNeural
        Gender: Male
        
        Name: id-ID-ArdiNeural
        Gender: Male
        
        Name: id-ID-GadisNeural
        Gender: Female
        
        Name: is-IS-GudrunNeural
        Gender: Female
        
        Name: is-IS-GunnarNeural
        Gender: Male
        
        Name: it-IT-DiegoNeural
        Gender: Male
        
        Name: it-IT-ElsaNeural
        Gender: Female
        
        Name: it-IT-GiuseppeNeural
        Gender: Male
        
        Name: it-IT-IsabellaNeural
        Gender: Female
        
        Name: ja-JP-KeitaNeural
        Gender: Male
        
        Name: ja-JP-NanamiNeural
        Gender: Female
        
        Name: jv-ID-DimasNeural
        Gender: Male
        
        Name: jv-ID-SitiNeural
        Gender: Female
        
        Name: ka-GE-EkaNeural
        Gender: Female
        
        Name: ka-GE-GiorgiNeural
        Gender: Male
        
        Name: kk-KZ-AigulNeural
        Gender: Female
        
        Name: kk-KZ-DauletNeural
        Gender: Male
        
        Name: km-KH-PisethNeural
        Gender: Male
        
        Name: km-KH-SreymomNeural
        Gender: Female
        
        Name: kn-IN-GaganNeural
        Gender: Male
        
        Name: kn-IN-SapnaNeural
        Gender: Female
        
        Name: ko-KR-HyunsuNeural
        Gender: Male
        
        Name: ko-KR-InJoonNeural
        Gender: Male
        
        Name: ko-KR-SunHiNeural
        Gender: Female
        
        Name: lo-LA-ChanthavongNeural
        Gender: Male
        
        Name: lo-LA-KeomanyNeural
        Gender: Female
        
        Name: lt-LT-LeonasNeural
        Gender: Male
        
        Name: lt-LT-OnaNeural
        Gender: Female
        
        Name: lv-LV-EveritaNeural
        Gender: Female
        
        Name: lv-LV-NilsNeural
        Gender: Male
        
        Name: mk-MK-AleksandarNeural
        Gender: Male
        
        Name: mk-MK-MarijaNeural
        Gender: Female
        
        Name: ml-IN-MidhunNeural
        Gender: Male
        
        Name: ml-IN-SobhanaNeural
        Gender: Female
        
        Name: mn-MN-BataaNeural
        Gender: Male
        
        Name: mn-MN-YesuiNeural
        Gender: Female
        
        Name: mr-IN-AarohiNeural
        Gender: Female
        
        Name: mr-IN-ManoharNeural
        Gender: Male
        
        Name: ms-MY-OsmanNeural
        Gender: Male
        
        Name: ms-MY-YasminNeural
        Gender: Female
        
        Name: mt-MT-GraceNeural
        Gender: Female
        
        Name: mt-MT-JosephNeural
        Gender: Male
        
        Name: my-MM-NilarNeural
        Gender: Female
        
        Name: my-MM-ThihaNeural
        Gender: Male
        
        Name: nb-NO-FinnNeural
        Gender: Male
        
        Name: nb-NO-PernilleNeural
        Gender: Female
        
        Name: ne-NP-HemkalaNeural
        Gender: Female
        
        Name: ne-NP-SagarNeural
        Gender: Male
        
        Name: nl-BE-ArnaudNeural
        Gender: Male
        
        Name: nl-BE-DenaNeural
        Gender: Female
        
        Name: nl-NL-ColetteNeural
        Gender: Female
        
        Name: nl-NL-FennaNeural
        Gender: Female
        
        Name: nl-NL-MaartenNeural
        Gender: Male
        
        Name: pl-PL-MarekNeural
        Gender: Male
        
        Name: pl-PL-ZofiaNeural
        Gender: Female
        
        Name: ps-AF-GulNawazNeural
        Gender: Male
        
        Name: ps-AF-LatifaNeural
        Gender: Female
        
        Name: pt-BR-AntonioNeural
        Gender: Male
        
        Name: pt-BR-FranciscaNeural
        Gender: Female
        
        Name: pt-BR-ThalitaNeural
        Gender: Female
        
        Name: pt-PT-DuarteNeural
        Gender: Male
        
        Name: pt-PT-RaquelNeural
        Gender: Female
        
        Name: ro-RO-AlinaNeural
        Gender: Female
        
        Name: ro-RO-EmilNeural
        Gender: Male
        
        Name: ru-RU-DmitryNeural
        Gender: Male
        
        Name: ru-RU-SvetlanaNeural
        Gender: Female
        
        Name: si-LK-SameeraNeural
        Gender: Male
        
        Name: si-LK-ThiliniNeural
        Gender: Female
        
        Name: sk-SK-LukasNeural
        Gender: Male
        
        Name: sk-SK-ViktoriaNeural
        Gender: Female
        
        Name: sl-SI-PetraNeural
        Gender: Female
        
        Name: sl-SI-RokNeural
        Gender: Male
        
        Name: so-SO-MuuseNeural
        Gender: Male
        
        Name: so-SO-UbaxNeural
        Gender: Female
        
        Name: sq-AL-AnilaNeural
        Gender: Female
        
        Name: sq-AL-IlirNeural
        Gender: Male
        
        Name: sr-RS-NicholasNeural
        Gender: Male
        
        Name: sr-RS-SophieNeural
        Gender: Female
        
        Name: su-ID-JajangNeural
        Gender: Male
        
        Name: su-ID-TutiNeural
        Gender: Female
        
        Name: sv-SE-MattiasNeural
        Gender: Male
        
        Name: sv-SE-SofieNeural
        Gender: Female
        
        Name: sw-KE-RafikiNeural
        Gender: Male
        
        Name: sw-KE-ZuriNeural
        Gender: Female
        
        Name: sw-TZ-DaudiNeural
        Gender: Male
        
        Name: sw-TZ-RehemaNeural
        Gender: Female
        
        Name: ta-IN-PallaviNeural
        Gender: Female
        
        Name: ta-IN-ValluvarNeural
        Gender: Male
        
        Name: ta-LK-KumarNeural
        Gender: Male
        
        Name: ta-LK-SaranyaNeural
        Gender: Female
        
        Name: ta-MY-KaniNeural
        Gender: Female
        
        Name: ta-MY-SuryaNeural
        Gender: Male
        
        Name: ta-SG-AnbuNeural
        Gender: Male
        
        Name: ta-SG-VenbaNeural
        Gender: Female
        
        Name: te-IN-MohanNeural
        Gender: Male
        
        Name: te-IN-ShrutiNeural
        Gender: Female
        
        Name: th-TH-NiwatNeural
        Gender: Male
        
        Name: th-TH-PremwadeeNeural
        Gender: Female
        
        Name: tr-TR-AhmetNeural
        Gender: Male
        
        Name: tr-TR-EmelNeural
        Gender: Female
        
        Name: uk-UA-OstapNeural
        Gender: Male
        
        Name: uk-UA-PolinaNeural
        Gender: Female
        
        Name: ur-IN-GulNeural
        Gender: Female
        
        Name: ur-IN-SalmanNeural
        Gender: Male
        
        Name: ur-PK-AsadNeural
        Gender: Male
        
        Name: ur-PK-UzmaNeural
        Gender: Female
        
        Name: uz-UZ-MadinaNeural
        Gender: Female
        
        Name: uz-UZ-SardorNeural
        Gender: Male
        
        Name: vi-VN-HoaiMyNeural
        Gender: Female
        
        Name: vi-VN-NamMinhNeural
        Gender: Male
        
        Name: zh-CN-XiaoxiaoNeural
        Gender: Female
        
        Name: zh-CN-XiaoyiNeural
        Gender: Female
        
        Name: zh-CN-YunjianNeural
        Gender: Male
        
        Name: zh-CN-YunxiNeural
        Gender: Male
        
        Name: zh-CN-YunxiaNeural
        Gender: Male
        
        Name: zh-CN-YunyangNeural
        Gender: Male
        
        Name: zh-CN-liaoning-XiaobeiNeural
        Gender: Female
        
        Name: zh-CN-shaanxi-XiaoniNeural
        Gender: Female
        
        Name: zh-HK-HiuGaaiNeural
        Gender: Female
        
        Name: zh-HK-HiuMaanNeural
        Gender: Female
        
        Name: zh-HK-WanLungNeural
        Gender: Male
        
        Name: zh-TW-HsiaoChenNeural
        Gender: Female
        
        Name: zh-TW-HsiaoYuNeural
        Gender: Female
        
        Name: zh-TW-YunJheNeural
        Gender: Male
        
        Name: zu-ZA-ThandoNeural
        Gender: Female
        
        Name: zu-ZA-ThembaNeural
        Gender: Male
        
        
        Name: en-US-AvaMultilingualNeural-V2
        Gender: Female
        
        Name: en-US-AndrewMultilingualNeural-V2
        Gender: Male
        
        Name: en-US-EmmaMultilingualNeural-V2
        Gender: Female
        
        Name: en-US-BrianMultilingualNeural-V2
        Gender: Male
        
        Name: de-DE-FlorianMultilingualNeural-V2
        Gender: Male
        
        Name: de-DE-SeraphinaMultilingualNeural-V2
        Gender: Female
        
        Name: fr-FR-RemyMultilingualNeural-V2
        Gender: Male
        
        Name: fr-FR-VivienneMultilingualNeural-V2
        Gender: Female
    
        Name: zh-CN-XiaoxiaoMultilingualNeural-V2
        Gender: Female
        """.strip()
        voices = []
        name = ""
        gender = ""

        for line in voices_str.split("\n"):
            line = line.strip()
            if not line:
                continue
            if line.startswith("Name: "):
                name = line[6:].strip()
            elif line.startswith("Gender: "):
                gender = line[8:].strip()
                if name and gender:
                    # 检查语言过滤
                    should_include = False
                    if filter_locals:
                        for filter_local in filter_locals:
                            if name.lower().startswith(filter_local.lower()):
                                should_include = True
                                break
                    else:
                        should_include = True

                    if should_include:
                        # 解析语言和地区
                        parts = name.split("-")
                        lang_code = parts[0] if len(parts) > 0 else "unknown"
                        region_code = parts[1] if len(parts) > 1 else "unknown"

                        voice_info = VoiceInfo(
                            name=name,
                            display_name=name,
                            language=f"{lang_code}-{region_code}"
                            if len(parts) >= 2
                            else lang_code,
                            gender=gender.lower(),
                            region=region_code,
                            engine="azure",
                            sample_rate=48000,
                            quality="high",
                        )
                        voices.append(voice_info)

                    name = ""
                    gender = ""

        voices.sort(key=lambda x: x.name)
        return voices

    @staticmethod
    def check(voice_name: str):
        if voice_name.endswith("-V2"):
            return voice_name.replace("-V2", "").strip()
        return voice_name

    def _synthesize(self, request: TTSRequest) -> TTSResponse:
        """Azure TTS语音合成核心方法

        Args:
            request: TTS请求对象

        Returns:
            TTS响应对象
        """
        start_time = time.time()

        voice_name = self.check(request.voice_name or self.get_default_voice())
        if not voice_name:
            return TTSResponse(
                success=False,
                request=request,
                error_message=f"无效的语音名称: {voice_name}",
                error_code="INVALID_VOICE",
                processing_time=time.time() - start_time,
            )

        text = request.text.strip()
        output_file = request.output_file

        if not output_file:
            import tempfile

            output_file = tempfile.mktemp(suffix=f".{request.output_format}")

        def _format_duration_to_offset(duration) -> int:
            if isinstance(duration, str):
                time_obj = datetime.strptime(duration, "%H:%M:%S.%f")
                milliseconds = (
                    (time_obj.hour * 3600000)
                    + (time_obj.minute * 60000)
                    + (time_obj.second * 1000)
                    + (time_obj.microsecond // 1000)
                )
                return milliseconds * 10000

            if isinstance(duration, int):
                return duration

            return 0

        # 创建字幕制作器
        subtitle_maker = SubtitleMaker() if request.generate_subtitles else None

        for i in range(3):
            try:
                logger.info(f"Azure TTS开始合成，语音: {voice_name}，尝试: {i + 1}")

                def speech_synthesizer_word_boundary_cb(
                    evt: speechsdk.SessionEventArgs,
                ):
                    if subtitle_maker:
                        duration = _format_duration_to_offset(str(evt.duration))
                        offset = _format_duration_to_offset(evt.audio_offset)

                        start_time = offset / 10000000.0  # 转换为秒
                        end_time = (offset + duration) / 10000000.0

                        # 添加音频片段
                        segment = AudioSegment(
                            start_time=start_time,
                            end_time=end_time,
                            text=evt.text,
                            voice_name=voice_name,
                        )
                        subtitle_maker.add_segment(segment)

                # 创建Azure语音配置
                if not self.speech_key or not self.service_region:
                    return TTSResponse(
                        success=False,
                        request=request,
                        error_message="Azure语音服务密钥或区域未配置",
                        error_code="CONFIG_ERROR",
                        processing_time=time.time() - start_time,
                    )

                audio_config = speechsdk.audio.AudioOutputConfig(
                    filename=output_file, use_default_speaker=True
                )
                speech_config = speechsdk.SpeechConfig(
                    subscription=self.speech_key, region=self.service_region
                )
                speech_config.speech_synthesis_voice_name = voice_name

                # 设置语音速率
                if request.voice_rate != 1.0:
                    rate_percent = int((request.voice_rate - 1.0) * 100)
                    rate_percent = max(-50, min(100, rate_percent))  # 限制范围
                    ssml_text = f'<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="zh-CN"><prosody rate="{rate_percent:+d}%">{text}</prosody></speak>'
                else:
                    ssml_text = text

                # 启用字幕边界事件
                if subtitle_maker:
                    speech_config.set_property(
                        property_id=speechsdk.PropertyId.SpeechServiceResponse_RequestWordBoundary,
                        value="true",
                    )

                # 设置输出格式
                if request.output_format.lower() == "wav":
                    speech_config.set_speech_synthesis_output_format(
                        speechsdk.SpeechSynthesisOutputFormat.Audio48Khz16BitMonoPcm
                    )
                else:
                    speech_config.set_speech_synthesis_output_format(
                        speechsdk.SpeechSynthesisOutputFormat.Audio48Khz192KBitRateMonoMp3
                    )
                speech_synthesizer = speechsdk.SpeechSynthesizer(
                    audio_config=audio_config, speech_config=speech_config
                )

                if subtitle_maker:
                    speech_synthesizer.synthesis_word_boundary.connect(
                        speech_synthesizer_word_boundary_cb
                    )

                # 执行合成
                if request.voice_rate != 1.0:
                    result = speech_synthesizer.speak_ssml_async(ssml_text).get()
                else:
                    result = speech_synthesizer.speak_text_async(text).get()
                if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
                    logger.success(f"Azure TTS合成成功: {output_file}")

                    # 获取音频时长
                    duration = self._get_audio_duration(output_file)

                    return TTSResponse(
                        success=True,
                        request=request,
                        audio_file=output_file,
                        subtitle_maker=subtitle_maker,
                        duration=duration,
                        voice_used=voice_name,
                        processing_time=time.time() - start_time,
                        engine_info=self.get_engine_info(),
                    )

                elif result.reason == speechsdk.ResultReason.Canceled:
                    cancellation_details = result.cancellation_details
                    error_msg = f"Azure TTS取消: {cancellation_details.reason}"
                    if (
                        cancellation_details.reason
                        == speechsdk.CancellationReason.Error
                    ):
                        error_msg += f" - {cancellation_details.error_details}"
                    logger.error(error_msg)

                    return TTSResponse(
                        success=False,
                        request=request,
                        error_message=error_msg,
                        error_code="AZURE_CANCELED",
                        processing_time=time.time() - start_time,
                    )
            except Exception as e:
                logger.error(f"Azure TTS尝试{i + 1}失败: {str(e)}")
                if i == 2:  # 最后一次尝试
                    return TTSResponse(
                        success=False,
                        request=request,
                        error_message=f"Azure TTS合成失败: {str(e)}",
                        error_code="AZURE_ERROR",
                        processing_time=time.time() - start_time,
                    )

        return TTSResponse(
            success=False,
            request=request,
            error_message="Azure TTS合成失败：所有重试均失败",
            error_code="MAX_RETRIES_EXCEEDED",
            processing_time=time.time() - start_time,
        )

    def _get_audio_duration(self, audio_file: str) -> float:
        """获取音频文件时长"""
        try:
            import subprocess

            result = subprocess.run(
                [
                    "ffprobe",
                    "-v",
                    "quiet",
                    "-show_entries",
                    "format=duration",
                    "-of",
                    "csv=p=0",
                    audio_file,
                ],
                capture_output=True,
                text=True,
                timeout=10,
            )

            if result.returncode == 0:
                return float(result.stdout.strip())
        except Exception:
            pass

        # 估算时长
        try:
            file_size = os.path.getsize(audio_file)
            # 48kHz MP3 约 192kbps = 24KB/s
            return file_size / 24000
        except Exception:
            return 0.0

    def get_engine_info(self) -> dict:
        """获取引擎信息"""
        return {
            "engine_name": "AzureTTS",
            "version": "1.0",
            "default_voice": self.default_voice,
            "supported_formats": ["wav", "mp3"],
            "max_text_length": 5000,
            "supports_ssml": True,
            "supports_subtitles": True,
        }
