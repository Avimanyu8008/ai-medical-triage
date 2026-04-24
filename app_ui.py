import gradio as gr
from server.inference import run_model
import whisper

# ✅ Load Whisper ONLY ONCE
print("Loading Whisper model...")
model = whisper.load_model("base")
print("Whisper loaded ✅")


# 🎤 Voice handler
def handle_voice(audio):
    print("DEBUG AUDIO:", audio)
    try:
        import os
        import time
        import shutil
        from deep_translator import GoogleTranslator

        print("DEBUG AUDIO:", audio)

        if audio is None:
            return "❌ No audio received"

        # 🛑 Wait for file to fully save
        time.sleep(1)

        # 🛑 Check file exists
        if not os.path.exists(audio):
            return "❌ Audio file not found"

        # 🛑 Check file size (VERY IMPORTANT)
        if os.path.getsize(audio) < 1000:
            return "❌ Audio too small / not recorded properly"

        # 🛑 Copy to stable file
        safe_path = "temp_audio.wav"
        shutil.copy(audio, safe_path)

        print("File size:", os.path.getsize(safe_path))

        # 🎤 Transcribe
        result = model.transcribe(safe_path)
        text = result["text"]

        print("Detected:", text)

        if not text.strip():
            return "❌ Could not understand audio"

        # 🌐 Translate
        translated = GoogleTranslator(source='auto', target='en').translate(text)

        # 🧠 AI
        ai_result = run_model(symptoms=translated)

        return f"""
🗣 Detected:
{text}

🌐 English:
{translated}

🧠 AI:
{ai_result}
"""

    except Exception as e:
        return f"❌ Error: {str(e)}"


# 🧾 Text handler
def handle_text(text):
    if not text:
        return "Please enter symptoms"
    return run_model(symptoms=text)


# 🎨 UI
with gr.Blocks() as demo:
    gr.Markdown("# 🧠 AI Medical Triage System")
    gr.Markdown("Speak or type your symptoms (Tamil / Hindi / English supported)")

    with gr.Tab("🎤 Voice Input"):
        audio_input = gr.Audio(
            sources=["microphone"],
            type="filepath",  # 🔥 IMPORTANT FIX
            label="🎤 Click → Speak → Stop → Then click Analyze"
        )
        voice_output = gr.Textbox(label="AI Response")
        voice_btn = gr.Button("Analyze Voice")

        voice_btn.click(fn=handle_voice, inputs=audio_input, outputs=voice_output)

    with gr.Tab("🧾 Text Input"):
        text_input = gr.Textbox(label="Enter symptoms")
        text_output = gr.Textbox(label="AI Response")
        text_btn = gr.Button("Analyze Text")

        text_btn.click(fn=handle_text, inputs=text_input, outputs=text_output)


# 🚀 Launch app
demo.launch(debug=True)