from flask import Flask, request
import openai
import os

app = Flask(__name__)

TOPICS = [
    "Bharatiya Nyaya Sanhita (BNS) 2023",
    "Bharatiya Nagarik Suraksha Sanhita (BNSS) 2023",
    "Bharatiya Sakshya Adhiniyam (BSA) 2023",
    "Indian Penal Code (IPC) 1860",
    "Code of Criminal Procedure (CrPC) 1973",
    "Indian Evidence Act 1872",
    "Constitution of India",
    "Law of Torts",
    "Contract Act 1872",
    "Transfer of Property Act 1882"
]

def get_system_prompt(difficulty):
    base = """You are a judicial exam coaching assistant for Indian law. You help students preparing for APO, ADA, and other judicial services examinations.
Your personality: formal yet friendly — like a strict but caring teacher.
Rules:
- Only answer questions related to Indian law and judicial exam preparation
- Always reference exact section numbers when answering
- Give structured answers — direct answer first — then explanation — then relevant section
- End your response with one exam tip or a related MCQ"""
    if difficulty == "beginner":
        return base + "\n\nDifficulty: BEGINNER — Use very simple language. Avoid complex legal jargon. Explain as if teaching a first year law student. Use analogies and simple examples."
    elif difficulty == "advanced":
        return base + "\n\nDifficulty: ADVANCED — Use precise legal terminology. Include exceptions, provisos, and landmark case references where relevant. Ask a tricky MCQ at the end with a nuanced correct answer."
    else:
        return base + "\n\nDifficulty: INTERMEDIATE — Standard judicial exam level. Balance between simplicity and technical accuracy."

@app.route("/", methods=["GET"])
def home():
    topics_options = ""
    for topic in TOPICS:
        topics_options += f'<option value="{topic}">{topic}</option>'
    return f"""<!DOCTYPE html><html><head><style>
body{{background-color:#1a1a2e;color:white;font-family:Arial;display:flex;justify-content:center;align-items:center;min-height:100vh;margin:0;padding:20px;box-sizing:border-box;}}
.box{{background-color:#16213e;padding:40px;border-radius:15px;text-align:center;width:550px;}}
h1{{color:#e94560;font-size:26px;}}
p{{color:#aaa;font-size:13px;}}
select{{width:90%;padding:10px;border-radius:8px;border:none;margin-top:15px;font-size:15px;background:#0f3460;color:white;}}
input{{width:85%;padding:10px;border-radius:8px;border:none;margin-top:15px;font-size:15px;}}
.difficulty{{display:flex;gap:10px;justify-content:center;margin-top:15px;}}
.diff-btn{{padding:10px 20px;border:2px solid #e94560;background:transparent;color:white;border-radius:8px;cursor:pointer;font-size:14px;}}
.diff-btn.selected{{background:#e94560;}}
button[type=submit]{{margin-top:20px;padding:12px 40px;background-color:#e94560;color:white;border:none;border-radius:8px;font-size:16px;cursor:pointer;width:90%;}}
label{{display:block;text-align:left;margin-top:15px;color:#aaa;font-size:13px;width:90%;margin-left:auto;margin-right:auto;}}
</style>
<script>
function selectDifficulty(level){{
    document.getElementById("difficulty").value = level;
    document.querySelectorAll(".diff-btn").forEach(btn => btn.classList.remove("selected"));
    document.getElementById("btn-"+level).classList.add("selected");
}}
window.onload = function(){{ selectDifficulty("intermediate"); }}
</script>
</head><body><div class="box">
<h1>⚖️ Judicial Exam Assistant</h1>
<p>Ask anything about Indian law — powered by AI</p>
<form action="/ask" method="POST">
<label>Select Topic</label>
<select name="topic">
{topics_options}
</select>
<label>Your Question</label>
<input type="text" name="question" placeholder="e.g. What is the punishment for murder?">
<label>Difficulty Level</label>
<div class="difficulty">
<button type="button" class="diff-btn" id="btn-beginner" onclick="selectDifficulty('beginner')">🟢 Beginner</button>
<button type="button" class="diff-btn" id="btn-intermediate" onclick="selectDifficulty('intermediate')">🟡 Intermediate</button>
<button type="button" class="diff-btn" id="btn-advanced" onclick="selectDifficulty('advanced')">🔴 Advanced</button>
</div>
<input type="hidden" name="difficulty" id="difficulty" value="intermediate">
<button type="submit">Ask</button>
</form></div></body></html>"""

@app.route("/ask", methods=["POST"])
def ask():
    question = request.form.get("question")
    topic = request.form.get("topic")
    difficulty = request.form.get("difficulty")
    client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    system_prompt = get_system_prompt(difficulty)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Topic: {topic}\n\nQuestion: {question}"}
        ]
    )
    answer = response.choices[0].message.content
    answer_html = answer.replace("\n", "<br>")
    difficulty_label = {"beginner": "🟢 Beginner", "intermediate": "🟡 Intermediate", "advanced": "🔴 Advanced"}.get(difficulty, "Intermediate")
    return f"""<!DOCTYPE html><html><head><style>
body{{background-color:#1a1a2e;color:white;font-family:Arial;display:flex;justify-content:center;align-items:center;min-height:100vh;margin:0;padding:20px;box-sizing:border-box;}}
.box{{background-color:#16213e;padding:40px;border-radius:15px;text-align:left;width:600px;line-height:1.8;}}
h2{{color:#e94560;}}
.meta{{color:#aaa;font-size:13px;margin-bottom:20px;}}
.answer{{font-size:15px;line-height:1.8;}}
a{{color:#e94560;display:block;text-align:center;margin-top:20px;font-size:15px;}}
</style></head><body><div class="box">
<h2>⚖️ Answer</h2>
<div class="meta">Topic: {topic} &nbsp;|&nbsp; Difficulty: {difficulty_label}</div>
<div class="answer">{answer_html}</div>
<a href="/">← Ask Another Question</a>
</div></body></html>"""

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
