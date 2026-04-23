from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")
model = AutoModelForSequenceClassification.from_pretrained(
    "distilbert-base-uncased", num_labels=2
)

text = "AI engineering is exciting"

inputs = tokenizer(text, return_tensors="pt")

outputs = model(**inputs)

print(outputs.logits)