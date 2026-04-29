import re

name = input("Whats your name? ").strip()

if matches := re.search(r"^(.+), (.+)$", name):
    name = matches.group(2) + " " + matches.group(1)
print(f"Hello, {name}")


# =========================================
# NOTES / SUMMARY (LESSON 7.1: REGEX GROUPS & WALRUS OPERATOR)
# =========================================
#
# 1. Capturing Groups ()
#    - Used to extract specific parts of a matched pattern
#    - group(1), group(2), etc. access captured values
#
# 2. Pattern Example
#    - "^(.+), (.+)$" matches "Last, First" format
#    - Splits input into two groups: last name and first name
#
# 3. String Reformatting
#    - Rearranges captured groups into "First Last" format
#
# 4. Walrus Operator (:=)
#    - Assigns and evaluates a value in one step
#    - Improves readability by avoiding repeated function calls
#
# 5. Conditional Matching
#    - Only reformats name if pattern is matched
#    - Prevents errors for unexpected input formats
#
# =========================================