import random
import re
import os
import html
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
            text = self.clean_text(text)
            words = self.tokenize(text)
            return words
    
    def clean_text(self, text):
        # cxonverting html to their unique unicode equivs
        text = html.unescape(text)
        
        text = text.replace('"', '"').replace('"', '"')
        text = text.replace(''', "'").replace(''', "'")
        
        # removing unwanted formatting (like _word_ or *word*)
        text = re.sub(r'([_*])(.*?)([_*])', r'\2', text)
        
        return text
    
    def tokenize(self, text):
        # splittting whitespace to get raw tokens
        raw_tokens = re.findall(r'\S+', text)
        tokens = []
        
        # processing each raw token
        for token in raw_tokens:
            # Skip empty tokens
            if not token:
                continue
                
            # keeping certain abbrevs and contractions as is
            if re.match(r'[A-Za-z]+\.[A-Za-z]+\.', token):  # e.g. U.S.A.
                tokens.append(token)
                continue
                
            # keep hyphenated words together
            if re.search(r'[^\w\'-]', token):
                
                # keep ending punct separate while preserving hyphenated words
                if token[-1] in '.!?,;:)]}' and not token[-2:] == '."':
                    # Only add non-empty parts
                    if token[:-1]:
                        tokens.append(token[:-1])
                    tokens.append(token[-1])
                else:
                    tokens.append(token)
            else:
                tokens.append(token)
        
        # final filter to ensure no empty strings made it through
        tokens = [t for t in tokens if t]
                    
        return tokens

    def find_starting_words(self):
        # find words that can start a sentence (capitalized!!)
        return [word for word in self.source_text if word and word[0].isupper()]
    
    def find_ending_words(self):
        # find words that can end a sentence (., !, ?) 
        return [word for word in self.source_text if word and word[-1] in ".!?"]
    
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
                return self.join_sentence_parts(sentence)
        
        # if we reached word limit but don't have punctuation ending
        if sentence and sentence[-1][-1] not in ".!?":
            # only add ending word if we haven't reached max_words yet
            if word_count < max_words:
                ending_words = self.find_ending_words()
                ending = random.choice(ending_words)
                sentence.append(ending)
        
        # clean text and return result
        result = self.join_sentence_parts(sentence)
        return re.sub(r"[\(\)\{\}\"]", "", result)

    def join_sentence_parts(self, parts):
        """Join sentence parts with appropriate spacing."""
        if not parts:
            return ""
        
        result = parts[0]
        
        for i in range(1, len(parts)):
            current = parts[i]
            
            # no space before punct!!
            if current and current[0] in '.,;:!?)]}':
                result += current
            else:
                result += ' ' + current
                
        return result

if __name__ == "__main__":
    markov = MarkovChain()

    print("Examples:")
    for i in range(5):
        print(f"\n{i+1}. {markov.generate_sentence()}")

