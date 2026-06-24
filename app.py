from flask import Flask, request
import openai
import os

app = Flask(__name__)

SYSTEM_PROMPT = """You are a judicial exam coaching assistant for Indian law. You help students preparing for APO, ADA, and other judicial services examinations.

Your personality:
- Formal yet friendly — like a strict but caring teacher
- Clear and explicit in your explanations
- Always reference exact section numbers when answering
- Give structured answers — first the direct answer, then the explanation, then the relevant section

Your focus areas:
- BNS (Bharatiya Nyaya Sanhita)
- BNSS (Bharatiya Nagarik Suraksha Sanhita)
- BSA (Bharatiya Sakshya Adhiniyam)
- IPC, CrPC, Indian Evidence Act
- Constitutional Law
- Any Indian law relevant to judicial services exams

Rules:
- Only answer questions related to Indian law and judicial exam preparation
- If asked anything outside law — politely decline and redirect to law topics
- Respond in English by default
- If the student writes in Hindi or asks for Hindi — respond in Hindi
- Always end your response with one exam tip or a related MCQ to test the student"""

@app.route("/", methods=["GET"])
def home():
    return """<!DOCTYPE html><html><head><style>body{background-color:#1a1a2e;color:white;font-family:Arial;display:flex;justify-content:center;align-items:center;height:100vh;margin:0;}.box{background-color:#16213e;padding:40px;border-radius:15px;text-align:center;width:500px;}input{width:80%;padding:10px;border-radius:8px;border:none;margin-top:20px;font-size:16px;}button{margin-top:15px;padding:10px 30px;background-color:#e94560;color:white;border:none;border-radius:8px;font-size:16px;}h1{font-size:24px;}p{color:#aaa;font-size:14px;}</style></head><body><div class="box"><h1>⚖️ Judicial Exam Assistant</h1><p>Ask anything about BNS, BNSS, BSA or Indian Law</p><form action="/ask" method="POST"><input type="text" name="question" placeholder="Type your legal question"><br><br><button type="submit">Ask</button></form></div></body></html>"""

@app.route("/ask", methods=["POST"])
def ask():
    client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    question = request.form.get("question")
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": question}
        ]
    )
    answer = response.choices[0].message.content
    answer_html = answer.replace("\n", "<br>")
    return f"""<!DOCTYPE html><html><head><style>body{{background-color:#1a1a2e;color:white;font-family:Arial;display:flex;justify-content:center;align-items:center;min-height:100vh;margin:0;padding:20px;box-sizing:border-box;}}.box{{background-color:#16213e;padding:40px;border-radius:15px;text-align:left;width:600px;line-height:1.8;}}a{{color:#e94560;display:block;text-align:center;margin-top:20px;}}</style></head><body><div class="box"><h2>⚖️ Answer</h2><p>{answer_html}</p><a href="/">Ask another question</a></div></body></html>"""

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
