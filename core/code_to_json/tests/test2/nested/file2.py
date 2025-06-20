class Calculator:
    def __init__(self):
        self.value = 0
    
    def add(self, x):
        self.value += x
        return self.value

if __name__ == "__main__":
    calc = Calculator()
    print(calc.add(10)) 