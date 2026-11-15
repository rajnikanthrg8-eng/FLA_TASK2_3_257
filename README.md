# Formal Languages & Automata (FLA) - Task 2 & Task 3

This repository contains the implementation of parsing, validation, and verification algorithms designed for **Task 2 (Regular Languages & Pattern Matching)** and **Task 3 (Context-Free Languages & Syntactic Structure Verification)**.

---

## 📋 Task 2: Regular Expressions & Pattern Recognition
Task 2 focuses on verifying structural formats of specific input domains using deterministic constraints and regular expressions (Regex). It handles structural parsing for three main categories of codes:

1. **Register Identifiers**
   - **Pattern**: `RA2[0-9]{12}`
   - **Purpose**: Detects and validates system registration IDs that start with the prefix `RA2` followed by exactly 12 numeric digits.

2. **Coupon Codes**
   - **Pattern**: `[A-Z]{4}[0-9]{2}-[A-Z0-9]{4}`
   - **Purpose**: Matches standard structural discount coupons comprised of 4 uppercase letters, 2 digits, a separator hyphen (`-`), and a final block of 4 alphanumeric characters.

3. **Flight Numbers**
   - **Pattern**: `(?:[A-Z][A-Z0-9]|[0-9][A-Z])[1-9][0-9]{0,3}`
   - **Purpose**: Validates standard International Air Transport Association (IATA) flight designators. It ensures a combination of alphanumeric carrier codes followed by a valid flight number starting with non-zero digits.

---

## 📋 Task 3: Context-Free Languages & Bracket Syntactic Diagnostics
Task 3 moves beyond simple regular matching to evaluate non-regular structural languages that require memory or stack tracking. It implements parenthetical validation representing context-free nested grammar structures:

1. **Nested Syntactic Checking**
   - Matches pairs of structural brackets: Parentheses `()`, Square Brackets `[]`, and Curly Braces `{}`.
   - Validates proper nesting, closure, and syntactic hierarchy.

2. **Trapping and Error States**
   - Integrates state-transition logic with an explicit trapping mechanism (`TRAP = 'trap'`) to immediately identify nested structural failures or mismatched closing bounds.
   - Defines precedence and structural ranking values (`RANK`) to enforce correct syntactic boundaries.

---

## 🚀 Getting Started

### Run Validation
Run the test cases and parsing engine directly:
```bash
python automata.py
```
