with open("data/words.txt") as f:
    valid_words = set(line.strip().upper() for line in f)

def is_valid(word):
    return word.upper() in valid_words