from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os

from faster_whisper import WhisperModel
from deep_translator import GoogleTranslator
from inference import run_model

app = FastAPI()

# ✅ FIXED CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://ai-medical-triage.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "AI Medical Triage API is running 🚀"}

# load model once
model = WhisperModel("base", compute_type="int8")

@app.post("/analyze")
async def analyze_audio(file: UploadFile = File(...)):
    try:
        save_path = os.path.abspath("temp_audio.wav")

        with open(save_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        segments, _ = model.transcribe(save_path)
        text = " ".join([s.text for s in segments]).strip()

        if not text:
            return {"error": "No speech detected"}

        translated = GoogleTranslator(source='auto', target='en').translate(text)
        ai_result = run_model(symptoms=translated)

        return {
            "detected_text": text,
            "translated_text": translated,
            "ai_response": ai_result
        }

    except Exception as e:
        return {"error": str(e)}

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

# ✅ FIXED RUN
import uvicorn

if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)