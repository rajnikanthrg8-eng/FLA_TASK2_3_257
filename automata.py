"""
automata.py  --  CLA-2 Tasks 2 and 3, 21CSC301T Formal Language and Automata
RAJNIKANTH R G (RA2411026050257)

Task 2 (regular languages, DFAs):  student register number, coupon code, flight number
Task 3 (context-free languages, DPDAs + CFGs):  nested mathematical brackets,
                                                nested function calls, equal 0s and 1s
"""
import re

TRAP = "trap"
DIGITS = "0123456789"
UPPER = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


# ----------------------------------------------------------------------------
# Task 2: table-driven DFA runner
# ----------------------------------------------------------------------------
class DFA:
    def __init__(self, name, start, accepting, delta, classify):
        self.name, self.start = name, start
        self.accepting = set(accepting)
        self.delta = delta              # delta[(state, symbol_class)] -> state
        self.classify = classify        # character -> symbol class

    def step(self, state, ch):
        return self.delta.get((state, self.classify(ch)), TRAP)

    def accepts(self, w):
        s = self.start
        for ch in w:
            s = self.step(s, ch)
            if s == TRAP:
                return False
        return s in self.accepting

    def trace(self, w):
        s, lines = self.start, ["Trace of %s:" % w]
        for ch in w:
            nxt = self.step(s, ch)
            lines.append("delta(%s, '%s' -> %s) = %s" % (s, ch, self.classify(ch), nxt))
            s = nxt
            if s == TRAP:
                break
        lines.append("final state %s: %s" % (s, "ACCEPTED" if s in self.accepting else "REJECTED"))
        return "\n".join(lines)

    def live_states(self):
        st = {self.start} | set(self.accepting)
        for (a, _), b in self.delta.items():
            st.add(a)
            st.add(b)
        st.discard(TRAP)
        return st


# --- Application 1: student register number  RA + 13 digits, first digit 2 ----
def cls_reg(ch):
    if ch == "R":
        return "R"
    if ch == "A":
        return "A"
    if ch == "2":
        return "T"                      # T = the digit 2
    if ch in "013456789":
        return "D"                      # D = any other digit
    return "O"


def build_register():
    d = {("q0", "R"): "q1", ("q1", "A"): "q2", ("q2", "T"): "d1"}
    for i in range(1, 13):
        for c in "TD":
            d[("d%d" % i, c)] = "d%d" % (i + 1)
    return DFA("register", "q0", {"d13"}, d, cls_reg)


# --- Application 2: coupon code  LLLL DD - XXXX ------------------------------
def cls_coupon(ch):
    if ch in UPPER:
        return "L"
    if ch in DIGITS:
        return "D"
    if ch == "-":
        return "H"
    return "O"


def build_coupon():
    d = {}
    for i in range(4):
        d[("C%d" % i, "L")] = "C%d" % (i + 1)
    d[("C4", "D")] = "N1"
    d[("N1", "D")] = "N2"
    d[("N2", "H")] = "H"
    for c in "LD":
        d[("H", c)] = "T1"
        for i in range(1, 4):
            d[("T%d" % i, c)] = "T%d" % (i + 1)
    return DFA("coupon", "C0", {"T4"}, d, cls_coupon)


# --- Application 3: flight number  airline code + 1..4 digits ----------------
def cls_flight(ch):
    if ch in UPPER:
        return "L"
    if ch == "0":
        return "Z"
    if ch in "123456789":
        return "N"
    return "O"


def build_flight():
    d = {("F0", "L"): "FL", ("F0", "Z"): "FD", ("F0", "N"): "FD",
         ("FL", "L"): "FC", ("FL", "Z"): "FC", ("FL", "N"): "FC",
         ("FD", "L"): "FC",
         ("FC", "N"): "G1"}
    for i in range(1, 4):
        for c in "ZN":
            d[("G%d" % i, c)] = "G%d" % (i + 1)
    return DFA("flight", "F0", {"G1", "G2", "G3", "G4"}, d, cls_flight)


REGEX = {   # independent references for Task 2 (regular expressions)
    "register": re.compile(r"RA2[0-9]{12}"),
    "coupon": re.compile(r"[A-Z]{4}[0-9]{2}-[A-Z0-9]{4}"),
    "flight": re.compile(r"(?:[A-Z][A-Z0-9]|[0-9][A-Z])[1-9][0-9]{0,3}"),
}


# ----------------------------------------------------------------------------
# Task 3: deterministic PDA runner
# ----------------------------------------------------------------------------
class DPDA:
    """step(state, token, top) -> (new_state, action) or None (no move).
    action is None (stack unchanged), ('push', X) or ('pop',).
    The scanner appends the end marker '$'; the machine accepts in state qf."""

    def __init__(self, name, start, accepting, step):
        self.name, self.start, self.accepting, self.step = name, start, set(accepting), step

    def run(self, kinds):
        state, stack = self.start, ["Z0"]
        for k in list(kinds) + ["$"]:
            mv = self.step(state, k, stack[-1])
            if mv is None:
                return False
            state, act = mv
            if act:
                if act[0] == "push":
                    stack.append(act[1])
                else:
                    stack.pop()
        return state in self.accepting

    def trace(self, toks, label):
        """toks = list of (kind, lexeme). Prints configurations (state, input left, stack)."""
        state, stack = self.start, ["Z0"]
        rest = [lx for _, lx in toks]
        kinds = [k for k, _ in toks] + ["$"]
        cfg = lambda: "(%s, %s, %s)" % (state, "".join(rest) or "e", "".join(reversed(stack)))
        lines = ["Trace of %s:" % label, cfg()]
        for i, k in enumerate(kinds):
            top = stack[-1]
            mv = self.step(state, k, top)
            if mv is None:
                shown = "end of input" if k == "$" else toks[i][1]
                lines.append("no move: %s with %s on top -> REJECTED" % (shown, "Z0" if top == "Z0" else top))
                return "\n".join(lines)
            state, act = mv
            if act:
                if act[0] == "push":
                    stack.append(act[1])
                else:
                    stack.pop()
            if k != "$":
                rest = rest[1:]
            lines.append("|- " + cfg())
        lines.append("ACCEPTED" if state in self.accepting else "REJECTED")
        return "\n".join(lines)


# --- Case study 1: nested mathematical brackets -------------------------------
RANK = {"(": 1, "[": 2, "{": 3}          # ( inside [ inside {
MATCH = {")": "(", "]": "[", "}": "{"}


def math_step(state, tok, top):
    if state == "q0":                               # a term must start here
        if tok == "v":
            return "q1", None                       # operand read
        if tok in RANK and (top == "Z0" or RANK[tok] <= RANK[top]):
            return "q0", ("push", tok)              # opener allowed at this depth
    elif state == "q1":                             # a term has just ended
        if tok == "o":
            return "q0", None
        if tok in MATCH and top == MATCH[tok]:
            return "q1", ("pop",)
        if tok == "$" and top == "Z0":
            return "qf", None
    return None                                     # no move: reject


MATH_PDA = DPDA("math brackets", "q0", {"qf"}, math_step)


def tokenize_math(s):
    out, i = [], 0
    while i < len(s):
        c = s[i]
        if c.isspace():
            i += 1
        elif c in DIGITS or c in UPPER or c in UPPER.lower():
            j = i
            while j < len(s) and (s[j] in DIGITS or s[j] in UPPER or s[j] in UPPER.lower()):
                j += 1
            out.append(("v", s[i:j]))
            i = j
        elif c in "+-*/^":
            out.append(("o", c))
            i += 1
        elif c in "()[]{}":
            out.append((c, c))
            i += 1
        else:
            return None                              # lexical error
    return out


def math_valid(s):
    t = tokenize_math(s)
    return t is not None and MATH_PDA.run([k for k, _ in t])


def math_reference(kinds):
    """Recursive-descent parser written from the CFG (independent of the PDA).
    C -> X | X o C ; X -> v | (P) | [B] | {C} ; B -> Y | Y o B ; Y -> v | (P) | [B]
    P -> Z | Z o P ; Z -> v | (P).  Level 1 = P, 2 = B, 3 = C."""
    n, pos = len(kinds), [0]

    def term(level):
        t = kinds[pos[0]] if pos[0] < n else None
        if t == "v":
            pos[0] += 1
        elif t in RANK and RANK[t] <= level:
            pos[0] += 1
            expr(RANK[t])
            close = {"(": ")", "[": "]", "{": "}"}[t]
            if pos[0] < n and kinds[pos[0]] == close:
                pos[0] += 1
            else:
                raise ValueError
        else:
            raise ValueError

    def expr(level):
        term(level)
        while pos[0] < n and kinds[pos[0]] == "o":
            pos[0] += 1
            term(level)

    try:
        expr(3)
        return pos[0] == n
    except ValueError:
        return False


# --- Case study 2: nested function calls ---------------------------------------
def call_step(state, tok, top):
    if state == "q0" and tok == "id":
        return "q1", None                           # maybe a function name
    if state == "q1":
        if tok == "(":
            return "q2", ("push", "F")              # it was a call: open it
        if top == "F" and tok == ",":
            return "q4", None                       # it was a plain argument
        if top == "F" and tok == ")":
            return "q3", ("pop",)
    if state == "q2":                               # just after '('
        if tok == "id":
            return "q1", None
        if tok == "num":
            return "q3", None
        if tok == ")":
            return "q3", ("pop",)                   # empty argument list
    if state == "q4":                               # just after ','
        if tok == "id":
            return "q1", None
        if tok == "num":
            return "q3", None
    if state == "q3":                               # an argument or call is complete
        if top == "F" and tok == ",":
            return "q4", None
        if top == "F" and tok == ")":
            return "q3", ("pop",)
        if top == "Z0" and tok == "$":
            return "qf", None
    return None


CALL_PDA = DPDA("function calls", "q0", {"qf"}, call_step)


def tokenize_call(s):
    out, i = [], 0
    while i < len(s):
        c = s[i]
        if c.isspace():
            i += 1
        elif c in UPPER or c in UPPER.lower() or c == "_":
            j = i
            while j < len(s) and (s[j] in UPPER or s[j] in UPPER.lower() or s[j] in DIGITS or s[j] == "_"):
                j += 1
            out.append(("id", s[i:j]))
            i = j
        elif c in DIGITS:
            j = i
            while j < len(s) and s[j] in DIGITS:
                j += 1
            out.append(("num", s[i:j]))
            i = j
        elif c in "(),":
            out.append((c, c))
            i += 1
        else:
            return None
    return out


def call_valid(s):
    t = tokenize_call(s)
    return t is not None and CALL_PDA.run([k for k, _ in t])


def call_reference(kinds):
    """Recursive descent for  F -> id ( A ) ; A -> e | L ; L -> G | G , L ; G -> id | num | F"""
    n, pos = len(kinds), [0]

    def peek():
        return kinds[pos[0]] if pos[0] < n else None

    def call():
        if peek() != "id":
            raise ValueError
        pos[0] += 1
        if peek() != "(":
            raise ValueError
        pos[0] += 1
        if peek() != ")":
            arg()
            while peek() == ",":
                pos[0] += 1
                arg()
        if peek() != ")":
            raise ValueError
        pos[0] += 1

    def arg():
        if peek() == "num":
            pos[0] += 1
        elif peek() == "id":
            if pos[0] + 1 < n and kinds[pos[0] + 1] == "(":
                call()
            else:
                pos[0] += 1
        else:
            raise ValueError

    try:
        call()
        return pos[0] == n
    except ValueError:
        return False


# --- Case study 3: equal number of 0s and 1s ------------------------------------
def eq_step(state, tok, top):
    if state == "q0":
        if tok in ("0", "1"):
            if top == "Z0" or top == tok:
                return "q0", ("push", tok)          # same symbol as the excess: push
            return "q0", ("pop",)                   # opposite symbol: cancel one
        if tok == "$" and top == "Z0":
            return "qf", None
    return None


EQ_PDA = DPDA("equal 0s and 1s", "q0", {"qf"}, eq_step)


def eq_valid(w):
    return set(w) <= {"0", "1"} and EQ_PDA.run(list(w))


def eq_reference(w):
    return w.count("0") == w.count("1")


# parse-tree counters for the two grammars of Case study 3 (ambiguity check)
from functools import lru_cache


@lru_cache(maxsize=None)
def trees_AB(x, c):
    """A -> 1 | 0AA  (c = '1')  and  B -> 0 | 1BB  (c = '0'): number of parse trees of x"""
    o = "0" if c == "1" else "1"
    if x == c:
        return 1
    if len(x) >= 3 and x[0] == o:
        return sum(trees_AB(x[1:k], c) * trees_AB(x[k:], c) for k in range(2, len(x)))
    return 0


@lru_cache(maxsize=None)
def trees_good(w):
    """S -> 0AS | 1BS | e   (number of parse trees of w)"""
    if w == "":
        return 1
    c = "1" if w[0] == "0" else "0"
    return sum(trees_AB(w[1:k], c) * trees_good(w[k:]) for k in range(2, len(w) + 1))


@lru_cache(maxsize=None)
def trees_naive(w):
    """S -> SS | 0S1 | 1S0 | 01 | 10   (non-empty strings)"""
    n, t = len(w), 0
    for k in range(1, n):
        t += trees_naive(w[:k]) * trees_naive(w[k:])
    if n == 2 and w in ("01", "10"):
        t += 1
    if n >= 3 and w[0] != w[-1]:
        t += trees_naive(w[1:-1])
    return t
