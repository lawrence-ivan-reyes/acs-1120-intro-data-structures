import random
import re
import os

class MarkovChain:
    def __init__(self):
        # initializing w my source text
        script_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(script_dir, "data", "source_text.txt")
        self.source_text = self.read_source_text(file_path)
        self.chain = self.build_chain()
    
    def read_source_text(self, source_text):
        # read & split
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
        # build markov chain dictionaryu
        chain = {}
        
        for i in range(len(self.source_text) - 1):
            current = self.source_text[i]
            next_word = self.source_text[i + 1]
            
            if current not in chain:
                chain[current] = []
            chain[current].append(next_word)
            
        return chain
    
    def generate_sentence(self, max_words=10):
        # generate sentence w markov chain
        try:
            # starting w capital word
            current = random.choice(self.find_starting_words())
            sentence = [current]
            
            # for the middle of sentence
            for _ in range(max_words - 2):  # -2 for start/end words
                if current not in self.chain:
                    break
                current = random.choice(self.chain[current])
                sentence.append(current)
                
                # stop if we hit an ending
                if current[-1] in ".!?":
                    break
            
            # ensure we end with punctuation!!
            if sentence[-1][-1] not in ".!?":
                ending = random.choice(self.find_ending_words())
                sentence.append(ending)
            
            # clean text
            result = " ".join(sentence)
            return re.sub(r"[\(\)\{\}]", "", result)
            
        except Exception as e:
            print(f"Error generating sentence: {e}")
            return "Could not generate sentence."

if __name__ == "__main__":
    markov = MarkovChain()

    print("Examples:")
    for i in range(5):
        print(f"\n{i+1}. {markov.generate_sentence()}")
