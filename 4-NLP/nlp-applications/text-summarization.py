from transformers import pipeline

summarizer = pipeline("summarization")

text = """
Artificial intelligence is transforming industries by enabling machines
to learn patterns from data and automate complex tasks.
"""

summary = summarizer(text, max_length=30)

print(summary)