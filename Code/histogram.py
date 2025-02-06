# using dictionaries
def histogram(source_text):
    with open(source_text, 'r') as file:
        text = file.read().lower() # adding .lower() so that instances like The & the are counted as the same word

    words = text.split()
    hist = {}

    for word in words:
        cleaned_word = word.strip('.,!?:;()"') # adding bc of the minute vs. minute. issue i encountered
        if cleaned_word in hist:
            hist[cleaned_word] += 1
        else:
            hist[cleaned_word] = 1

    return hist 

def unique_words(histogram):
    return len(histogram)

def frequency(word, histogram):
    # the code below is basically saying in the histogram, look for this word, and if you don't find it, return 0
    return histogram.get(word.lower(), 0)

# testing!!!
# hist = histogram("source_text.txt")

# print("Unique words:", unique_words(hist))
# print("Times 'minutes' appears:", frequency("minutes", hist))
# print("Times 'week' appears:", frequency("week", hist))
# print("Times 'the' appears:", frequency("the", hist))
