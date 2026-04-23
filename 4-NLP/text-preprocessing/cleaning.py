import re

text = "Hello!!! This is an NLP example, with numbers 123 and symbols."

clean_text = re.sub(r'[^a-zA-Z\s]', '', text)
clean_text = clean_text.lower()

print(clean_text)