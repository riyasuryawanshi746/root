"""
Code depends on parsing grammar,
To write code for other grammar, study structure of code

Working : 
      1. Store Grammar as a Dictionary
      2. Store FIRST and FOLLOW as Dictionaries
      3. Rest of the code remains same for all grammars
      
"""

# ---------------- GRAMMAR ----------------
grammar = {
    'E': ['TQ'],
    'Q': ['+TQ', '#'],
    'T': ['FR'],
    'R': ['*FR', '#'],
    'F': ['(E)', 'i']
}
# ---------------- MANUAL FIRST ----------------
first = {
    'E': {'(', 'i'},
    'Q': {'+', '#'},
    'T': {'(', 'i'},
    'R': {'*', '#'},
    'F': {'(', 'i'}
}
# ---------------- MANUAL FOLLOW ----------------
follow = {
    'E': {'$', ')'},
    'Q': {'$', ')'},
    'T': {'+', '$', ')'},
    'R': {'+', '$', ')'},
    'F': {'*', '+', '$', ')'}
}
# ---------------- LL(1) TABLE GENERATION ----------------
table = {}
for nt in grammar:
    table[nt] = {}
for head in grammar:
    for prod in grammar[head]:
        first_prod = set()
        # epsilon production
        if prod == '#':
            first_prod.add('#')
        else:
            for ch in prod:
                # non-terminal
                if ch in grammar:
                    temp = first[ch]
                # terminal
                else:
                    temp = {ch}
                first_prod.update(temp - {'#'})
                if '#' not in temp:
                    break
            else:
                first_prod.add('#')
        # FIRST entries
        for terminal in first_prod - {'#'}:
            table[head][terminal] = prod
        # FOLLOW entries for epsilon
        if '#' in first_prod:
            for terminal in follow[head]:
                table[head][terminal] = '#'

# ---------------- PRINT TABLE ----------------
print("\nLL(1) Parsing Table\n")
for nt in table:
    for terminal in table[nt]:
        print("M[", nt, ",", terminal, "] =",
              nt + "->" + table[nt][terminal])

# ---------------- PARSER ----------------
stack = ['$', 'E']
inp = list(input("\nEnter expression: ") + '$')
print("\nStack\t\tInput\t\tAction")
while True:
    stack_str = "".join(stack)
    input_str = "".join(inp)
    top = stack.pop()
    current = inp[0]
    # ACCEPT
    if top == '$' and current == '$':
        print(stack_str,
              "\t\t",
              input_str,
              "\t\tAccepted")
        break
    # TERMINAL MATCH
    elif top == current:
        print(stack_str,
              "\t\t",
              input_str,
              "\t\tMatch")
        inp.pop(0)
    # NON TERMINAL
    elif top in grammar:
        if current in table[top]:
            production = table[top][current]
            print(stack_str,
                  "\t\t",
                  input_str,
                  "\t\t",
                  top + "->" + production)
            # epsilon skip
            if production != '#':
                for symbol in reversed(production):
                    stack.append(symbol)
        else:
            print(stack_str,
                  "\t\t",
                  input_str,
                  "\t\tRejected")
            break
    else:
        print(stack_str,
              "\t\t",
              input_str,
              "\t\tRejected")
        break