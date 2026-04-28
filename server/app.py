from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os

from faster_whisper import WhisperModel
from deep_translator import GoogleTranslator
from server.inference import run_model

app = FastAPI()   # ✅ CREATE FIRST

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://ai-medical-triage.vercel.app"],   # 🔥 keep this for now
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ✅ Health check
@app.get("/")
def home():
    return {"message": "AI Medical Triage API is running 🚀"}


# ✅ Load Whisper once
model = WhisperModel("base", compute_type="int8")


# 🎤 AUDIO ENDPOINT
@app.post("/analyze")
async def analyze_audio(file: UploadFile = File(...)):
    try:
        save_path = os.path.abspath("temp_audio.wav")

        # Save file
        with open(save_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        print("Saved at:", save_path)

        if not os.path.exists(save_path):
            return {"error": "File was not saved"}

        size = os.path.getsize(save_path)
        print("File size:", size)

        if size < 1000:
            return {"error": "Audio too small / empty"}

        # Transcribe
        segments, _ = model.transcribe(save_path)
        text = " ".join([segment.text for segment in segments]).strip()

        if not text:
            return {"error": "No speech detected"}

        print("Detected:", text)

        # Translate
        translated = GoogleTranslator(source='auto', target='en').translate(text)
        print("Translated:", translated)

        # AI
        ai_result = run_model(symptoms=translated)

        return {
            "detected_text": text,
            "translated_text": translated,
            "ai_response": ai_result
        }

    except Exception as e:
        print("FULL ERROR:", str(e))
        return {"error": str(e)}


# 🧾 TEXT ENDPOINT (🔥 CORRECTLY PLACED)
@app.post("/analyze-text")
async def analyze_text(text: str = Form(...)):
    try:
        translated = GoogleTranslator(source='auto', target='en').translate(text)

        ai_result = run_model(symptoms=translated)

        return {
            "original_text": text,
            "translated_text": translated,
            "ai_response": ai_result
        }

    except Exception as e:
        return {"error": str(e)}


# 🚀 Local run (optional)
import uvicorn

if __name__ == "__main__":
    uvicorn.run("server.app:app", host="127.0.0.1", port=8000, reload=True)