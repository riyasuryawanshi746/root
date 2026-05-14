# Simple Shift Reduce Parser
# Grammar:

# E -> E+E
# E -> E*E
# E -> (E)
# E -> i  

# Operator precedence not enforced perfectly.
# Educational SPCC-style implementation.

stack = []

inp = input("Enter expression : ") + "$"
i = 0
print("\nStack\t\tInput\t\tAction")
while True:
    stack_str = "".join(stack)
    input_str = inp[i:]
    action = ""
    # ---------------- REDUCTIONS ----------------
    # E -> i
    if len(stack) >= 1 and stack[-1] == 'i':
        stack.pop()
        stack.append('E')
        action = "Reduce E->i"
    # E -> (E)
    elif len(stack) >= 3 and "".join(stack[-3:]) == "(E)":
        stack.pop()
        stack.pop()
        stack.pop()
        stack.append('E')
        action = "Reduce E->(E)"
        
    # E -> E+E
    elif len(stack) >= 3 and "".join(stack[-3:]) == "E+E":
        stack.pop()
        stack.pop()
        stack.pop()

        stack.append('E')

        action = "Reduce E->E+E"

    # E -> E*E
    elif len(stack) >= 3 and "".join(stack[-3:]) == "E*E":
        stack.pop()
        stack.pop()
        stack.pop()
        stack.append('E')
        action = "Reduce E->E*E"
    # ACCEPT
    elif "".join(stack) == "E" and inp[i] == "$":
        action = "Accepted"
        print(stack_str,
              "\t\t",
              input_str,
              "\t\t",
              action)
        break

    # SHIFT
    elif inp[i] != "$":

        stack.append(inp[i])

        action = "Shift " + inp[i]

        i += 1

    else:

        action = "Rejected"

        print(stack_str,
              "\t\t",
              input_str,
              "\t\t",
              action)

        break

    print("".join(stack),
          "\t\t",
          inp[i:],
          "\t\t",
          action)