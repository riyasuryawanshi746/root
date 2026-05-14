mnt = {}

mdt = []

# Hardcoded Macro Definition
macro = "INCR"

params = ["&ARG1", "&ARG2"]

macro_body = [
    "LDA &ARG1",
    "ADD &ARG2",
    "STA &ARG1"
]

# Build MDT
for line in macro_body:

    for j in range(len(params)):
        line = line.replace(params[j], "?" + str(j + 1))

    mdt.append(line)

# Store in MNT
mnt[macro] = 0

print("\nMNT")
print(mnt)

print("\nMDT")

for line in mdt:
    print(line)

# Hardcoded Macro Call
call = ["INCR", "NUM1,NUM2"]

actual = call[1].split(',')

print("\nExpanded Code")

for line in mdt:
    temp = line

    for i in range(len(actual)):
        temp = temp.replace("?" + str(i + 1), actual[i])

    print(temp)