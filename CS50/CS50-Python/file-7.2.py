import re

url = input("URL: ").strip()

if matches := re.search(r"^(https?://)?(www\.)?twitter\.com/([A-Za-z0-9_]+)$", url, re.IGNORECASE):
    print(f"Username: {matches.group(3)}")

# =========================================
# NOTES / SUMMARY (LESSON 7.2: REGEX URL EXTRACTION)
# =========================================
#
# 1. re.search vs re.sub
#    - re.search() → used to extract matching parts
#    - re.sub() → used to replace text (NOT for capturing groups)
#
# 2. URL Pattern Matching
#    - Handles optional parts:
#        (https?://)? → optional http or https
#        (www\.)?     → optional www
#    - Matches: twitter.com/username
#
# 3. Capturing Groups
#    - group(1) → https:// (optional)
#    - group(2) → www. (optional)
#    - group(3) → username (main extracted value)
#
# 4. Regex Purpose in This Example
#    - Cleanly extract a username from a full URL
#    - Ignore extra parts like protocol and subdomain
#
# 5. Best Practice
#    - Use re.search() when extracting data
#    - Use re.sub() only when replacing text
#
# =========================================