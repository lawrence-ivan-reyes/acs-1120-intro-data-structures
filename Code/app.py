"""Main script, uses other modules to generate sentences."""
from flask import Flask, render_template
import random
from .markov import MarkovChain

app = Flask(__name__)

# TODO: Initialize your histogram, hash table, or markov chain here.
# Any code placed here will run only once, when the server starts.
# hist = histogram("Code/data/source_text.txt") # creates histo from my source text
markov_chain = MarkovChain()

@app.route("/")
def home():
    """Route that returns a web page containing the generated text."""
    sentence = markov_chain.generate_sentence(max_words=25)
    return render_template('index.html', sentence=sentence)

@app.route("/generate")
def generate():
    """API endpoint that returns just the new sentence."""
    sentence = markov_chain.generate_sentence(max_words=25)
    return sentence

if __name__ == "__main__":
    """To run the Flask server, execute `python app.py` in your terminal.
       To learn more about Flask's DEBUG mode, visit
       https://flask.palletsprojects.com/en/2.0.x/server/#in-code"""
    app.run(debug=True)
