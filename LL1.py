"""
NOTE : Only works for the given grammar S -> aS | #       This is a predictive parser
Code depends on parsing grammar,
To write code for other grammar, study structure of code
"""
stack = ["$", "S"]

inp = list(input("Enter string: ") + "$")

print("\nStack\t\tInput\t\tAction")

while True:
    stack_str = "".join(stack)

    input_str = "".join(inp)

    top = stack.pop()

    current = inp[0]

    if top == current:
        print(stack_str, "\t\t", input_str, "\t\tMatch")

        inp.pop(0)

    elif top == "S" and current == "a":
        print(stack_str, "\t\t", input_str, "\t\tS->aS")

        stack.append("S")
        stack.append("a")

    elif top == "S" and current == "$":
        print(stack_str, "\t\t", input_str, "\t\tS->#")

    elif top == "$" and current == "$":
        print(stack_str, "\t\t", input_str, "\t\tAccepted")
        break

    else:
        print(stack_str, "\t\t", input_str, "\t\tRejected")
        break