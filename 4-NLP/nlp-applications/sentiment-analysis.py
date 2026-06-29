from transformers import pipeline

classifier = pipeline("sentiment-analysis")

# Single input — returns label and confidence score
result = classifier("I love learning AI engineering")
print("Single input:")
print(f"  Label: {result[0]['label']}, Score: {result[0]['score']:.2%}")
print()

# Batch input — always prefer batch over calling one at a time
texts = [
    "I love learning AI engineering",
    "This course is incredibly boring and confusing",
    "The model is okay, not great but not terrible either",
    "Absolutely mind-blowing results. Highly recommended.",
    "Waste of my time. Would not suggest.",
]

results = classifier(texts)

print("Batch classification:")
for text, res in zip(texts, results):
    label = res["label"]
    score = res["score"]
    bar = "+" * int(score * 20)
    print(f"  [{label:8s} {score:.0%}] {bar}  \"{text[:50]}\"")

print()

# The score is the model's confidence in its predicted label, not a general sentiment score.
# A NEGATIVE label with 0.97 score means the model is 97% sure it's negative.
# A POSITIVE label with 0.54 score means the model is barely sure — treat this as uncertain.

# Inspect low-confidence predictions — these are where the model struggles
uncertain = [(t, r) for t, r in zip(texts, results) if r["score"] < 0.85]
print("Low-confidence predictions (review these manually):")
for t, r in uncertain:
    print(f"  [{r['label']} {r['score']:.0%}] {t}")
