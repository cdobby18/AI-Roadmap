from transformers import pipeline

classifier = pipeline("sentiment-analysis")

print(classifier("Transformers are powerful"))