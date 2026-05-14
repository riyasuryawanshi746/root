keywords = ["int", "float", "if", "else", "while"]

operators = ['+', '-', '*', '/', '=', '>', '<']

line = input("Enter code: ").split()

for word in line:
    if word in keywords:
        print(word, "-> Keyword")

    elif word.isdigit():
        print(word, "-> Number")

    elif word in operators:
        print(word, "-> Operator")

    elif word.isidentifier():
        print(word, "-> Identifier")

    else:
        print(word, "-> Unknown")