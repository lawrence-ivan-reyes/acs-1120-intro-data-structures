# new method - using lists/tuples
def histogram(source_text):
    """
    so i want to create a histogram of word frequencies from my source_text.txt file
    i then want to return a dfictionary with words as keys and their frequencies as values
    """
    with open(source_text, 'r') as file:
        text = file.read().lower() # adding .lower() so that instances like The & the are counted as the same word

    words = text.split()
    word_list = []

    cleaned_words = [word.strip('.,!?:;()"') for word in words] # adding bc of the minute vs. minute. issue i encountered
    cleaned_words.sort() # sorting words first to group identical words together

    # now to count the words
    if cleaned_words:
        current_word = cleaned_words[0]
        count = 1
        
        for word in cleaned_words[1:]:
            if word == current_word:
                count += 1
            else:
                word_list.append((current_word, count))
                current_word = word
                count = 1
        
        word_list.append((current_word, count))
    
    return word_list

def unique_words(histogram):
    # here i want to return the total count of unique words in the histogram
    return len(histogram)

def frequency(word, histogram):
    # here i want to return the frequency of a word in the histogram

    target = word.lower()
    left = 0
    right = len(histogram) - 1
    
    while left <= right:
        mid = (left + right) // 2
        current_word = histogram[mid][0]
        
        if current_word == target:
            return histogram[mid][1]
        elif current_word < target:
            left = mid + 1
        else:
            right = mid - 1
            
    return 0 



# old method - using dictionaries
def histogram(source_text):
    with open(source_text, 'r') as file:
        text = file.read().lower()

    words = text.split()
    hist = {}

    for word in words:
        cleaned_word = word.strip('.,!?:;()"') 
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
hist = histogram("source_text.txt")

print("Unique words:", unique_words(hist))
print("Times 'minutes' appears:", frequency("minutes", hist))
print("Times 'week' appears:", frequency("week", hist))
print("Times 'the' appears:", frequency("the", hist))

# print("\nAll word counts:", hist)
