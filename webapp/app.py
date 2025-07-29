from flask import Flask, render_template, request, redirect, session, url_for
import random
import os

app = Flask(__name__)
app.secret_key = "hangman_secret_key"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)

MAX_ATTEMPTS = 6  # You can adjust this

def load_word(theme, difficulty):
    filepath = os.path.join(PROJECT_ROOT, difficulty, f"{theme}.txt")
    with open(filepath, 'r') as f:
        words = f.read().splitlines()
    return random.choice(words).strip().lower()

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/start", methods=["POST"])
def start_game():
    theme = request.form["theme"]
    difficulty = request.form["difficulty"]
    players = int(request.form["players"])
    player1 = request.form.get("player1", "Player 1")
    player2 = request.form.get("player2", "Player 2") if players == 2 else None

    word = load_word(theme, difficulty)
    display_word = ["_" if ch.isalpha() else ch for ch in word]

    session.clear()
    session["word"] = word
    session["display_word"] = display_word
    session["guessed_letters"] = []
    session["wrong_guesses"] = []
    session["max_attempts"] = MAX_ATTEMPTS
    session["theme"] = theme
    session["difficulty"] = difficulty
    session["players"] = players
    session["player1"] = player1
    session["player2"] = player2
    session["current_player"] = 1
    session["message"] = ""

    return redirect(url_for("game"))

@app.route("/game")
def game():
    current_player_name = session["player1"] if session["current_player"] == 1 else session.get("player2", session["player1"])
    return render_template(
        "game.html",
        theme=session["theme"],
        difficulty=session["difficulty"],
        display_word=" ".join(session["display_word"]),
        guessed_letters=session["guessed_letters"],
        wrong_guesses=session["wrong_guesses"],
        max_attempts=session["max_attempts"],
        current_player=current_player_name,
        message=session.get("message", "")
    )

@app.route("/guess", methods=["POST"])
def guess():
    guess = request.form["guess"].lower()
    session["message"] = ""

    if not guess.isalpha() or len(guess) != 1:
        session["message"] = "❌ Please enter a single alphabet letter."
        return redirect(url_for("game"))

    if guess in session["guessed_letters"]:
        session["message"] = f"⚠️ You've already guessed '{guess}'. Try something else."
        return redirect(url_for("game"))

    session["guessed_letters"].append(guess)

    if guess in session["word"]:
        for idx, char in enumerate(session["word"]):
            if char == guess:
                session["display_word"][idx] = guess
        session["message"] = f"✅ Good guess! '{guess}' is in the word."
    else:
        session["wrong_guesses"].append(guess)
        session["message"] = f"❌ Oops! '{guess}' is not in the word."
        if session["players"] == 2:
            session["current_player"] = 2 if session["current_player"] == 1 else 1

    if "_" not in session["display_word"]:
        return redirect("/result?won=true")

    if len(session["wrong_guesses"]) >= session["max_attempts"]:
        return redirect("/result?won=false")

    return redirect(url_for("game"))

@app.route("/result")
def result():
    won = request.args.get("won") == "true"
    return render_template("result.html", won=won, word=session["word"])

if __name__ == "__main__":
    app.run(debug=True)
