"""
הדגמה: tool use תקני שלא שוכח את המודל.
The agent calls YOUR trained model as a tool, and the final recommendation is built
FROM the model's output (the segment). The model's result is never discarded — that is
the difference between a real prescriptive agent and "an LLM with a decorative model".

Run:  export GROQ_API_KEY=...   &&   python M4_tool_use_demo.py
(In Streamlit, read the key from st.secrets["GROQ_API_KEY"] instead of os.environ.)
"""
import json, os
from groq import Groq

client = Groq(api_key=os.environ["GROQ_API_KEY"])
MODEL = "llama-3.3-70b-versatile"            # supports tools on Groq

# --- YOUR trained model (toy stand-in). Returns a SEGMENT — the class the whole agent
# depends on. In your project this line is pipe.predict(...) on your real model. ---
SEGMENTS = {0: "עממי", 1: "בינוני", 2: "יוקרה"}
def predict_segment(price_level: int, rating: float) -> dict:
    score = price_level + (1 if rating >= 4.5 else 0)
    cluster = 2 if score >= 3 else 1 if score == 2 else 0
    return {"cluster": cluster, "segment": SEGMENTS[cluster]}

tools = [{"type": "function", "function": {
    "name": "predict_segment",
    "description": "Classifies a venue into a market segment using the trained model.",
    "parameters": {"type": "object", "properties": {
        "price_level": {"type": "integer", "description": "1=cheap .. 3=expensive"},
        "rating": {"type": "number"}}, "required": ["price_level", "rating"]}}}]

def run(user_text: str) -> str:
    messages = [
        {"role": "system", "content":
         "You recommend venues. To classify, call predict_segment. Never invent the segment."},
        {"role": "user", "content": user_text}]

    # Turn 1 — input layer: the model decides to call the tool
    r1 = client.chat.completions.create(model=MODEL, messages=messages,
                                        tools=tools, tool_choice="auto", temperature=0)
    msg = r1.choices[0].message
    tc = msg.tool_calls[0]
    args = json.loads(tc.function.arguments)

    # YOUR model runs. Its output is what the recommendation MUST be built on.
    model_out = predict_segment(**args)

    # Turn 2 — prescriptive layer: recommendation grounded in the model's segment.
    # The tool result is fed back, so the model's output is NOT forgotten.
    messages.append(msg)
    messages.append({"role": "tool", "tool_call_id": tc.id, "name": tc.function.name,
                     "content": json.dumps(model_out, ensure_ascii=False)})
    messages.append({"role": "system", "content":
        "המלץ פעולה אחת המבוססת על ה-segment שהמודל החזיר. הזכר את שם הסגמנט בתשובה."})
    r2 = client.chat.completions.create(model=MODEL, messages=messages, temperature=0)
    answer = r2.choices[0].message.content

    # Proof the model was not forgotten: its segment must appear in the recommendation.
    assert model_out["segment"] in answer, "המודל נשכח! ההמלצה לא מבוססת על פלט המודל."
    return f"[model -> {model_out['segment']}]\n{answer}"

if __name__ == "__main__":
    print(run("מסעדה בחיפה, מחירים גבוהים מאוד ודירוג 4.7. מה להמליץ?"))
