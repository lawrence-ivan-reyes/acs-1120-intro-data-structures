import random
import sys

words = sys.argv[1:]

random.shuffle(words)

print(" ".join(words))
