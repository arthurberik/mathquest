"""
Project: MathQuest — mini-site with math problems
Author: [your name]
Description: website where user chooses difficulty and solves math problems
"""

from flask import Flask, render_template_string, request
import random
import sympy as sp

app = Flask(__name__)

# ------------------- HTML TEMPLATES -------------------

difficulty_page = """
<!doctype html>
<html>
<head>
    <title>MathQuest — Difficulty</title>
    <style>
        body { font-family: Arial; background: #f0f2f5; }
        .container { width: 400px; margin: 80px auto; background: white; padding: 25px; border-radius: 10px; text-align:center; }
        button { padding: 10px 20px; margin: 10px; font-size: 18px; cursor:pointer; }
    </style>
</head>
<body>
<div class="container">
    <h1>Select difficulty</h1>
    <form method="GET" action="/play">
        {% for d in [1,2,3,4,5] %}
            <button name="difficulty" value="{{d}}">{{ "⭐" * d }}</button>
        {% endfor %}
    </form>
</div>
</body>
</html>
"""

play_page = """
<!doctype html>
<html>
<head>
    <title>MathQuest</title>
    <style>
        body { font-family: Arial; background: #f0f2f5; }
        .container { width: 400px; margin: 80px auto; background: white; padding: 25px; border-radius: 10px; text-align:center; }
        input[type=text] { width: 200px; padding: 5px; font-size: 16px; }
        button { margin-top: 10px; padding: 5px 15px; font-size: 16px; }
        .result { margin-top: 15px; font-size: 18px; }
    </style>
</head>
<body>
<div class="container">
    <h2>Difficulty: {{stars}}</h2>

    <form method="POST">
        <p><b>Problem:</b> {{problem_text}}</p>
        <input type="hidden" name="difficulty" value="{{difficulty}}">
        <input type="hidden" name="correct" value="{{correct}}">
        <input type="text" name="answer" required>
        <br><button type="submit">Check</button>
    </form>

    {% if result %}
    <div class="result">{{ result }}</div>
    {% endif %}
</div>
</body>
</html>
"""

# ------------------- PROBLEM GENERATION -------------------

def generate_problem(difficulty):
    if difficulty == 1:
        # Easy: + -
        a, b = random.randint(1, 20), random.randint(1, 20)
        op = random.choice(["+", "-"])
        expr = f"{a} {op} {b}"
        correct = eval(expr)

    elif difficulty == 2:
        # Medium: * /
        a, b = random.randint(2, 12), random.randint(2, 12)
        op = random.choice(["*", "/"])
        expr = f"{a} {op} {b}"
        correct = round(eval(expr), 2)

    elif difficulty == 3:
        # Harder: multiple operations
        a,b,c = random.randint(1,20), random.randint(1,20), random.randint(1,20)
        ops = random.choice(["+", "-", "*"])
        expr = f"{a} {ops} {b} * {c}"
        correct = eval(expr)

    elif difficulty == 4:
        # Very hard: brackets
        a,b,c = random.randint(1,20), random.randint(1,20), random.randint(1,20)
        expr = f"({a} + {b}) * {c}"
        correct = eval(expr)

    else:
        # Difficulty 5 — basic university math
        x = sp.symbols("x")
        tasks = [
            ("Derivative of x^3?", sp.diff(x**3, x)),
            ("Derivative of sin(x)?", sp.diff(sp.sin(x), x)),
            ("Derivative of ln(x)?", sp.diff(sp.log(x), x)),
            ("Integral of x dx?", sp.integrate(x, x)),
            ("Integral of 1/x dx?", sp.integrate(1/x, x)),
            ("Limit of sin(x)/x as x->0?", sp.limit(sp.sin(x)/x, x, 0)),
        ]
        problem_text, solution = random.choice(tasks)
        return problem_text, str(solution)

    return expr, str(correct)

# ------------------- ROUTES -------------------

@app.route("/")
def difficulty():
    return render_template_string(difficulty_page)

@app.route("/play", methods=["GET", "POST"])
def play():
    if request.method == "POST":
        user_answer = request.form["answer"].strip()
        correct = request.form["correct"].strip()
        difficulty = int(request.form["difficulty"])

        if user_answer == correct:
            result = f"✅ Correct! The answer is {correct}"
        else:
            result = f"❌ Incorrect. Correct answer: {correct}"

        problem_text, correct_answer = generate_problem(difficulty)
        return render_template_string(
            play_page,
            difficulty=difficulty,
            stars="⭐" * difficulty,
            problem_text=problem_text,
            correct=correct_answer,
            result=result,
        )

    # GET: first load after selecting difficulty
    difficulty = int(request.args.get("difficulty", 1))
    problem_text, correct = generate_problem(difficulty)

    return render_template_string(
        play_page,
        difficulty=difficulty,
        stars="⭐" * difficulty,
        problem_text=problem_text,
        correct=correct,
        result=None,
    )


if __name__ == "__main__":
    app.run(debug=True)
