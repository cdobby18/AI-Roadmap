from transformers import pipeline

classifier = pipeline("sentiment-analysis")

result = classifier("I love learning AI engineering")

print(result)