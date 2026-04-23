from transformers import BertTokenizer, BertForSequenceClassification
import torch

tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
model = BertForSequenceClassification.from_pretrained(
    "bert-base-uncased", num_labels=2
)

inputs = tokenizer("AI is the future", return_tensors="pt")

outputs = model(**inputs)

print(outputs.logits)