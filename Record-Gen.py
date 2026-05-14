# H/T/E Record and Symbol Table Generation

pname = "COPY"
start = 0x1000
length = 0x0030
symtab = {
    "LOOP": 0x1003,
    "ALPHA": 0x1010,
    "BETA": 0x1020,
    "TEMP": 0x1030
}
# ---------------- H RECORD ----------------
print("\nH RECORD")
print("H^" + pname + "^" +
      format(start, '06X') + "^" +
      format(length, '06X'))
# ---------------- SYMBOL TABLE ----------------
print("\nSYMBOL TABLE")
print("Symbol\tValue")
for sym, addr in symtab.items():

    print(sym,
          "\t",
          format(addr, '06X'))

# ---------------- E RECORD ----------------

print("\nE RECORD")

print("E^" + format(start, '06X'))