# Formal Languages & Automata (FLA) - Task 2 & Task 3

This repository contains the implementation of parsing, validation, and verification algorithms designed for **Task 2 (Regular Languages & Pattern Matching)** and **Task 3 (Context-Free Languages, DPDAs, & CFGs)**.

---

## 📋 Task 2: Regular Expressions & Pattern Recognition
Task 2 focuses on verifying structural formats of specific input domains using deterministic constraints and regular expressions (Regex):

1. **Register Identifiers**
   - **Pattern**: `RA2[0-9]{12}`
   - **Purpose**: Detects and validates system registration IDs that start with the prefix `RA2` followed by exactly 12 numeric digits.

2. **Coupon Codes**
   - **Pattern**: `[A-Z]{4}[0-9]{2}-[A-Z0-9]{4}`
   - **Purpose**: Matches standard structural discount coupons comprised of 4 uppercase letters, 2 digits, a separator hyphen (`-`), and a final block of 4 alphanumeric characters.

3. **Flight Numbers**
   - **Pattern**: `(?:[A-Z][A-Z0-9]|[0-9][A-Z])[1-9][0-9]{0,3}`
   - **Purpose**: Validates standard International Air Transport Association (IATA) flight designators.

---

## 📋 Task 3: Context-Free Languages & Pushdown Automata
Task 3 implements parser/recognizer logic for context-free grammar constraints and deterministic pushdown automata (DPDAs):

1. **Nested Mathematical Brackets**
   - Tracks nested pairs of parentheses `()`, square brackets `[]`, and curly braces `{}`.
   - Ensures correct syntactic matching bounds and hierarchical precedence.

2. **Nested Function Calls**
   - Parses functional structure formats where argument closures and parameters need to be syntactically validated in a nested hierarchy.

3. **Equal 0s and 1s Verification**
   - Evaluates strings containing equal numbers of `0`s and `1`s (a classic non-regular context-free language requirement managed via stack tracking).

---

## 🚀 Getting Started

### Run Validation
Run the test cases and parsing engine directly:
```bash
python automata.py
```
