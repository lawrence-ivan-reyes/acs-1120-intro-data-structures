import random
import re
import os
from .dictogram import Dictogram

class MarkovChain(dict):
    def __init__(self, source_text_path=None):
        # initializing this markovchain as a new dict and build chain from my source txt
        super(MarkovChain, self).__init__() 
        
        # setting up path to the source txt
        if source_text_path is None:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            source_text_path = os.path.join(script_dir, "data", "source_text.txt")
        
        # reading/storing source txt
        self.source_text = self.read_source_text(source_text_path)
        
        self.build_chain()
    
    def read_source_text(self, source_text):
        # read text file and split it into words
        with open(source_text) as file:
            text = file.read()
            return text.split()
    
    def find_starting_words(self):
        # find words that can start a sentence (capitalized!!)
        return [word for word in self.source_text if word[0].isupper()]
    
    def find_ending_words(self):
        # find words that can end a sentence (., !, ?) 
        return [word for word in self.source_text if word[-1] in ".!?"]
    
    def build_chain(self):
        # iterate through words (except last one)
        for i in range(len(self.source_text) - 1):
            current = self.source_text[i]  
            next_word = self.source_text[i + 1] 
            
            # initialize dictogram for current word if not present
            if current not in self:
                self[current] = Dictogram()
            
            # add next word to dictogram of possible next words
            self[current].add_count(next_word)
    
    def generate_sentence(self, max_words=10):
        # starting w capitalized word
        starting_words = self.find_starting_words()
        current = random.choice(starting_words)
        sentence = [current]
        
        # bringing in counter
        word_count = 1
        
        # for middle of sentence
        while word_count < max_words - 1:  
            # if current word not in chain or has no next words, break
            if current not in self or not self[current]:
                break
            
            # using dictogram's sample method to weight selection by freq
            current = self[current].sample()
            sentence.append(current)
            word_count += 1
            
            # stop if we hit an ending (word w punctuation)
            if current[-1] in ".!?":
                return " ".join(sentence)  
        
        # if we reached word limit but don't have punctuation ending
        if sentence and sentence[-1][-1] not in ".!?":
            # only add ending word if we haven't reached max_words yet
            if word_count < max_words:
                ending_words = self.find_ending_words()
                ending = random.choice(ending_words)
                sentence.append(ending)
        
        # clean text and return result
        result = " ".join(sentence)
        return re.sub(r"[\(\)\{\}]", "", result)

if __name__ == "__main__":
    markov = MarkovChain()

    print("Examples:")
    for i in range(5):
        print(f"\n{i+1}. {markov.generate_sentence()}")

