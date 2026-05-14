x = 0
y = 0

moves = input("Enter moves: ")

for ch in moves:
    if ch == 'n':
        y += 1

    elif ch == 's':
        y -= 1

    elif ch == 'e':
        x += 1

    elif ch == 'w':
        x -= 1

print("Final Position =", x, y)