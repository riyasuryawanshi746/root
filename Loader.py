program = "PROGA"

start = int("1000", 16)

extdef = ["ALPHA", "BETA"]

extref = ["X", "Y", "Z"]

statements = [
    ["FIRST", "STL"],
    ["ALPHA", "LDA"],
    ["BETA", "ADD"],
    ["END", "RSUB"]
]

n = len(statements)

locctr = start

symtab = {}

for line in statements:

    if len(line) == 2:
        label = line[0]
        symtab[label] = locctr

    locctr += 3

print("\nBLOCK TABLE")
print("DEFAULT\tStart =", format(start, '06X'),
      "Length =", format(locctr - start, '06X'))

print("\nD RECORD")

drec = "D"

for sym in extdef:
    if sym in symtab:
        drec += "^" + sym + "^" + format(symtab[sym], '06X')

print(drec)

print("\nR RECORD")

rrec = "R"

for sym in extref:
    rrec += "^" + sym

print(rrec)

print("\nLOCAL SYMBOL TABLE")
print("Symbol\tValue")

for sym, addr in symtab.items():
    print(sym, "\t", format(addr, '06X'))