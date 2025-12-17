from flask import Flask, render_template_string, request
import random

# Flaski rakenduse loomine
app = Flask(__name__)

# ─────────────────────────────────────────────
# 🎨 HTML MALL — RASKUSASTME VALIK
# ─────────────────────────────────────────────
# See leht võimaldab kasutajal valida mängu raskusastme (1–5)
difficulty_page = """
<!doctype html>
<html>
<head>
    <title>MathQuest — Difficulty</title>
    <style>
        /* Lehe üldine kujundus */
        body {
            margin: 0;
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #6a5af9, #8069ff, #4b9bff);
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            color: white;
        }

        /* Keskne kaart */
        .card {
            background: rgba(255, 255, 255, 0.15);
            backdrop-filter: blur(12px);
            padding: 40px;
            border-radius: 20px;
            width: 420px;
            text-align: center;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }

        /* Pealkiri */
        .title {
            font-size: 38px;
            font-weight: bold;
            margin-bottom: 20px;
        }

        /* Nupud */
        .btn {
            margin: 10px;
            padding: 12px 25px;
            font-size: 22px;
            border-radius: 12px;
            border: none;
            cursor: pointer;
            background: linear-gradient(135deg, #4aa3ff, #267fff);
            color: white;
            font-weight: bold;
        }

        .btn:hover {
            opacity: 0.9;
        }
    </style>
</head>
<body>

<div class="card">
    <div class="title">⭐️ MathQuest</div>
    <h2>Vali raskusaste</h2>

    <!-- Raskusastme valik -->
    <form method="GET" action="/play">
        {% for d in [1,2,3,4,5] %}
            <button class="btn" name="difficulty" value="{{ d }}">
                {{ "⭐️" * d }}
            </button>
        {% endfor %}
    </form>
</div>

</body>
</html>
"""

# ─────────────────────────────────────────────
# 🎨 HTML MALL — MÄNGUEKRAAN
# ─────────────────────────────────────────────
# Peamine mänguvaade: ülesanne, vastus, punktid
game_page = """
<!doctype html>
<html>
<head>
    <title>MathQuest</title>
    <style>
        body {
            margin: 0;
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #6a5af9, #8069ff, #4b9bff);
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            color: white;
        }

        .card {
            background: rgba(255, 255, 255, 0.15);
            backdrop-filter: blur(12px);
            padding: 35px;
            border-radius: 20px;
            width: 440px;
            text-align: center;
            box-shadow: 0 10px 30px rgba(0,0,0,0.25);
        }

        h1 {
            margin-top: 0;
            font-size: 32px;
            font-weight: bold;
        }

        /* Punktide kuvamine */
        .score {
            margin: 10px 0;
            font-size: 20px;
            color: #ffe58a;
        }

        p {
            font-size: 20px;
        }

        /* Vastuse sisestus */
        input[type=number] {
            margin-top: 15px;
            width: 160px;
            padding: 10px;
            font-size: 18px;
            border-radius: 10px;
            border: none;
            outline: none;
        }

        /* Üldised nupud */
        .btn {
            margin-top: 20px;
            padding: 12px 30px;
            font-size: 18px;
            border-radius: 12px;
            border: none;
            background: linear-gradient(135deg, #4aa3ff, #267fff);
            color: white;
            cursor: pointer;
            font-weight: bold;
        }

        .btn:hover {
            opacity: 0.9;
        }

        /* Tagasi nupu stiil */
        .back-btn {
            margin-top: 15px;
            background: linear-gradient(135deg, #ff6a6a, #ff4646);
        }

        /* Tulemuse tekst */
        .result {
            margin-top: 20px;
            font-size: 20px;
            font-weight: bold;
        }
    </style>
</head>
<body>

<div class="card">
    <!-- Mängu pealkiri ja raskusaste -->
    <h1>MathQuest {{ stars }}</h1>

    <!-- Punktide arv -->
    <div class="score">🎖 Score: {{ score }}</div>

    <!-- Vastuse vorm -->
    <form method="POST">
        <p><b>Ülesanne:</b> {{ problem }}</p>

        <!-- Peidetud väljad mängu oleku hoidmiseks -->
        <input type="hidden" name="correct" value="{{ correct }}">
        <input type="hidden" name="difficulty" value="{{ difficulty }}">
        <input type="hidden" name="score" value="{{ score }}">

        <input type="number" step="0.01" name="answer" required>
        <br>
        <button class="btn" type="submit">Kontrolli</button>
    </form>

    <!-- Vastuse tulemus -->
    {% if result %}
        <div class="result">{{ result }}</div>
    {% endif %}

    <!-- Raskusastme muutmine -->
    <form method="GET" action="/">
        <button class="btn back-btn">Muuda taset</button>
    </form>
</div>

</body>
</html>
"""

# ─────────────────────────────────────────────
# 🧠 ÜLESANNETE GENEREERIMINE
# ─────────────────────────────────────────────
# Loob matemaatilise ülesande vastavalt raskusastmele
def generate_problem(level):
    if level == 1:
        # Lihtne liitmine ja lahutamine
        a, b = random.randint(1, 20), random.randint(1, 20)
        op = random.choice(["+", "-"])
        expr = f"{a} {op} {b}"
        return expr, eval(expr)

    elif level == 2:
        # Korrutamine ja jagamine
        a, b = random.randint(2, 10), random.randint(2, 10)
        op = random.choice(["*", "/"])
        expr = f"{a} {op} {b}"
        return expr, round(eval(expr), 2)

    elif level == 3:
        # Tehete järjekord
        a, b, c = random.randint(1, 15), random.randint(1, 15), random.randint(1, 10)
        expr = f"{a} + {b} * {c}"
        return expr, a + b * c

    elif level == 4:
        # Sulud ja korrutamine
        a, b, c = random.randint(1, 15), random.randint(1, 15), random.randint(1, 10)
        expr = f"({a} + {b}) * {c}"
        return expr, (a + b) * c

    else:
        # Keerulisemad ja fikseeritud ülesanded
        tasks = [
            ("12²", 144),
            ("√144", 12),
            ("15³", 3375),
            ("Lahenda 2x + 10 = 30 (x=?)", 10),
            ("(5×8) – (4×3)", 28),
        ]
        return random.choice(tasks)

# ─────────────────────────────────────────────
# 🌐 ROUTE'ID
# ─────────────────────────────────────────────

# Avaleht – raskusastme valik
@app.route("/")
def home():
    return render_template_string(difficulty_page)

# Mängu loogika (GET ja POST)
@app.route("/play", methods=["GET", "POST"])
def play():
    if request.method == "POST":
        # Andmete lugemine vormist
        correct = float(request.form["correct"])
        level = int(request.form["difficulty"])
        score = int(request.form["score"])
        user_answer = float(request.form["answer"])

        # Vastuse kontroll
        if abs(user_answer - correct) < 0.01:
            score += 1
            result = "✅ Õige! +1 punkt"
        else:
            result = f"❌ Vale. Õige vastus: {correct}"

        # Uue ülesande loomine
        problem, new_correct = generate_problem(level)

        return render_template_string(
            game_page,
            problem=problem,
            correct=new_correct,
            difficulty=level,
            score=score,
            stars="⭐️" * level,
            result=result
        )

    # Esmane mängu käivitamine
    level = int(request.args.get("difficulty", 1))
    problem, correct = generate_problem(level)

    return render_template_string(
        game_page,
        problem=problem,
        correct=correct,
        difficulty=level,
        score=0,
        stars="⭐️" * level,
        result=None
    )

# Rakenduse käivitamine
if __name__ == "__main__":
    app.run()
