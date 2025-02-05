"""Main script, uses other modules to generate sentences."""
from flask import Flask
from histogram import histogram
import random

app = Flask(__name__)

# TODO: Initialize your histogram, hash table, or markov chain here.
# Any code placed here will run only once, when the server starts.
hist = histogram("source_text.txt")

@app.route("/")
def home():
    """Route that returns a web page containing the generated text."""
    words = list(hist.keys())
    index = random.randint(0, len(words) - 1)
    return f"<p>{words[index]}</p>"

if __name__ == "__main__":
    """To run the Flask server, execute `python app.py` in your terminal.
       To learn more about Flask's DEBUG mode, visit
       https://flask.palletsprojects.com/en/2.0.x/server/#in-code"""
    app.run(debug=True)
