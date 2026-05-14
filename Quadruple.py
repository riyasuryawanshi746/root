# Quadruples and Triples from Infix Expression
def precedence(op):
    if op in ['+', '-']:
        return 1
    elif op in ['*', '/']:
        return 2
    return 0
def infix_to_postfix(expr):
    stack = []
    postfix = []
    for ch in expr:
        # operand
        if ch.isalnum():
            postfix.append(ch)
        # opening bracket
        elif ch == '(':
            stack.append(ch)
        # closing bracket
        elif ch == ')':
            while stack and stack[-1] != '(':
                postfix.append(stack.pop())
            stack.pop()
        # operator
        else:
            while (stack and
                   precedence(stack[-1]) >= precedence(ch)):
                postfix.append(stack.pop())
            stack.append(ch)
    while stack:
        postfix.append(stack.pop())
    return postfix
expr = input("Enter infix expression: ")
postfix = infix_to_postfix(expr)
print("\nPostfix Expression =", "".join(postfix))
stack = []
temp = 1
index = 0
quadruples = []
triples = []
# ---------------- GENERATE TAC ----------------
for token in postfix:
    if token in ['+', '-', '*', '/']:
        op2 = stack.pop()
        op1 = stack.pop()
        result = "t" + str(temp)
        # quadruple
        quadruples.append([token, op1, op2, result])
        # triple
        triples.append([index, token, op1, op2])
        stack.append(result)
        temp += 1
        index += 1
    else:
        stack.append(token)
print("\nQUADRUPLES")
print("Op\tArg1\tArg2\tResult")
for q in quadruples:
    print(q[0],"\t",q[1],"\t",q[2],"\t",q[3])
print("\nTRIPLES")
print("Index\tOp\tArg1\tArg2")
for t in triples:
    print(t[0],"\t",t[1],"\t",t[2],"\t",t[3])