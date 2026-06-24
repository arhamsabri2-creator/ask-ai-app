from flask import Flask, request
import openai
import os

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return """<!DOCTYPE html><html><head><style>body{background-color:#1a1a2e;color:white;font-family:Arial;display:flex;justify-content:center;align-items:center;height:100vh;margin:0;}.box{background-color:#16213e;padding:40px;border-radius:15px;text-align:center;width:500px;}input{width:80%;padding:10px;border-radius:8px;border:none;margin-top:20px;font-size:16px;}button{margin-top:15px;padding:10px 30px;background-color:#e94560;color:white;border:none;border-radius:8px;font-size:16px;}</style></head><body><div class="box"><h1>Ask AI Anything</h1><form action="/ask" method="POST"><input type="text" name="question" placeholder="Type your question"><br><br><button type="submit">Ask</button></form></div></body></html>"""

@app.route("/ask", methods=["POST"])
def ask():
    client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    question = request.form.get("question")
    response = client.chat.completions.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": question}])
    answer = response.choices[0].message.content
    return f"""<!DOCTYPE html><html><head><style>body{{background-color:#1a1a2e;color:white;font-family:Arial;display:flex;justify-content:center;align-items:center;height:100vh;margin:0;}}.box{{background-color:#16213e;padding:40px;border-radius:15px;text-align:center;width:500px;}}a{{color:#e94560;}}</style></head><body><div class="box"><h1>Answer</h1><p>{answer}</p><a href="/">Ask another question</a></div></body></html>"""

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
