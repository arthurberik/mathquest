"""
Project: MathQuest — стильный сайт с математическими уровнями
Description: Улучшенная версия с красивым интерфейсом и плавными эффектами.
"""

from flask import Flask, render_template_string, request, redirect, url_for, session
import random

app = Flask(__name__)
app.secret_key = "supersecretkey"

page = """
<!doctype html>
<html>
<head>
    <title>MathQuest — Level {{ level }}</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap');

        body {
            font-family: 'Poppins', sans-serif;
            background: linear-gradient(135deg, #667eea, #764ba2);
            height: 100vh;
            margin: 0;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #fff;
        }

        .container {
            background: rgba(255, 255, 255, 0.15);
            backdrop-filter: blur(12px);
            border-radius: 20px;
            padding: 30px 40px;
            text-align: center;
            width: 380px;
            box-shadow: 0 8px 25px rgba(0,0,0,0.25);
            animation: fadeIn 0.8s ease;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        h1 {
            margin-bottom: 10px;
            color: #fff;
        }

        p {
            font-size: 18px;
        }

        input[type=number] {
            width: 120px;
            padding: 8px;
            font-size: 18px;
            border-radius: 10px;
            border: none;
            text-align: center;
            margin-top: 10px;
        }

        button {
            margin-top: 20px;
            padding: 10px 25px;
            font-size: 18px;
            border: none;
            border-radius: 10px;
            background: linear-gradient(90deg, #00c6ff, #0072ff);
            color: white;
            cursor: pointer;
            transition: 0.3s;
        }

        button:hover {
            transform: scale(1.05);
            box-shadow: 0 0 15px rgba(0, 114, 255, 0.6);
        }

        .result {
            margin-top: 20px;
            font-size: 20px;
            font-weight: 600;
        }

        .score {
            margin-top: 8px;
            font-size: 16px;
            color: #ffe082;
        }

        a {
            display: inline-block;
            text-decoration: none;
            background: linear-gradient(90deg, #ff6a00, #ee0979);
            padding: 10px 20px;
            border-radius: 10px;
            color: white;
            margin-top: 15px;
            transition: 0.3s;
        }

        a:hover {
            transform: scale(1.05);
            box-shadow: 0 0 15px rgba(255, 106, 0, 0.5);
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🌟 MathQuest</h1>
        <h2>Level {{ level }}</h2>
        <div class="score">🏅 Score: {{ score }}</div>

        {% if not result %}
        <form method="POST">
            <p><b>Task:</b> {{a}} {{op}} {{b}} = ?</p>
            <input type="hidden" name="a" value="{{a}}">
            <input type="hidden" name="b" value="{{b}}">
            <input type="hidden" name="op" value="{{op}}">
            <input type="number" step="0.01" name="answer" required>
            <br>
            <button type="submit">Check</button>
        </form>
        {% else %}
        <div class="result">{{ result }}</div>
            {% if next_level %}
                <a href="{{ url_for('level', level=next_level) }}">Next level →</a>
            {% else %}
                <p>🎉 Congratulations! You’ve completed all levels!</p>
                <a href="{{ url_for('restart') }}">Restart</a>
            {% endif %}
        {% endif %}
    </div>
</body>
</html>
"""

# === Генерация задач ===
def generate_task(level):
    if level == 1:
        a, b = random.randint(1, 10), random.randint(1, 10)
        op = random.choice(["+", "-"])
    elif level == 2:
        a, b = random.randint(5, 20), random.randint(1, 10)
        op = random.choice(["+", "-", "*"])
    else:
        a, b = random.randint(10, 50), random.randint(1, 10)
        op = random.choice(["+", "-", "*", "/"])
    return a, b, op


@app.route("/")
def home():
    session["score"] = 0
    return redirect(url_for("level", level=1))


@app.route("/level/<int:level>", methods=["GET", "POST"])
def level(level):
    score = session.get("score", 0)
    a, b, op = generate_task(level)

    if request.method == "POST":
        a = int(request.form["a"])
        b = int(request.form["b"])
        op = request.form["op"]
        user_answer = float(request.form["answer"])

        if op == "+":
            correct = a + b
        elif op == "-":
            correct = a - b
        elif op == "*":
            correct = a * b
        else:
            correct = round(a / b, 2)

        if abs(user_answer - correct) < 0.01:
            session["score"] = score + 10
            result = f"✅ Correct! {a} {op} {b} = {correct}"
            next_level = level + 1 if level < 3 else None
        else:
            result = f"❌ Incorrect. Correct answer: {correct}"
            next_level = level
    else:
        result = None
        next_level = None

    return render_template_string(page, a=a, b=b, op=op, result=result,
                                  level=level, next_level=next_level, score=session["score"])


@app.route("/restart")
def restart():
    session.clear()
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
