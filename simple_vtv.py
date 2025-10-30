import gradio as gr
import assemblyai as aai
from translate import Translator
from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs
import uuid
from pathlib import Path

def voice_to_voice(audio_file):
    #transcribe audio to text
    transcription_response = audio_transcription(audio_file)
    
    if transcription_response.status == aai.TranscriptStatus.error:
        raise gr.Error(transcription_response.error)
    
    else:
        text = transcription_response.text

        es_translation , tr_translation, ja_translation = text_translation(text)

    es_audi_path = text_to_speech (es_translation)
    tr_audi_path = text_to_speech (tr_translation)
    ja_audi_path = text_to_speech (ja_translation)
    
    es_path = Path(es_audi_path)
    tr_path = Path(tr_audi_path)
    ja_path = Path(ja_audi_path)

    return es_path, tr_path, ja_path


def audio_transcription(audio_file):
    aai.settings.api_key = "07992ff9083a4c1186997a8f7cb1266b"  # replace with env var later
    transcriber = aai.Transcriber()
    # open the local file and send bytes to AssemblyAI
    with open(audio_file, "rb") as f:
        transcription = transcriber.transcribe(f)
    return transcription






def text_translation(text):
    translator_es = Translator(from_lang="en", to_lang = "es")
    es_text = translator_es.translate(text)


    translator_tr = Translator(from_lang="en", to_lang = "tr")
    tr_text = translator_tr.translate(text)



    translator_ja = Translator(from_lang="en", to_lang = "ja")
    ja_text = translator_ja.translate(text)



    return es_text, tr_text, ja_text


def text_to_speech(text):
    client = ElevenLabs(
        api_key="sk_3ec073df858e20b1bb14924a9dbb4a319faad4e9a6017365",  # <-- make sure to add your ElevenLabs API key here
    )

    response = client.text_to_speech.convert(
        voice_id="7knVx0nyvqogrzuXOIqx",  # Adam pre-made voice
        output_format="mp3_22050_32",
        text=text,
        model_id="eleven_multilingual_v2",  # use the turbo model for low latency
        # Optional voice settings that allow you to customize the output
        voice_settings=VoiceSettings(
            stability=0.8,
            similarity_boost=0.8,
            style=0.5,
            use_speaker_boost=True,
            speed=1.0,
        ),
    )

    # Generating a unique file name for the output MP3 file
    save_file_path = f"{uuid.uuid4()}.mp3"

    # Writing the audio to a file
    with open(save_file_path, "wb") as f:
        for chunk in response:
            if chunk:
                f.write(chunk)

    print(f"{save_file_path}: A new audio file was saved successfully!")
    return save_file_path



audio_input = gr.Audio(
    sources = ["microphone"],
    type="filepath"
)


demo = gr.Interface(

    fn=voice_to_voice,
    inputs=audio_input,
    outputs= [gr.Audio(label = "Spanish"), gr.Audio(label = "Turkish"), gr.Audio(label="japanese")],
)


if __name__ == "__main__":
    demo.launch()
