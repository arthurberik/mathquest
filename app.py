"""
Project: MathQuest — mini-site with math problems
Author: [your name]
Description: website with difficulty levels and math tasks
"""

from flask import Flask, render_template_string, request
import random

app = Flask(__name__)

# ---------------------- TEMPLATES ----------------------

difficulty_page = """
<!doctype html>
<html>
<head>
    <title>MathQuest — Difficulty</title>
    <style>
        body { font-family: Arial; background: #f0f2f5; }
        .container {
            width: 400px; margin: 80px auto; background: white;
            padding: 25px; border-radius: 10px;
            box-shadow: 0 0 10px rgba(0,0,0,0.2);
            text-align: center;
        }
        button {
            margin: 10px; padding: 10px 20px;
            font-size: 18px; border-radius: 8px;
            cursor: pointer; border: none;
            background: #4a78ff; color: white;
        }
        button:hover { background: #365bd1; }
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

game_page = """
<!doctype html>
<html>
<head>
    <title>MathQuest</title>
    <style>
        body { font-family: Arial; background: #f0f2f5; }
        .container {
            width: 400px; margin: 80px auto; background: white;
            padding: 25px; border-radius: 10px;
            box-shadow: 0 0 10px rgba(0,0,0,0.2);
        }
        h1 { text-align: center; color: #333; }
        form { text-align: center; }
        input[type=number], input[type=text] {
            width: 120px; padding: 7px; font-size: 18px;
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
            <br>
            <button type="submit">Check</button>
        </form>

        {% if result %}
        <div class="result">{{ result }}</div>
        {% endif %}

        <form method="GET" action="/">
            <button style="margin-top:20px; background:#ff5757;">Change level</button>
        </form>
    </div>
</body>
</html>
"""

# ---------------------- PROBLEM GENERATION ----------------------

def generate_problem(level):
    # LEVEL 1 – Easy addition/subtraction
    if level == 1:
        a, b = random.randint(1, 20), random.randint(1, 20)
        op = random.choice(["+", "-"])
        expr = f"{a} {op} {b}"
        correct = eval(expr)

    # LEVEL 2 – Multiplication / Division
    elif level == 2:
        a, b = random.randint(2, 12), random.randint(2, 12)
        op = random.choice(["*", "/"])
        expr = f"{a} {op} {b}"
        correct = round(eval(expr), 2)

    # LEVEL 3 – Mixed operations
    elif level == 3:
        a,b,c = random.randint(1,20), random.randint(1,20), random.randint(1,20)
        expr = f"{a} + {b} * {c}"
        correct = a + b*c

    # LEVEL 4 – Brackets
    elif level == 4:
        a,b,c = random.randint(1,20), random.randint(1,20), random.randint(1,20)
        expr = f"({a} + {b}) * {c}"
        correct = (a + b) * c

    # LEVEL 5 – Harder numeric tasks (no SymPy)
    else:
        tasks = [
            ("What is 12²?", 144),
            ("What is 15³?", 3375),
            ("Solve: 2x + 6 = 18 (find x)", 6),
            ("Simplify: (5*4) - (3*2)", 14),
            ("What is √144?", 12),
        ]
        expr, correct = random.choice(tasks)

        return expr, correct

    return expr, correct

# ---------------------- ROUTES ----------------------

@app.route("/")
def choose():
    return render_template_string(difficulty_page)

@app.route("/play", methods=["GET", "POST"])
def play():
    # POST: checking an answer
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
            result=result,
            stars="⭐" * level,
            difficulty=level
        )

    # GET: first entry after choosing difficulty
    level = int(request.args.get("difficulty", 1))
    problem, correct = generate_problem(level)

    return render_template_string(
        game_page,
        problem=problem,
        correct=correct,
        result=None,
        stars="⭐" * level,
        difficulty=level
    )


if __name__ == "__main__":
    app.run(debug=True)
