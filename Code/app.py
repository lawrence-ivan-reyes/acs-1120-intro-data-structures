"""Main script, uses other modules to generate sentences."""
from flask import Flask
# from .histogram import histogram # adding . to import from same directory
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
    # words = list(hist.keys()) # getting all words from histo as a list
    # sentence_length = random.randint(20, 30)
    sentence = markov_chain.generate_sentence(max_words=25)

    # # generating rand words & joining w spaces
    # random_words = [words[random.randint(0, len(words) - 1)] for _ in range(sentence_length)]
    # sentence = " ".join(random_words) 

    return f"<p>{sentence}</p>"

if __name__ == "__main__":
    """To run the Flask server, execute `python app.py` in your terminal.
       To learn more about Flask's DEBUG mode, visit
       https://flask.palletsprojects.com/en/2.0.x/server/#in-code"""
    app.run(debug=True)
