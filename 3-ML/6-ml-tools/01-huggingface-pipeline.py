"""
Hugging Face pipeline() — run pre-trained models in 3 lines.
Understand what's happening: model downloads weights, tokenizes input,
runs inference, and decodes output — all behind the scenes.
"""
from transformers import pipeline

# Sentiment analysis
classifier = pipeline("sentiment-analysis")
result = classifier("I love building AI applications!")
print("Sentiment:", result)

# Text generation
generator = pipeline("text-generation", model="gpt2")
output = generator("The future of AI is", max_new_tokens=30, num_return_sequences=1)
print("Generated:", output[0]["generated_text"])

# Zero-shot classification — no fine-tuning needed
zero_shot = pipeline("zero-shot-classification")
result = zero_shot(
    "The new GPU has 80GB of VRAM.",
    candidate_labels=["technology", "sports", "politics"],
)
print("Labels:", result["labels"])
print("Scores:", result["scores"])
