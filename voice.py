import whisper
from deep_translator import GoogleTranslator

model = whisper.load_model("base")

def process_voice(audio_path):
    result = model.transcribe(audio_path)
    text = result["text"]

    translated = GoogleTranslator(source='auto', target='en').translate(text)

    return translated