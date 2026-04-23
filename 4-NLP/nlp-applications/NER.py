from transformers import pipeline

ner = pipeline("ner")

text = "Elon Musk founded SpaceX in the United States."

entities = ner(text)

print(entities)