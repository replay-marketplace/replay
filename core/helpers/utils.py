import os

def debug_print(message: str, indent: int = 0, DEBUG: bool = True):
    if DEBUG:
        print(" " * indent + message)



# Given a string, count the number of words in the string
def count_words(string: str) -> int:
    return len(string.split())



