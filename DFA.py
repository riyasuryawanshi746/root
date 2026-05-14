regex = input("Enter regular expression: ")

symbols = []

for ch in regex:
    if ch.isalpha():
        symbols.append(ch)

n = len(symbols)

if n == 0:
    print("Invalid Regular Expression")

else:
    print("\nNullable = False")

    firstpos = {1}

    lastpos = {n}

    print("Firstpos =", firstpos)

    print("Lastpos =", lastpos)

    print("\nFollowpos Table")

    followpos = {}

    for i in range(1, n):
        followpos[i] = {i + 1}

    followpos[n] = set()

    for k, v in followpos.items():
        print("Followpos(", k, ") =", v)

    print("\nDFA STATES")

    state = 1

    for sym in symbols:
        print("State", state, "--", sym, "--> State", state + 1)

        state += 1
        