from transformers import AutoTokenizer, AutoModelForSequenceClassification

# After fine-tuning (see bert-classification.py), push your model to the Hub.
# Run: huggingface-cli login   (paste your token from huggingface.co/settings/tokens)

MODEL_DIR = "./bert-sentiment"   # output_dir from your TrainingArguments
HUB_REPO  = "your-username/bert-sentiment-classifier"

tokenizer = AutoTokenizer.from_pretrained(MODEL_DIR)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_DIR)

tokenizer.push_to_hub(HUB_REPO)
model.push_to_hub(HUB_REPO)

print(f"Model live at: https://huggingface.co/{HUB_REPO}")

# Anyone can now use your model:
#   from transformers import pipeline
#   classifier = pipeline("text-classification", model="your-username/bert-sentiment-classifier")
#   classifier("This is great!")
