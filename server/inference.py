from openai import OpenAI
import os

client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=os.getenv("HF_TOKEN")
)

def run_model(symptoms: str):

    if not symptoms:
        return "No input provided"

    symptoms_lower = symptoms.lower()

    decision = ""
    urgency = ""
    advice = ""
    risk_notes = ""

    # 🧠 RULE-BASED TRIAGE (CORE LOGIC)
    if "chest pain" in symptoms_lower:
        if "breathing" in symptoms_lower:
            decision = "Emergency"
            urgency = "High"
            advice = "Call emergency services immediately"
            risk_notes = "Chest pain with breathing difficulty can indicate serious conditions like heart or lung issues."
        else:
            decision = "Emergency"
            urgency = "High"
            advice = "Seek immediate medical attention"
            risk_notes = "Chest pain alone can still be serious and should not be ignored."

    elif "fever" in symptoms_lower:
        decision = "Non-emergency"
        urgency = "Low to Moderate"
        advice = "Rest, drink fluids, and monitor temperature"
        risk_notes = "Fever is commonly caused by infections and usually resolves with rest."

    elif "headache" in symptoms_lower:
        decision = "Non-emergency"
        urgency = "Low"
        advice = "Rest and monitor symptoms"
        risk_notes = "Most headaches are not serious, but persistent or severe pain needs attention."

    elif "breathing" in symptoms_lower:
        decision = "Emergency"
        urgency = "High"
        advice = "Seek immediate medical attention"
        risk_notes = "Breathing difficulty can become life-threatening if untreated."

    else:
        decision = "Non-emergency"
        urgency = "Low"
        advice = "Monitor symptoms and rest"
        risk_notes = "Symptoms appear mild but should still be observed."

    # 🤖 LLM (DOCTOR-STYLE EXPLANATION)
    try:
        response = client.chat.completions.create(
            model="Qwen/Qwen2.5-72B-Instruct",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a calm, helpful medical assistant. "
                        "Explain in simple language so a normal patient can understand. "
                        "Avoid complex medical jargon. "
                        "Be reassuring but honest."
                    )
                },
                {
                    "role": "user",
                    "content": (
                        f"Patient symptoms: {symptoms}\n"
                        f"Risk level: {decision}\n"
                        f"Explain what might be happening and what the patient should do."
                    )
                }
            ],
            temperature=0.4,
            max_tokens=200
        )

        explanation = response.choices[0].message.content.strip()

    except Exception:
        explanation = "Based on your symptoms, this appears to be a manageable condition, but monitoring is important."

    # 🧾 FINAL CLEAN OUTPUT (UI-FRIENDLY)
    output = f"""
🧠 Medical Summary:

Patient symptoms:
👉 {symptoms}

📊 Risk Level:
👉 {decision} ({urgency})

📘 What this means:
{explanation}

⚠️ Important notes:
{risk_notes}

💡 What you should do:
👉 {advice}

🚑 When to seek immediate help:
• Symptoms get worse
• New symptoms appear
• Breathing difficulty or severe pain occurs
"""

    return output.strip()