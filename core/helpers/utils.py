import os

def debug_print(message: str, indent: int = 0, DEBUG: bool = True):
    if DEBUG:
        print(" " * indent + message)
