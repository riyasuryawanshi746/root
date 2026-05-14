# SLR Parser for Expression Grammar
# Grammar:
#
# 1. E -> E+T
# 2. E -> T
# 3. T -> T*F
# 4. T -> F
# 5. F -> (E)
# 6. F -> i
# ---------------- ACTION TABLE ----------------
ACTION = {
    0: {'i': 'S5', '(': 'S4'},
    1: {'+': 'S6', '$': 'ACC'},
    2: {'+': 'R2', '*': 'S7', ')': 'R2', '$': 'R2'},
    3: {'+': 'R4', '*': 'R4', ')': 'R4', '$': 'R4'},
    4: {'i': 'S5', '(': 'S4'},
    5: {'+': 'R6', '*': 'R6', ')': 'R6', '$': 'R6'},
    6: {'i': 'S5', '(': 'S4'},
    7: {'i': 'S5', '(': 'S4'},
    8: {'+': 'S6', ')': 'S11'},
    9: {'+': 'R1', '*': 'S7', ')': 'R1', '$': 'R1'},
    10: {'+': 'R3', '*': 'R3', ')': 'R3', '$': 'R3'},
    11: {'+': 'R5', '*': 'R5', ')': 'R5', '$': 'R5'}
}
# ---------------- GOTO TABLE ----------------
GOTO = {
    0: {'E': 1, 'T': 2, 'F': 3},
    4: {'E': 8, 'T': 2, 'F': 3},
    6: {'T': 9, 'F': 3},
    7: {'F': 10}
}
# ---------------- PRODUCTIONS ----------------
productions = {
    1: ('E', 'E+T'),
    2: ('E', 'T'),
    3: ('T', 'T*F'),
    4: ('T', 'F'),
    5: ('F', '(E)'),
    6: ('F', 'i')
}
# ---------------- PARSER ----------------
stack = [0]
inp = list(input("Enter expression: ") + '$')
print("\nStack\t\t\tInput\t\t\tAction")
while True:
    stack_str = " ".join(map(str, stack))
    input_str = "".join(inp)
    state = stack[-1]
    current = inp[0]
    # INVALID
    if current not in ACTION[state]:
        print(stack_str,
              "\t\t\t",
              input_str,
              "\t\t\tRejected")
        break
    action = ACTION[state][current]
    # ---------------- SHIFT ----------------
    if action.startswith('S'):
        next_state = int(action[1:])
        print(stack_str,
              "\t\t\t",
              input_str,
              "\t\t\tShift", current)
        stack.append(current)
        stack.append(next_state)
        inp.pop(0)
    # ---------------- REDUCE ----------------
    elif action.startswith('R'):
        prod_num = int(action[1:])
        lhs, rhs = productions[prod_num]
        pop_len = 2 * len(rhs)
        for i in range(pop_len):
            stack.pop()
        top_state = stack[-1]
        stack.append(lhs)
        stack.append(GOTO[top_state][lhs])
        print(stack_str,
              "\t\t\t",
              input_str,
              "\t\t\tReduce",
              lhs + "->" + rhs)
    # ---------------- ACCEPT ----------------
    elif action == 'ACC':
        print(stack_str,
              "\t\t\t",
              input_str,
              "\t\t\tAccepted")
        break