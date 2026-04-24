from fastapi import FastAPI, UploadFile, File
import shutil
import os
from faster_whisper import WhisperModel
from deep_translator import GoogleTranslator
from server.inference import run_model

app = FastAPI()

# ✅ ADD THIS HERE
@app.get("/")
def home():
    return {"message": "AI Medical Triage API is running 🚀"}

# Load once
model = WhisperModel("base", compute_type="int8")

@app.post("/analyze")
async def analyze_audio(file: UploadFile = File(...)):
    try:
        save_path = os.path.abspath("temp_audio.wav")

        # 1) Save file safely
        with open(save_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        print("Saved at:", save_path)

        # 2) Verify file really exists
        if not os.path.exists(save_path):
            return {"error": "File was not saved"}

        # 3) Verify file size
        size = os.path.getsize(save_path)
        print("File size:", size)

        if size < 1000:
            return {"error": "Audio too small / empty"}

        @app.post("/analyze-text")
        async def analyze_text(text: str):
            from deep_translator import GoogleTranslator

            translated = GoogleTranslator(source='auto', target='en').translate(text)

            ai_result = run_model(symptoms=translated)

            return {
                "original_text": text,
                "translated_text": translated,
                "ai_response": ai_result
            }

        # 4) Transcribe
        segments, _ = model.transcribe(save_path)

        text = " ".join([segment.text for segment in segments]).strip()

        if not text:
            return {"error": "No speech detected"}

        print("Detected:", text)

        # 5) Translate
        translated = GoogleTranslator(source='auto', target='en').translate(text)
        print("Translated:", translated)

        # 6) TEMP: bypass your model to isolate bug
        # ai_result = run_model(symptoms=translated)

        ai_result = run_model(symptoms=translated)

        return {
            "detected_text": text,
            "translated_text": translated,
            "ai_response": ai_result
        }

    except Exception as e:
        print("FULL ERROR:", str(e))
        return {"error": str(e)}
import uvicorn

if __name__ == "__main__":
        uvicorn.run("server.app:app", host="127.0.0.1", port=8000, reload=True)