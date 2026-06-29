from transformers import pipeline

# aggregation_strategy="simple" merges B- and I- tokens into single entities
ner = pipeline("ner", aggregation_strategy="simple")

text = "Elon Musk founded SpaceX in Hawthorne, California, and Tesla in Palo Alto."
entities = ner(text)

print("Raw entity output:")
for e in entities:
    print(f"  [{e['entity_group']:4s}] '{e['word']}' — score: {e['score']:.2%}")

# Entity group labels:
#   PER  = person name
#   ORG  = organization (company, institution)
#   LOC  = location (city, country, geographic)
#   MISC = miscellaneous (nationalities, events, products)

print()

# Real-world use: extract characters, locations, organizations from any text
texts = [
    "Barack Obama was born in Honolulu, Hawaii, and served as the 44th president.",
    "Google DeepMind and OpenAI are racing to build artificial general intelligence.",
    "The One Piece manga is published by Shueisha in Japan and written by Eiichiro Oda.",
]

for t in texts:
    print(f"Text: {t}")
    for e in ner(t):
        print(f"  [{e['entity_group']:4s}] {e['word']}")
    print()

# Without aggregation (raw BIO tags):
#   B-PER = Beginning of a person entity
#   I-PER = Inside (continuation) of a person entity
#   B-ORG, I-ORG, B-LOC, I-LOC, etc.
# aggregation_strategy="simple" groups these into clean spans — use this in practice
