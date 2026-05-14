"""
============================================================
  SPCC LAB ESE - CORRECTED CODES (As per Sir's Notice)
============================================================

NOTICE SAYS:
  Exp 2  : Lexical Analyser - recognise subset of tokens (identifiers,
           reserved words, numbers, operators) for C or Python
  Exp 3  : Left Recursion Removal + FIRST/FOLLOW (only doable parts
           may be asked - e.g. only FIRST, or only remove recursion)
  Exp 4  : LL(1)/LR(1) Parser - prepare table ON PAPER manually,
           encode in program, use STACK to accept/reject string.
           Program works for THAT SPECIFIC grammar only.
  Exp 5  : ICG - accept POSTFIX expression directly, generate
           Quadruples and Triples (infix->postfix may also be asked)
  Exp 7  : Code Generation - input TAC, find number of basic blocks,
           print all statements in each basic block
  Exp 8  : SIC Assembler - generate H record, E record,
           Symbol Table (Symbol name | Value). 
           (Notice does NOT mention T record for assembler exam)
  Exp 9  : Macroprocessor - given .asm file generate DEFTAB and NAMETAB
  Exp 10 : SIC Program Blocks - identify blocks, generate Block Table
  Exp 11 : Linking Loader -
           Task 1: Generate D record, R record
           Task 2: Local Symbol Table (symbol name | value)
           (Sample given in notice with EXTDEF, EXTREF)
============================================================
"""

# ============================================================
# EXP 2: LEXICAL ANALYSER
# Recognise: keywords, identifiers, numbers, operators
# Sir says: recognise a SUBSET - e.g. only identifiers + few keywords
# ============================================================

import re

def exp2_lexical_analyser():
    # C Language keywords (Odd UID) - can be reduced in exam
    keywords = {'int', 'float', 'if', 'else', 'while', 'for',
                'return', 'void', 'char', 'double', 'switch', 'break'}

    token_patterns = [
        ('NUMBER',     r'\b\d+(\.\d+)?\b'),
        ('KEYWORD',    r'\b(?:' + '|'.join(keywords) + r')\b'),
        ('IDENTIFIER', r'\b[a-zA-Z_]\w*\b'),
        ('OPERATOR',   r'[+\-*/=<>!&|]+'),
        ('PUNCTUATION',r'[(){};,]'),
        ('WHITESPACE', r'\s+'),
    ]
    master = '|'.join(f'(?P<{n}>{p})' for n, p in token_patterns)

    code = input("Enter C code / expression: ")
    print(f"\n{'TOKEN TYPE':<15} {'VALUE'}")
    print("-" * 30)
    for m in re.finditer(master, code):
        kind, val = m.lastgroup, m.group()
        if kind != 'WHITESPACE':
            print(f"{kind:<15} {val}")


# ============================================================
# EXP 3: LEFT RECURSION REMOVAL + FIRST + FOLLOW
# Sir says: only doable parts may be asked
# All three parts are here; in exam use whichever is asked
# ============================================================

def exp3_left_recursion_and_first_follow():

    def remove_left_recursion(grammar):
        new_g = {}
        nts = list(grammar.keys())
        for i, A in enumerate(nts):
            # Substitute earlier NTs
            for j in range(i):
                B = nts[j]
                new_prods = []
                for prod in grammar[A]:
                    if prod[0] == B:
                        for bp in new_g[B]:
                            new_prods.append(bp + prod[1:])
                    else:
                        new_prods.append(prod)
                grammar[A] = new_prods
            # Eliminate immediate left recursion
            alpha, beta = [], []
            for prod in grammar[A]:
                if prod[0] == A:
                    alpha.append(prod[1:])
                else:
                    beta.append(prod)
            if alpha:
                A1 = A + "'"
                new_g[A]  = [b + [A1] for b in beta] or [['ε', A1]]
                new_g[A1] = [a + [A1] for a in alpha] + [['ε']]
            else:
                new_g[A] = grammar[A]
        return new_g

    def compute_first(grammar):
        first = {nt: set() for nt in grammar}
        changed = True
        while changed:
            changed = False
            for nt, prods in grammar.items():
                for prod in prods:
                    for sym in prod:
                        if sym == 'ε':
                            if 'ε' not in first[nt]:
                                first[nt].add('ε'); changed = True
                            break
                        elif sym not in grammar:
                            if sym not in first[nt]:
                                first[nt].add(sym); changed = True
                            break
                        else:
                            before = len(first[nt])
                            first[nt] |= (first[sym] - {'ε'})
                            if len(first[nt]) != before: changed = True
                            if 'ε' not in first[sym]: break
                    else:
                        if 'ε' not in first[nt]:
                            first[nt].add('ε'); changed = True
        return first

    def compute_follow(grammar, first, start):
        follow = {nt: set() for nt in grammar}
        follow[start].add('$')
        changed = True
        while changed:
            changed = False
            for nt, prods in grammar.items():
                for prod in prods:
                    for i, sym in enumerate(prod):
                        if sym in grammar:
                            rest = prod[i+1:]
                            before = len(follow[sym])
                            eps = True
                            for r in rest:
                                if r not in grammar:
                                    follow[sym].add(r); eps = False; break
                                follow[sym] |= (first[r] - {'ε'})
                                if 'ε' not in first[r]: eps = False; break
                            else:
                                eps = True
                            if eps:
                                follow[sym] |= follow[nt]
                            if len(follow[sym]) != before: changed = True
        return follow

    n = int(input("Enter number of productions: "))
    print("Enter each as:  E -> E + T | T")
    grammar = {}
    for _ in range(n):
        line = input().replace(' ', '')
        lhs, rhs = line.split('->')
        grammar[lhs] = [list(p) for p in rhs.split('|')]

    start = list(grammar.keys())[0]

    print("\n--- After Left Recursion Removal ---")
    new_g = remove_left_recursion(dict(grammar))
    for nt, prods in new_g.items():
        print(f"  {nt} -> {' | '.join(' '.join(p) for p in prods)}")

    first  = compute_first(new_g)
    follow = compute_follow(new_g, first, start)

    print(f"\n{'NT':<8} {'FIRST':<25} {'FOLLOW'}")
    print("-" * 55)
    for nt in new_g:
        f  = "{ " + ", ".join(sorted(first[nt]))  + " }"
        fo = "{ " + ", ".join(sorted(follow[nt])) + " }"
        print(f"  {nt:<8} {f:<25} {fo}")


# ============================================================
# EXP 4: LL(1) PARSER SIMULATION
#
# SIR SAYS:
#   - Teacher gives grammar
#   - Student manually prepares parse table ON PAPER
#   - Encode that table in program
#   - Use stack to accept/reject given string
#   - Program works for THAT specific grammar ONLY
#
# Parse table below is for standard arithmetic grammar:
#   E  -> T E'
#   E' -> + T E' | ε
#   T  -> F T'
#   T' -> * F T' | ε
#   F  -> ( E ) | id
#
# In exam: change table dict to match your given grammar
# ============================================================

def exp4_ll1_parser():
    # ---- PARSE TABLE (change this for your exam grammar) ----
    # Key: (NonTerminal, terminal) -> production as list
    table = {
        ('E',  'id'): ['T', "E'"],
        ('E',  '(' ): ['T', "E'"],
        ("E'", '+' ): ['+', 'T', "E'"],
        ("E'", ')' ): ['ε'],
        ("E'", '$' ): ['ε'],
        ('T',  'id'): ['F', "T'"],
        ('T',  '(' ): ['F', "T'"],
        ("T'", '+' ): ['ε'],
        ("T'", '*' ): ['*', 'F', "T'"],
        ("T'", ')' ): ['ε'],
        ("T'", '$' ): ['ε'],
        ('F',  'id'): ['id'],
        ('F',  '(' ): ['(', 'E', ')'],
    }
    # ---- Grammar START symbol ----
    START = 'E'
    # ---------------------------------------------------------

    inp = input("Enter tokens separated by space (end with $): ").split()
    stack = ['$', START]
    idx = 0

    print(f"\n{'STACK':<30} {'INPUT':<25} {'ACTION'}")
    print("-" * 70)

    while stack:
        top  = stack[-1]
        curr = inp[idx] if idx < len(inp) else '$'
        stk_str = ' '.join(reversed(stack))
        inp_str = ' '.join(inp[idx:])

        if top == '$' and curr == '$':
            print(f"{stk_str:<30} {inp_str:<25} ✅ ACCEPTED")
            break
        elif top == curr:
            print(f"{stk_str:<30} {inp_str:<25} Match '{curr}'")
            stack.pop(); idx += 1
        elif top in table.get('_terminals', set()) or top not in [k[0] for k in table]:
            print(f"{stk_str:<30} {inp_str:<25} ❌ ERROR - unexpected '{curr}'")
            break
        elif (top, curr) in table:
            prod = table[(top, curr)]
            print(f"{stk_str:<30} {inp_str:<25} {top} -> {' '.join(prod)}")
            stack.pop()
            if prod != ['ε']:
                stack.extend(reversed(prod))
        else:
            print(f"{stk_str:<30} {inp_str:<25} ❌ ERROR - no rule for ({top}, {curr})")
            break


# ============================================================
# EXP 5: INTERMEDIATE CODE GENERATION
#
# SIR SAYS:
#   - Accept POSTFIX (or prefix) expression
#   - Represent using Quadruples and Triples
#   - Infix to postfix conversion may also be asked before this
#
# So: first do infix->postfix, then generate quads & triples
# ============================================================

def exp5_intermediate_code():
    precedence = {'=': 0, '+': 1, '-': 1, '*': 2, '/': 2}

    def infix_to_postfix(expr):
        tokens = expr.split()
        output, stack = [], []
        for t in tokens:
            if t == '(':
                stack.append(t)
            elif t == ')':
                while stack and stack[-1] != '(':
                    output.append(stack.pop())
                stack.pop()
            elif t in precedence:
                while (stack and stack[-1] != '(' and
                       stack[-1] in precedence and
                       precedence[stack[-1]] >= precedence[t]):
                    output.append(stack.pop())
                stack.append(t)
            else:
                output.append(t)   # operand
        while stack:
            output.append(stack.pop())
        return output

    def postfix_to_tac(postfix):
        stack = []
        quads, triples = [], []
        count = [1]

        def tmp():
            t = f"t{count[0]}"; count[0] += 1; return t

        for sym in postfix:
            if sym in precedence:
                r = stack.pop()
                l = stack.pop()
                t = tmp()
                quads.append((sym, l, r, t))
                triples.append((sym, l, r))
                stack.append(t)
            else:
                stack.append(sym)
        return quads, triples

    # Step 1: Infix -> Postfix
    infix = input("Enter INFIX expression (space-separated, e.g. a = b + c * d): ")
    postfix = infix_to_postfix(infix)
    print("\nPostfix:", ' '.join(postfix))

    # Step 2: Also allow direct postfix input
    use_direct = input("\nDirectly enter postfix instead? (y/n): ").strip().lower()
    if use_direct == 'y':
        postfix = input("Enter POSTFIX (space-separated): ").split()

    # Step 3: Generate TAC
    quads, triples = postfix_to_tac(postfix)

    print("\n--- Quadruples (Op, Arg1, Arg2, Result) ---")
    print(f"{'No.':<5} {'Op':<5} {'Arg1':<8} {'Arg2':<8} {'Result'}")
    print("-" * 35)
    for i, (op, a1, a2, res) in enumerate(quads):
        print(f"({i})   {op:<5} {a1:<8} {a2:<8} {res}")

    print("\n--- Triples (Op, Arg1, Arg2) ---")
    print(f"{'No.':<5} {'Op':<5} {'Arg1':<10} {'Arg2'}")
    print("-" * 30)
    for i, (op, a1, a2) in enumerate(triples):
        print(f"({i})   {op:<5} {a1:<10} {a2}")


# ============================================================
# EXP 7: BASIC BLOCKS + FLOW GRAPH
#
# SIR SAYS:
#   - Input: Three address code
#   - Output: NUMBER of basic blocks + all statements in each block
# ============================================================

def exp7_basic_blocks():
    print("Enter TAC statements one per line (blank line to stop):")
    tac = []
    while True:
        line = input()
        if not line: break
        tac.append(line.strip())

    if not tac:
        print("No input."); return

    # Step 1: Find leaders
    leaders = {0}   # first stmt is always a leader
    for i, stmt in enumerate(tac):
        up = stmt.upper()
        if up.startswith('GOTO') or up.startswith('IF'):
            if i + 1 < len(tac):
                leaders.add(i + 1)   # stmt after goto is a leader
            # find the target label
            target_label = stmt.split()[-1]
            for j, t in enumerate(tac):
                if t.split(':')[0].strip() == target_label:
                    leaders.add(j)

    leaders = sorted(leaders)

    # Step 2: Form blocks
    blocks = []
    for i, s in enumerate(leaders):
        end = leaders[i+1] if i+1 < len(leaders) else len(tac)
        blocks.append(tac[s:end])

    print(f"\nTotal Basic Blocks: {len(blocks)}")
    print("-" * 35)
    for i, blk in enumerate(blocks):
        print(f"\nBlock B{i+1}:")
        for stmt in blk:
            print(f"  {stmt}")

    # Flow graph
    print("\nFlow Graph:")
    for i, blk in enumerate(blocks):
        if not blk: continue
        last = blk[-1].upper()
        if 'GOTO' in last:
            target = blk[-1].split()[-1]
            for j, b in enumerate(blocks):
                if b and b[0].split(':')[0].strip() == target:
                    print(f"  B{i+1} --> B{j+1}")
        else:
            if i+1 < len(blocks):
                print(f"  B{i+1} --> B{i+2}")
        if last.startswith('IF'):
            if i+1 < len(blocks):
                print(f"  B{i+1} --> B{i+2}  (fall-through)")


# ============================================================
# EXP 8: SIC ASSEMBLER
#
# SIR SAYS (from notice):
#   "generate H record, E record and Symbol table
#    with two columns Symbol name and Value"
#   Each H,T,E,Symbol table = 2.5 Marks
#   NOTE: T record IS shown in exam sample, so keep it too.
#   Sir's sample output has H, T, E + Symbol table.
# ============================================================

def exp8_sic_assembler():
    optab = {
        'JMP': '10', 'LDA': '00', 'STA': '0C', 'ADD': '18',
        'SUB': '1C', 'MUL': '20', 'DIV': '24', 'COMP': '28',
        'JEQ': '30', 'JGT': '34', 'JLT': '38', 'JSUB': '48',
        'RSUB': '4C', 'LDCH': '50', 'STCH': '54',
    }

    print("Enter SIC program (label mnemonic operand). Blank to stop.")
    print("Supported: START END BYTE WORD RESB RESW EQU + instructions")
    lines = []
    while True:
        ln = input()
        if not ln: break
        lines.append(ln.split())

    # ---- PASS 1: Build Symbol Table ----
    symtab = {}
    locctr = 0
    start_addr = 0
    prog_name = 'PROG'

    for parts in lines:
        if len(parts) == 3:
            label, mnem, operand = parts
        elif len(parts) == 2:
            label, mnem, operand = None, parts[0], parts[1]
        else:
            label, mnem, operand = None, parts[0], None

        if mnem == 'START':
            start_addr = int(operand, 16)
            locctr = start_addr
            prog_name = label or 'PROG'
            continue
        if mnem == 'END':
            break
        if mnem == 'EQU':
            if label:
                # EQU stores value directly (not address)
                symtab[label] = format(int(operand) if operand.isdigit() else 0, '04X')
            continue
        if label:
            symtab[label] = format(locctr, '04X')

        if mnem in optab:       locctr += 3
        elif mnem == 'WORD':    locctr += 3
        elif mnem == 'RESW':    locctr += 3 * int(operand)
        elif mnem == 'RESB':    locctr += int(operand)
        elif mnem == 'BYTE':
            if operand.startswith("C='"):
                locctr += len(operand) - 3
            elif operand.startswith("X='"):
                locctr += (len(operand) - 3) // 2

    prog_len = locctr - start_addr

    # ---- PASS 2: Generate Object Code ----
    obj_records = []   # (address, hex_code, byte_count)
    locctr = start_addr

    for parts in lines:
        if len(parts) == 3:
            label, mnem, operand = parts
        elif len(parts) == 2:
            label, mnem, operand = None, parts[0], parts[1]
        else:
            label, mnem, operand = None, parts[0], None

        if mnem in ('START', 'END', 'RESW', 'RESB', 'EQU'):
            continue

        if mnem in optab:
            addr = symtab.get(operand, '0000')
            code = optab[mnem] + addr
            obj_records.append((locctr, code, 3))
            locctr += 3
        elif mnem == 'WORD':
            code = format(int(operand), '06X')
            obj_records.append((locctr, code, 3))
            locctr += 3
        elif mnem == 'BYTE':
            if operand.startswith("C='"):
                text = operand[3:-1]
                code = ''.join(format(ord(c), '02X') for c in text)
                obj_records.append((locctr, code, len(text)))
                locctr += len(text)
            elif operand.startswith("X='"):
                code = operand[3:-1]
                obj_records.append((locctr, code, len(code)//2))
                locctr += len(code) // 2

    # ---- Print Records ----
    h = format(start_addr, '06X')
    l = format(prog_len,   '06X')
    print(f"\nH^{prog_name}^{h}^{l}")

    # T records (max 30 bytes per record)
    t_start = obj_records[0][0] if obj_records else start_addr
    t_data, t_len = "", 0
    for (addr, code, size) in obj_records:
        if t_len + size > 30 or addr != t_start + t_len:
            if t_data:
                print(f"T^{format(t_start,'06X')}^{format(t_len,'02X')}^{t_data}")
            t_start = addr; t_data = ""; t_len = 0
        t_data += code; t_len += size
    if t_data:
        print(f"T^{format(t_start,'06X')}^{format(t_len,'02X')}^{t_data}")

    print(f"E^{h}")

    # Symbol Table
    print("\nSymbol Table:")
    print(f"{'Symbol name':<15} {'Value'}")
    print("-" * 22)
    for sym, val in symtab.items():
        print(f"  {sym:<15} {val}")


# ============================================================
# EXP 9: MACROPROCESSOR
#
# SIR SAYS:
#   - Given sample .asm file with MACRO
#   - Generate: NAMETAB + DEFTAB
#   (Expanded code is bonus, focus on tables)
# ============================================================

def exp9_macroprocessor():
    print("Enter .asm program (blank to stop):")
    lines = []
    while True:
        ln = input()
        if not ln: break
        lines.append(ln.strip())

    nametab = {}   # macro_name -> start index in deftab
    deftab  = []   # all lines of macro definitions

    i = 0
    while i < len(lines):
        parts = lines[i].split()
        if len(parts) >= 2 and parts[1].upper() == 'MACRO':
            name = parts[0]
            nametab[name] = len(deftab)
            deftab.append(lines[i])   # header line
            i += 1
            while i < len(lines) and lines[i].strip().upper() != 'MEND':
                deftab.append(lines[i])
                i += 1
            deftab.append('MEND')
        i += 1

    # Print NAMETAB
    print("\n--- NAMETAB ---")
    print(f"{'Macro Name':<15} {'DEFTAB index'}")
    print("-" * 28)
    for name, idx in nametab.items():
        print(f"  {name:<15} {idx}")

    # Print DEFTAB
    print("\n--- DEFTAB ---")
    print(f"{'Index':<8} {'Line'}")
    print("-" * 35)
    for idx, line in enumerate(deftab):
        print(f"  {idx:<8} {line}")


# ============================================================
# EXP 10: SIC PROGRAM BLOCKS
#
# SIR SAYS:
#   - Given .asm file, identify PROGRAM BLOCKS
#   - Generate BLOCK TABLE
#   (Similar to what you did in lab)
# ============================================================

def exp10_program_blocks():
    print("Enter SIC assembly (blank to stop):")
    print("USE <blockname> switches block. All instructions = 3 bytes.")
    lines = []
    while True:
        ln = input()
        if not ln: break
        lines.append(ln.strip())

    block_order = []
    block_lc    = {}   # block_name -> current length
    current     = None
    start_addr  = 0

    for parts_raw in lines:
        parts = parts_raw.split()
        if not parts: continue

        if len(parts) >= 3:
            label, mnem, operand = parts[0], parts[1], parts[2]
        elif len(parts) == 2:
            label, mnem, operand = None, parts[0], parts[1]
        else:
            label, mnem, operand = None, parts[0], None

        if mnem == 'START':
            start_addr = int(operand)
            current = 'CODE'
            if current not in block_lc:
                block_order.append(current)
                block_lc[current] = 0
            continue
        if mnem == 'END':
            break
        if mnem == 'USE':
            blk = operand if operand else 'CODE'
            if blk not in block_lc:
                block_order.append(blk)
                block_lc[blk] = 0
            current = blk
            continue

        if current is None:
            current = 'DEFAULT'
            block_order.append(current)
            block_lc[current] = 0

        if mnem == 'RESW':
            block_lc[current] += 3 * int(operand)
        elif mnem == 'RESB':
            block_lc[current] += int(operand)
        elif mnem == 'WORD':
            block_lc[current] += 3
        elif mnem == 'BYTE':
            if operand and operand.startswith("C='"):
                block_lc[current] += len(operand) - 3
            elif operand and operand.startswith("X='"):
                block_lc[current] += (len(operand) - 3) // 2
        else:
            block_lc[current] += 3   # instruction

    # Print Block Table
    print("\n--- Block Table ---")
    print(f"{'Block No.':<12} {'Block Name':<12} {'Starting Addr':<16} {'Length (hex)'}")
    print("-" * 55)
    addr = start_addr
    for i, bname in enumerate(block_order):
        ln = block_lc[bname]
        print(f"  {i:<12} {bname:<12} {addr:<16} {format(ln, '04X')}")
        addr += ln


# ============================================================
# EXP 11: SIC LINKING LOADER
#
# SIR SAYS (from notice):
#   Task: Given .asm file -
#     1. Generate D record and R record
#     2. Generate Local Symbol Table (symbol name | value)
#   All instructions are 3 bytes.
#   Sample:
#     PG1 START 0000
#     EXTDEF A, B
#     EXTREF C, D
#     ADD ABC       -> A is label below
#     A SUB PQR
#     ...
#     B MUL ABC
#     END
#   Output:
#     D^ A^000003^B^000009
#     R^ C ^ D ^
#     Local Symbol Table: A->000003, B->000009
# ============================================================

def exp11_linking_loader():
    print("Enter .asm program (blank to stop):")
    print("Use EXTDEF and EXTREF directives. All instructions = 3 bytes.")
    lines = []
    while True:
        ln = input()
        if not ln: break
        lines.append(ln.strip())

    prog_name  = ''
    start_addr = 0
    locctr     = 0
    symtab     = {}   # local labels -> address
    extdefs    = []   # symbols to export
    extrefs    = []   # external references

    for parts_raw in lines:
        parts = parts_raw.split()
        if not parts: continue

        if len(parts) >= 3:
            label, mnem = parts[0], parts[1]
            operand = ' '.join(parts[2:])
        elif len(parts) == 2:
            label, mnem, operand = None, parts[0], parts[1]
        else:
            label, mnem, operand = None, parts[0], None

        if mnem == 'START':
            prog_name  = label or 'PROG'
            start_addr = int(operand)
            locctr     = start_addr
            continue
        if mnem == 'END':
            break
        if mnem == 'EXTDEF':
            # operand like "A, B" or "A,B"
            extdefs = [s.strip() for s in operand.replace(',', ' ').split()]
            continue
        if mnem == 'EXTREF':
            extrefs = [s.strip() for s in operand.replace(',', ' ').split()]
            continue

        # Normal instruction or directive
        if label:
            symtab[label] = format(locctr, '06X')

        # Advance locctr (all 3 bytes as per sir's notice)
        locctr += 3

    # D Record: exported symbols with their addresses
    d_parts = [f"{sym}^{symtab.get(sym, '000000')}" for sym in extdefs]
    print("\nD Record:")
    print("D^" + "^".join(d_parts))

    # R Record: external references
    print("\nR Record:")
    print("R^" + "^".join(extrefs))

    # Local Symbol Table
    print("\nLocal Symbol Table:")
    print(f"{'Symbol NAME':<15} {'value'}")
    print("-" * 25)
    for sym, val in symtab.items():
        print(f"  {sym:<15} {val}")


# ============================================================
#                         MAIN MENU
# ============================================================

def main():
    exps = {
        '2':  ("Exp 2  - Lexical Analyser",              exp2_lexical_analyser),
        '3':  ("Exp 3  - Left Recursion + FIRST/FOLLOW", exp3_left_recursion_and_first_follow),
        '4':  ("Exp 4  - LL(1) Parser Simulation",       exp4_ll1_parser),
        '5':  ("Exp 5  - Intermediate Code Generation",  exp5_intermediate_code),
        '7':  ("Exp 7  - Basic Blocks + Flow Graph",     exp7_basic_blocks),
        '8':  ("Exp 8  - SIC Assembler (H,T,E + SymTab)",exp8_sic_assembler),
        '9':  ("Exp 9  - Macroprocessor (NAMETAB+DEFTAB)",exp9_macroprocessor),
        '10': ("Exp 10 - SIC Program Blocks",            exp10_program_blocks),
        '11': ("Exp 11 - SIC Linking Loader (D,R,SymTab)",exp11_linking_loader),
    }

    print("=" * 55)
    print("   SPCC LAB ESE - AS PER SIR'S NOTICE")
    print("=" * 55)
    for k, (name, _) in exps.items():
        print(f"  [{k:>2}]  {name}")
    print("=" * 55)
    choice = input("Enter experiment number: ").strip()
    if choice in exps:
        print(f"\n{'='*55}")
        print(f"  {exps[choice][0]}")
        print(f"{'='*55}\n")
        exps[choice][1]()
    else:
        print("Invalid choice.")

if __name__ == "__main__":
    main()