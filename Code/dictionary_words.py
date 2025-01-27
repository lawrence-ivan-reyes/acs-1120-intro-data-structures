# PSEUDOCODE
# open words file
# select desired number of random words from the words file
# combine selected words into a string
# print string

import random
import sys

def get_random_sentence(words_requested):
    with open("/usr/share/dict/words", "r") as dictionary:
        words = dictionary.read().split()
    sentence = random.sample(words, words_requested) 
    print(" ".join(sentence)) 

if __name__ == "__main__":
    get_random_sentence(int(sys.argv[1]))
