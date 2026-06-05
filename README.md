## 🔗 Live Demo
https://ai-medical-triage.vercel.app/

🏥 AI Medical Triage

Multilingual AI-powered healthcare assistant that understands symptoms in Tamil, Hindi, and English, translates them into English, analyzes them using AI, and provides a structured medical summary with risk assessment.

🌟 Features
📝 Multilingual Symptom Analysis

Users can describe symptoms in:

Tamil 🇮🇳
Hindi 🇮🇳
English 🇬🇧

Example:

எனக்கு வயிற்று வலியும் தலைவலியும் இருக்கிறது.

Automatically translated to:

I have stomach ache and headache.
🎤 Voice Input Support

Users can upload audio recordings of symptoms.

The system:

Converts speech to text
Detects language automatically
Translates to English
Sends symptoms to the AI medical model
Returns structured medical guidance
🤖 AI Medical Analysis

The AI generates:

Medical Summary
Risk Level
Condition Explanation
Recommended Next Steps

Example:

Risk Level: Low

Possible Cause:
Mild digestive discomfort

Recommendation:
Rest, hydration, monitor symptoms
🔐 Authentication

Supports secure login using:

Google OAuth
Email Authentication

Powered by Supabase Authentication.

☁️ Cloud Deployment

Frontend and backend are deployed separately for scalability.

🏗️ Architecture
User
 │
 ▼
React Frontend (Vercel)
 │
 ▼
Supabase Authentication
 │
 ▼
FastAPI Backend (Render)
 │
 ├── Speech-to-Text
 │       ▼
 │   Faster-Whisper
 │
 ├── Translation
 │       ▼
 │   Google Translator
 │
 └── Medical AI Model
         ▼
     AI Medical Summary
🧠 AI Models Used
1. Faster-Whisper

Used for:

Speech Recognition
Audio Transcription

Model:

WhisperModel("base")

Purpose:

Audio → Text

Example:

Tamil Audio
     ↓
"எனக்கு தலைவலி"
2. Google Translator

Library:

deep-translator

Translator:

GoogleTranslator

Purpose:

Tamil/Hindi → English

Example:

எனக்கு தலைவலி
      ↓
I have headache
3. AI Medical Triage Model

Custom inference pipeline:

run_model()

Purpose:

Symptom analysis
Risk assessment
Medical summary generation
User guidance
🛠️ Tech Stack
Frontend
React
Vite
Axios
CSS
Backend
FastAPI
Uvicorn
Python
Authentication
Supabase Auth
Google OAuth
AI & NLP
Faster-Whisper
Deep Translator
Custom Medical Inference Engine
Deployment
Frontend
Vercel
Backend
Render
📂 Project Structure
MedTriageEnvs
│
├── server
│   ├── app.py
│   ├── inference.py
│   ├── requirements.txt
│   └── Dockerfile
│
├── ai-medical-ui
│   ├── src
│   ├── public
│   ├── package.json
│   └── vite.config.js
│
└── README.md
🚀 Local Setup
Clone Repository
git clone https://github.com/yourusername/ai-medical-triage.git

cd ai-medical-triage
Backend
cd server

pip install -r requirements.txt

uvicorn app:app --reload

Backend:

http://127.0.0.1:8000
Frontend
cd ai-medical-ui

npm install

npm run dev

Frontend:

http://localhost:5173
🌐 Production URLs
Frontend
https://ai-medical-triage.vercel.app
Backend
https://ai-medical-triage.onrender.com
🔄 API Endpoints
Health Check
GET /

Response:

{
  "message": "AI Medical Triage API is running 🚀"
}
Text Analysis
POST /analyze-text

Input:

Symptoms in Tamil/Hindi/English

Output:

{
  "original_text": "...",
  "translated_text": "...",
  "ai_response": "..."
}
Audio Analysis
POST /analyze

Input:

Audio File (.wav)

Output:

{
  "detected_text": "...",
  "translated_text": "...",
  "ai_response": "..."
}
🎯 Future Improvements
Real-time microphone recording
Multi-language voice responses
Medicine recommendations
Appointment booking integration
Doctor consultation escalation
Emergency detection alerts
Patient health history tracking
Personalized health monitoring
👨‍💻 Team

AI Medical Triage

Built to make preliminary healthcare guidance accessible in native languages using AI, speech recognition, translation, and cloud technologies.

## 👨‍💻 Built by

**TEAM : Attack on Titan**

## 👨‍💻 Team Members
**Avimanyu**
**Krishna**


---
