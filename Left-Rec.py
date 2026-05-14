grammar = input("Enter production: ")

lhs, rhs = grammar.split("->")

productions = rhs.split("|")

alpha = []
beta = []

for prod in productions:
    if prod.startswith(lhs):
        alpha.append(prod[len(lhs):])
    else:
        beta.append(prod)

print("\nAfter Removing Left Recursion")

if alpha:
    print(lhs, "->", " | ".join([b + lhs + "'" for b in beta]))

    print(lhs + "'", "->",
          " | ".join([a + lhs + "'" for a in alpha]) + " | #")

else:
    print("No Left Recursion")

first = set()

for prod in beta:
    first.add(prod[0])

print("\nFIRST =", first)

follow = {"$"}

print("FOLLOW =", follow)