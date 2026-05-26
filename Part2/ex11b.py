def calculate(number1, operator, number2):
    if operator == "+":
        return number1 + number2
    elif operator == "-":
        return number1 - number2
    elif operator == "*":
        return number1 * number2
    elif operator == "/":
        return number1 / number2
print(calculate(10, "+", 10))  # 20
print(calculate(10, "-", 10))  # 0
print(calculate(10, "*", 10))  # 100
print(calculate(10, "/", 10))  # 1.0