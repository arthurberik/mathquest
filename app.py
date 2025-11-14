"""
Project: MathQuest — mini-site with math problems
Author: [your name]
Description: website where users choose difficulty and solve math tasks
"""

from flask import Flask, render_template_string, request
import random

app = Flask(__name__)

# ---------------------- TEMPLATES ----------------------

# Difficulty selection page
difficulty_page = """
<!doctype html>
<html>
<head>
    <title>MathQuest — Difficulty</title>
    <style>
        body { font-family: Arial, sans-serif; background: #f0f2f5; }
        .container {
            width: 400px; margin: 80px auto; background: white;
            padding: 25px; border-radius: 10px;
            box-shadow: 0 0 10px rgba(0,0,0,0.2);
            text-align: center;
        }
        button {
            margin: 10px; padding: 12px 20px;
            font-size: 20px; border-radius: 10px;
            border: none; background: #4c7bff; color: white;
            cursor: pointer;
        }
        button:hover { background: #3659d1; }
        h1 { color: #333; }
    </style>
</head>
<body>
<div class="container">
    <h1>Select Difficulty</h1>
    <form method="GET" action="/play">
        {% for d in [1,2,3,4,5] %}
            <button name="difficulty" value="{{d}}">{{ "⭐" * d }}</button>
        {% endfor %}
    </form>
</div>
</body>
</html>
"""

# Problem gameplay page
game_page = """
<!doctype html>
<html>
<head>
    <title>MathQuest</title>
    <style>
        body { font-family: Arial, sans-serif; background: #f0f2f5; }
        .container {
            width: 400px; margin: 80px auto; background: white;
            padding: 25px; border-radius: 10px;
            box-shadow: 0 0 10px rgba(0,0,0,0.2);
        }
        h1 { text-align: center; color: #333; }
        form { text-align: center; }
        input[type=number] {
            width: 120px; padding: 6px; font-size: 18px;
        }
        button {
            margin-top: 10px; padding: 7px 15px;
            font-size: 16px; border-radius: 8px;
            background: #4a78ff; color: white; border: none;
            cursor: pointer;
        }
        button:hover { background: #365bd1; }
        .result {
            text-align: center; font-size: 18px;
            margin-top: 15px; padding: 10px;
            border-radius: 8px;
        }
        .back-btn {
            margin-top: 20px;
            background: #ff5b5b;
        }
        .back-btn:hover {
            background: #d94a4a;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>MathQuest {{stars}}</h1>

        <form method="POST">
            <p><b>Task:</b> {{problem}}</p>

            <input type="hidden" name="correct" value="{{correct}}">
            <input type="hidden" name="difficulty" value="{{difficulty}}">
            <input type="number" step="0.01" name="answer" required>

            <br><button type="submit">Check</button>
        </form>

        {% if result %}
        <div class="result">{{ result }}</div>
        {% endif %}

        <form method="GET" action="/">
            <button class="back-btn">Change level</button>
        </form>
    </div>
</body>
</html>
"""

# ---------------------- PROBLEM GENERATION ----------------------

def generate_problem(level):
    """
    Generates a problem depending on chosen difficulty level.
    """

    # ⭐ LEVEL 1 — addition / subtraction
    if level == 1:
        a, b = random.randint(1, 20), random.randint(1, 20)
        op = random.choice(["+", "-"])
        expr = f"{a} {op} {b}"
        return expr, eval(expr)

    # ⭐⭐ LEVEL 2 — multiplication / division
    elif level == 2:
        a, b = random.randint(2, 15), random.randint(2, 15)
        op = random.choice(["*", "/"])
        expr = f"{a} {op} {b}"
        return expr, round(eval(expr), 2)

    # ⭐⭐⭐ LEVEL 3 — multiple operations
    elif level == 3:
        a, b, c = random.randint(1, 15), random.randint(1, 15), random.randint(1, 15)
        expr = f"{a} + {b} * {c}"
        return expr, a + b * c

    # ⭐⭐⭐⭐ LEVEL 4 — parentheses
    elif level == 4:
        a, b, c = random.randint(1, 15), random.randint(1, 15), random.randint(1, 15)
        expr = f"({a} + {b}) * {c}"
        return expr, (a + b) * c

    # ⭐⭐⭐⭐⭐ LEVEL 5 — harder numeric problems (no SymPy)
    else:
        tasks = [
            ("12²", 144),
            ("√144", 12),
            ("15³", 3375),
            ("Solve 2x + 10 = 30 (x=?)", 10),
            ("(5×8) – (4×3)", 28),
        ]
        return random.choice(tasks)

# ---------------------- ROUTES ----------------------

@app.route("/")
def home():
    return render_template_string(difficulty_page)

@app.route("/play", methods=["GET", "POST"])
def play():
    # --- POST → checking an answer ---
    if request.method == "POST":
        correct = float(request.form["correct"])
        level = int(request.form["difficulty"])
        user = float(request.form["answer"])

        if abs(user - correct) < 0.01:
            result = f"✅ Correct! Answer: {correct}"
        else:
            result = f"❌ Incorrect. Correct answer: {correct}"

        problem, new_correct = generate_problem(level)
        return render_template_string(
            game_page,
            problem=problem,
            correct=new_correct,
            difficulty=level,
            stars="⭐"*level,
            result=result
        )

    # --- GET → starting the level ---
    level = int(request.args.get("difficulty", 1))
    problem, correct = generate_problem(level)

    return render_template_string(
        game_page,
        problem=problem,
        correct=correct,
        difficulty=level,
        stars="⭐"*level,
        result=None
    )


if __name__ == "__main__":
    app.run(debug=True)
