import gradio as gr
import requests
from deep_translator import GoogleTranslator

AUDIO_API = "https://ai-medical-triage.onrender.com/analyze"
TEXT_API = "https://ai-medical-triage.onrender.com/analyze-text"


# 🧹 Clean + improve AI response
def format_ai_response(text):
    if not text:
        return "⚠️ AI did not return a response"

    text = text.replace("[START]", "").replace("[END]", "").strip()

    # Better readability
    text = text.replace("Step 1:", "\n🔹 Step 1:")
    text = text.replace("Step 2:", "\n🔹 Step 2:")
    text = text.replace("Explanation:", "\n📘 Explanation:")
    text = text.replace("Final:", "\n🚨 Final:")
    text = text.replace("Advice:", "\n💡 Advice:")

    return text.strip()


# 🎤 AUDIO FUNCTION
def analyze_audio(audio):
    if audio is None:
        return "❌ No audio", "", ""

    try:
        with open(audio, "rb") as f:
            res = requests.post(
                AUDIO_API,
                files={"file": ("audio.wav", f, "audio/wav")}
            )

        data = res.json()
        print("AUDIO DEBUG:", data)

        if "error" in data:
            return "", "", f"❌ {data['error']}"

        return (
            data.get("detected_text", ""),
            data.get("translated_text", ""),
            format_ai_response(data.get("ai_response"))
        )

    except Exception as e:
        return "", "", f"❌ Error: {str(e)}"


# 🧾 TEXT FUNCTION (FIXED)
def analyze_text(text):
    if not text:
        return "", "", "❌ Please enter symptoms"

    try:
        res = requests.post(
            TEXT_API,
            data={"text": text}
        )

        data = res.json()
        print("TEXT DEBUG:", data)

        if "error" in data:
            return "", "", f"❌ {data['error']}"

        return (
            data.get("original_text", ""),
            data.get("translated_text", ""),
            format_ai_response(data.get("ai_response"))
        )

    except Exception as e:
        return "", "", f"❌ Error: {str(e)}"


# 🎨 UI
with gr.Blocks(theme=gr.themes.Soft()) as demo:

    gr.Markdown("""
    # 🏥 AI Medical Triage System
    ### 🎤 Speak OR ✍️ Type your symptoms (Tamil / Hindi / English)
    """)

    with gr.Tabs():

        # 🎤 VOICE TAB
        with gr.Tab("🎤 Voice Input"):
            audio_input = gr.Audio(
                sources=["microphone", "upload"],
                type="filepath",
                label="🎤 Record or Upload your symptoms"
            )

            voice_btn = gr.Button("🔍 Analyze Voice", variant="primary")

            with gr.Row():
                detected = gr.Textbox(label="🎤 Detected Speech")
                translated = gr.Textbox(label="🌍 English Translation")

            ai_voice = gr.Textbox(label="🧠 AI Medical Advice", lines=10)

            voice_btn.click(
                analyze_audio,
                inputs=audio_input,
                outputs=[detected, translated, ai_voice]
            )

        # 🧾 TEXT TAB
        with gr.Tab("🧾 Text Input"):
            text_input = gr.Textbox(
                label="✍️ Type symptoms (any language)",
                lines=3
            )

            text_btn = gr.Button("🔍 Analyze Text", variant="primary")

            with gr.Row():
                detected_text = gr.Textbox(label="📝 Original")
                translated_text = gr.Textbox(label="🌍 English")

            ai_text = gr.Textbox(label="🧠 AI Medical Advice", lines=10)

            text_btn.click(
                analyze_text,
                inputs=text_input,
                outputs=[detected_text, translated_text, ai_text]
            )

demo.launch()