# REGEX

import re

email = input("Whats your email? ").strip()

if re.search(r"^\w+@(\w+\.)?\w+\.edu$", email, re.IGNORECASE):
    print("Valid")
else:
    print("Invalid")


# SYMBOLS
# r = raw string (treats backslashes literally, avoids escape issues)
# . = any character except newline
# * = 0 or more repetitions
# + = 1 or more repetitions
# ? = 0 or 1 repetition (optional)
# {m} = exactly m repetitions
# {m, n} = between m and n repetitions
# ^ = matches the start of the string
# $ = matches the end of the string
# [] = set of characters (e.g., [abc])
# [^] = negation (anything NOT inside the brackets)
# \d = digit (0–9)
# \D = not a digit
# \s = whitespace (space, tab, newline)
# \S = not whitespace
# \w = word character (letters, digits, underscore)
# \W = not a word character
# () = grouping
# | = OR operator

# FLAGS
# re.IGNORECASE = ignore uppercase/lowercase differences
# re.MULTILINE = ^ and $ match each line, not just whole string
# re.DOTALL = . matches newline as well


# =========================================
# NOTES / SUMMARY (LESSON 7: REGULAR EXPRESSIONS)
# =========================================
#
# 1. Regular Expressions (re)
#    - Used for searching, validating, and matching text patterns
#    - Common use case: validating inputs like emails
#
# 2. Raw Strings
#    - r"" ensures regex patterns work correctly with backslashes
#
# 3. Pattern Matching
#    - re.search() finds patterns in text
#    - ^ and $ ensure full string validation
#
# 4. Email Validation
#    - Validates format: username@domain.edu
#    - Supports optional subdomains
#
# 5. Regex Symbols & Flags
#    - Special syntax for defining flexible matching rules
#    - Flags modify how matching behaves
#
# =========================================