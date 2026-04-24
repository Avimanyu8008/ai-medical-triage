from fastapi import FastAPI, UploadFile, File
import shutil
import os
import whisper
from deep_translator import GoogleTranslator
from inference import run_model

app = FastAPI()

# Load once
model = whisper.load_model("base")

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

        # 4) Transcribe
        result = model.transcribe(save_path, fp16=False)
        text = result.get("text", "").strip()

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