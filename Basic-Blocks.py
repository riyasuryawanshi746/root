n = int(input("Enter number of statements: "))

code = []

for i in range(n):
    code.append(input())

leaders = set()

leaders.add(0)

for i in range(n):
    words = code[i].split()

    if "goto" in words:
        target = int(words[-1])

        if 0 <= target < n:
            leaders.add(target)

        if i + 1 < n:
            leaders.add(i + 1)

leaders = sorted(list(leaders))

print("\nLeaders are:")

for l in leaders:
    print(l, end=" ")

print("\n\nBasic Blocks:")

for i in range(len(leaders)):
    start = leaders[i]

    if i + 1 < len(leaders):
        end = leaders[i + 1] - 1
    else:
        end = n - 1

    print("\nBlock", i + 1)

    for j in range(start, end + 1):
        print(j, ":", code[j])