"""
Project: MathQuest — mini-site with math levels
Description: A Flask web app where users solve math problems and move through levels.
"""

from flask import Flask, render_template_string, request, redirect, url_for, session
import random

app = Flask(__name__)
app.secret_key = "supersecretkey"  # нужен для хранения данных сессии

# HTML-шаблон
page = """
<!doctype html>
<html>
<head>
    <title>MathQuest — Level {{ level }}</title>
    <style>
        body { font-family: Arial, sans-serif; background: #f0f2f5; }
        .container { width: 400px; margin: 80px auto; background: white; padding: 25px; border-radius: 10px;
                     box-shadow: 0 0 10px rgba(0,0,0,0.2); text-align: center; }
        h1 { color: #333; }
        input[type=number] { width: 120px; padding: 5px; font-size: 16px; }
        button { margin-top: 10px; padding: 8px 18px; font-size: 16px; }
        .result { font-size: 18px; margin-top: 15px; }
        .score { color: #007bff; margin-top: 10px; }
        a { text-decoration: none; color: white; background: #007bff; padding: 6px 12px; border-radius: 6px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Level {{ level }}</h1>
        <p><b>Score:</b> {{ score }}</p>

        {% if not result %}
        <form method="POST">
            <p><b>Task:</b> {{a}} {{op}} {{b}} = ?</p>
            <input type="hidden" name="a" value="{{a}}">
            <input type="hidden" name="b" value="{{b}}">
            <input type="hidden" name="op" value="{{op}}">
            <input type="number" step="0.01" name="answer" required>
            <br><button type="submit">Check</button>
        </form>
        {% else %}
        <div class="result">{{ result }}</div>
            {% if next_level %}
                <p><a href="{{ url_for('level', level=next_level) }}">Next level →</a></p>
            {% else %}
                <p>🎉 Congratulations! You've completed all levels!</p>
                <p><a href="{{ url_for('restart') }}">Restart</a></p>
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
    app.run(host="0.0.0.0", port=5000, debug=True)
