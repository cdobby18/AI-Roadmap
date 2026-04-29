# REGEX

import re

email = input("Whats your email? ").strip()

if re.search(r"^\w+@(\w+\.)?\w+\.edu$", email, re.IGNORECASE):
    print("Valid")
else:
    print("Invalid")


# SYMBOLS
# r = ??
# . = any character except newline
# * = 0 or more repititons
# + = 1 or more repetitions
# ? = 0 or 1 repetition
# {m} = m repetitions
# {m, n} = m-n repetitions
# ^ = matches the start of string
# $ = matches the end of string
# [] = set of characters
# [^] = complementing the set
# \d & \D = decimal digit or not 
# \s & \S = whitespace character or not
# \w & \W = word character or no including numbers and _
# re.IGNORECASE = ?
# re.MULTILINE = ?
# re.DOTALL = ?
