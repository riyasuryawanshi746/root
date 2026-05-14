# Canonical LR (CLR) Parser
#
# Grammar:
#
# 1. S -> CC
# 2. C -> cC
# 3. C -> d
#
# Valid Strings:
# dd
# cdd
# ccdd
# cdcd
#
# CLR Parsing using ACTION and GOTO tables

# ---------------- ACTION TABLE ----------------

ACTION = {

    0: {'c': 'S3', 'd': 'S4'},

    1: {'$': 'ACC'},

    2: {'c': 'S6', 'd': 'S7'},

    3: {'c': 'S3', 'd': 'S4'},

    4: {'c': 'R3', 'd': 'R3'},

    5: {'$': 'R1'},

    6: {'c': 'S6', 'd': 'S7'},

    7: {'$': 'R3'},

    8: {'c': 'R2', 'd': 'R2'},

    9: {'$': 'R2'}
}

# ---------------- GOTO TABLE ----------------

GOTO = {

    0: {'S': 1, 'C': 2},

    2: {'C': 5},

    3: {'C': 8},

    6: {'C': 9}
}

# ---------------- PRODUCTIONS ----------------

productions = {

    1: ('S', 'CC'),

    2: ('C', 'cC'),

    3: ('C', 'd')
}

# ---------------- PARSER ----------------

stack = [0]

inp = list(input("Enter string: ") + '$')

print("\nStack\t\tInput\t\tAction")

while True:

    stack_str = " ".join(map(str, stack))

    input_str = "".join(inp)

    state = stack[-1]

    current = inp[0]

    # INVALID ACTION
    if current not in ACTION[state]:

        print(stack_str,
              "\t\t",
              input_str,
              "\t\tRejected")

        break

    action = ACTION[state][current]

    # ---------------- SHIFT ----------------

    if action.startswith('S'):

        next_state = int(action[1:])

        print(stack_str,
              "\t\t",
              input_str,
              "\t\tShift", current)

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
              "\t\t",
              input_str,
              "\t\tReduce",
              lhs + "->" + rhs)

    # ---------------- ACCEPT ----------------

    elif action == 'ACC':

        print(stack_str,
              "\t\t",
              input_str,
              "\t\tAccepted")

        break