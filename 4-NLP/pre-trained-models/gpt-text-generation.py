from transformers import pipeline

generator = pipeline("text-generation", model="gpt2")

result = generator("Artificial intelligence will", max_length=40)

print(result)