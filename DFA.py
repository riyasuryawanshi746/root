import collections

class Node:
    def __init__(self, char, node_type, left=None, right=None, pos=None):
        self.char = char
        self.type = node_type
        self.left = left
        self.right = right
        self.pos = pos
        self.nullable = False
        self.firstpos = set()
        self.lastpos = set()

def preprocess(regex):
    """Inserts explicit concatenation operator '.' where needed."""
    res = ""
    for i in range(len(regex)):
        c1 = regex[i]
        res += c1
        if i + 1 < len(regex):
            c2 = regex[i+1]
            # Logic: Add dot between (operand/)/star) and (operand/()
            if (c1.isalnum() or c1 in {'*', ')', '#'}) and (c2.isalnum() or c2 in {'(', '#'}):
                res += '.'
    return res

def shunting_yard(regex):
    """Converts infix (a+b)*.c.# to postfix ab+*c.#.."""
    precedence = {'*': 3, '.': 2, '+': 1}
    output = []
    stack = []
    for char in regex:
        if char.isalnum() or char == '#':
            output.append(char)
        elif char == '(':
            stack.append(char)
        elif char == ')':
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            stack.pop()
        elif char in precedence:
            while stack and stack[-1] != '(' and precedence.get(stack[-1], 0) >= precedence[char]:
                output.append(stack.pop())
            stack.append(char)
    while stack:
        output.append(stack.pop())
    return "".join(output)

def build_tree(postfix):
    stack = []
    pos = 1
    nodes_with_pos = {}
    for char in postfix:
        if char.isalnum() or char == '#':
            node = Node(char, 'leaf', pos=pos)
            nodes_with_pos[pos] = char
            stack.append(node)
            pos += 1
        elif char == '*':
            child = stack.pop()
            stack.append(Node(char, 'star', left=child))
        else: # + or .
            right = stack.pop()
            left = stack.pop()
            ntype = 'union' if char == '+' else 'concat'
            stack.append(Node(char, ntype, left=left, right=right))
    return stack.pop(), pos - 1, nodes_with_pos

def compute_functions(node, followpos):
    if not node: return
    compute_functions(node.left, followpos)
    compute_functions(node.right, followpos)

    if node.type == 'leaf':
        node.nullable = False
        node.firstpos = {node.pos}
        node.lastpos = {node.pos}
    elif node.type == 'union':
        node.nullable = node.left.nullable or node.right.nullable
        node.firstpos = node.left.firstpos | node.right.firstpos
        node.lastpos = node.left.lastpos | node.right.lastpos
    elif node.type == 'concat':
        node.nullable = node.left.nullable and node.right.nullable
        node.firstpos = node.left.firstpos | (node.right.firstpos if node.left.nullable else set())
        node.lastpos = node.right.lastpos | (node.left.lastpos if node.right.nullable else set())
        # The key Rule for Followpos (Concat)
        for i in node.left.lastpos:
            followpos[i].update(node.right.firstpos)
    elif node.type == 'star':
        node.nullable = True
        node.firstpos = node.left.firstpos
        node.lastpos = node.left.lastpos
        # The key Rule for Followpos (Star)
        for i in node.lastpos:
            followpos[i].update(node.firstpos)

# --- Execution ---
user_input = input("Enter Regex (e.g., (a+b)*c): ")
raw_regex = f"({user_input})#" 
processed = preprocess(raw_regex)
postfix = shunting_yard(processed)
tree_root, total_pos, pos_map = build_tree(postfix)

followpos = {i: set() for i in range(1, total_pos + 1)}
compute_functions(tree_root, followpos)

print(f"\nProcessed Infix: {processed}")
print(f"Postfix: {postfix}")
print("-" * 30)
print("Followpos Table:")
for i in range(1, total_pos + 1):
    print(f"Position {i} ({pos_map[i]}): {followpos[i]}")
    

def construct_dfa(tree_root, followpos, pos_map):
    # The starting state is the firstpos of the root
    start_state = frozenset(tree_root.firstpos)
    states = [start_state]
    dfa_transitions = {}
    
    # Get unique alphabet symbols (excluding the endmarker #)
    alphabet = set(pos_map.values()) - {'#'}
    
    i = 0
    while i < len(states):
        current_state = states[i]
        dfa_transitions[current_state] = {}
        
        for symbol in alphabet:
            # Find all positions in the current state that match this symbol
            next_positions = set()
            for pos in current_state:
                if pos_map.get(pos) == symbol:
                    next_positions.update(followpos[pos])
            
            if next_positions:
                next_state = frozenset(next_positions)
                if next_state not in states:
                    states.append(next_state)
                dfa_transitions[current_state][symbol] = next_state
        i += 1
    
    return states, dfa_transitions

# --- Execution for DFA ---
states, transitions = construct_dfa(tree_root, followpos, pos_map)

print("\nDFA TRANSITION TABLE")
print(f"{'State':<20} | {'Symbol':<10} | {'Next State'}")
print("-" * 50)

for state in states:
    state_name = sorted(list(state))
    for symbol, next_state in transitions[state].items():
        next_state_name = sorted(list(next_state))
        print(f"{str(state_name):<20} | {symbol:<10} | {next_state_name}")

# Identify Accepting States
accepting_pos = [pos for pos, char in pos_map.items() if char == '#'][0]
final_states = [sorted(list(s)) for s in states if accepting_pos in s]
print(f"\nFinal (Accepting) States: {final_states}")