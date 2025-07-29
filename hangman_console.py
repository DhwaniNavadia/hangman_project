import random
import time
import os

# 🧠 Available themes (must have .txt files in respective difficulty folders)
THEMES = [
    "fruits", "animals", "countries", "movies", "space",
    "sports", "computer_terms", "geography", "medical", "ai_ml"
]

LEADERBOARD_FILE = "leaderboard.txt"

def load_words(difficulty, theme):
    filename = os.path.join(difficulty, f"{theme}.txt")
    try:
        with open(filename, 'r') as file:
            words = file.read().splitlines()
        return words
    except FileNotFoundError:
        print(f"⚠️ Error: {filename} not found.")
        return []

def get_random_word(difficulty, theme):
    words = load_words(difficulty, theme)
    return random.choice(words).lower() if words else "python"

def display_hangman(tries):
    stages = [
        """
           ------
           |    |
           |    O
           |   /|\\
           |   / \\
           -
        """,
        """
           ------
           |    |
           |    O
           |   /|\\
           |   / 
           -
        """,
        """
           ------
           |    |
           |    O
           |   /|\\
           |    
           -
        """,
        """
           ------
           |    |
           |    O
           |   /|
           |    
           -
        """,
        """
           ------
           |    |
           |    O
           |    |
           |    
           -
        """,
        """
           ------
           |    |
           |    O
           |    
           |    
           -
        """,
        """
           ------
           |    |
           |    
           |    
           |    
           -
        """
    ]
    return stages[tries]

def save_to_leaderboard(name, score):
    with open(LEADERBOARD_FILE, "a") as f:
        f.write(f"{name} {score}\n")

def show_leaderboard():
    print("\n🏆 Leaderboard:")
    try:
        with open(LEADERBOARD_FILE, "r") as f:
            scores = [line.strip().split() for line in f.readlines()]
            scores = [(name, int(score)) for name, score in scores]
            scores.sort(key=lambda x: x[1], reverse=True)
            for i, (name, score) in enumerate(scores[:10], start=1):
                print(f"{i}. {name}: {score}")
    except FileNotFoundError:
        print("No leaderboard found yet.")

def play_game(player_name, difficulty, theme):
    word = get_random_word(difficulty, theme)
    word_completion = ["_"] * len(word)
    guessed = False
    guessed_letters = []
    guessed_words = []
    tries = 6

    start_time = time.time()
    time_limit = {"easy": 60, "medium": 45, "hard": 30}.get(difficulty, 60)

    print(f"\n🎮 {player_name}'s turn!")
    print(f"Guess the word in {time_limit} seconds!")
    print(display_hangman(tries))
    print("Word: " + " ".join(word_completion))

    while not guessed and tries > 0:
        if time.time() - start_time > time_limit:
            print("⏱️ Time's up!")
            break

        guess = input("Enter a letter or word: ").lower()
        if len(guess) == 1 and guess.isalpha():
            if guess in guessed_letters:
                print("⚠️ You already guessed that letter.")
            elif guess not in word:
                print(f"❌ {guess} is not in the word.")
                tries -= 1
                guessed_letters.append(guess)
            else:
                print(f"✅ Good guess: {guess}")
                guessed_letters.append(guess)
                for i, letter in enumerate(word):
                    if letter == guess:
                        word_completion[i] = guess
                if "_" not in word_completion:
                    guessed = True
        elif len(guess) == len(word) and guess.isalpha():
            if guess in guessed_words:
                print("⚠️ You already guessed that word.")
            elif guess != word:
                print(f"❌ {guess} is not the word.")
                tries -= 1
                guessed_words.append(guess)
            else:
                guessed = True
                word_completion = list(word)
        else:
            print("Invalid input.")

        print(display_hangman(tries))
        print("Word: " + " ".join(word_completion))

    if guessed:
        print(f"🎉 Congrats, {player_name}! You guessed the word: {word}")
        score = tries * 10
    else:
        print(f"💀 Sorry, {player_name}. The word was: {word}")
        score = 0

    print(f"Score for {player_name}: {score}")
    save_to_leaderboard(player_name, score)
    return score

def main():
    print("🎮 Welcome to Multiplayer Hangman Game 🎮")
    while True:
        mode = input("Choose mode: 1. Single-player  2. Two-player\nEnter 1 or 2: ").strip()
        if mode not in ['1', '2']:
            print("Please enter a valid choice.")
            continue

        players = []
        scores = []
        if mode == '2':
            players = [input("Enter Player 1 name: "), input("Enter Player 2 name: ")]
        else:
            players = [input("Enter your name: ")]

        difficulty = input("Choose difficulty (easy / medium / hard): ").lower()
        if difficulty not in ['easy', 'medium', 'hard']:
            print("Defaulting to 'easy'.")
            difficulty = 'easy'

        print("\nChoose a theme from the following:")
        for t in THEMES:
            print(f"- {t}")
        theme = input("Enter theme: ").lower()
        if theme not in THEMES:
            print("Invalid theme. Using 'fruits'.")
            theme = "fruits"

        for player in players:
            scores.append(play_game(player, difficulty, theme))

        print("\n🎯 Final Scores:")
        for i, player in enumerate(players):
            print(f"{player}: {scores[i]}")

        show_leaderboard()

        again = input("\nDo you want to play again? (y/n): ").lower()
        if again != 'y':
            break

if __name__ == "__main__":
    main()
