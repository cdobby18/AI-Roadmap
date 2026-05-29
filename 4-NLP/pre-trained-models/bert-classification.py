from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    TrainingArguments,
    Trainer,
)
from datasets import Dataset
import torch

# Small labeled dataset — in production, use a real dataset from HuggingFace Hub
data = {
    "text": [
        "I love this product!", "Absolutely terrible experience.",
        "Great quality and fast shipping.", "Worst purchase I ever made.",
        "Highly recommend this!", "Do not buy this garbage.",
    ],
    "label": [1, 0, 1, 0, 1, 0],   # 1 = positive, 0 = negative
}

dataset = Dataset.from_dict(data).train_test_split(test_size=0.33)

tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")

def tokenize(batch):
    return tokenizer(batch["text"], padding="max_length", truncation=True, max_length=64)

dataset = dataset.map(tokenize, batched=True)

model = AutoModelForSequenceClassification.from_pretrained("bert-base-uncased", num_labels=2)

args = TrainingArguments(
    output_dir="./bert-sentiment",
    num_train_epochs=3,
    per_device_train_batch_size=4,
    per_device_eval_batch_size=4,
    eval_strategy="epoch",
    logging_steps=5,
    save_strategy="no",
)

trainer = Trainer(
    model=model,
    args=args,
    train_dataset=dataset["train"],
    eval_dataset=dataset["test"],
    tokenizer=tokenizer,
)

trainer.train()

# Run inference on new text
inputs = tokenizer("This is an amazing experience!", return_tensors="pt")
with torch.no_grad():
    logits = model(**inputs).logits
predicted_class = logits.argmax().item()
print("Predicted class:", "positive" if predicted_class == 1 else "negative")
