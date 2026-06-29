"""
Generate and save BERT embeddings for all character bios.
Run this once — it saves embeddings.pt so search.py and app.py don't
re-run BERT on every query.
"""

import torch
import torch.nn.functional as F
from transformers import AutoTokenizer, AutoModel
from data import get_all_characters, get_bios


MODEL_NAME = "bert-base-uncased"


def mean_pool(last_hidden_state, attention_mask):
    mask = attention_mask.unsqueeze(-1).float()
    return (last_hidden_state * mask).sum(dim=1) / mask.sum(dim=1)


def embed_texts(texts, tokenizer, model, batch_size=8):
    all_embeddings = []
    for i in range(0, len(texts), batch_size):
        batch = texts[i : i + batch_size]
        inputs = tokenizer(
            batch,
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=256,
        )
        with torch.no_grad():
            outputs = model(**inputs)
        embeddings = mean_pool(outputs.last_hidden_state, inputs["attention_mask"])
        all_embeddings.append(embeddings)
    return torch.cat(all_embeddings, dim=0)


if __name__ == "__main__":
    print(f"Loading {MODEL_NAME}...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModel.from_pretrained(MODEL_NAME)
    model.eval()

    characters = get_all_characters()
    bios = get_bios()

    print(f"Embedding {len(bios)} character bios...")
    embeddings = embed_texts(bios, tokenizer, model)

    # L2-normalize so cosine similarity = dot product (faster at search time)
    embeddings = F.normalize(embeddings, dim=-1)

    print("Embeddings shape:", embeddings.shape)  # (num_characters, 768)

    torch.save(
        {
            "embeddings": embeddings,
            "characters": characters,
            "model": MODEL_NAME,
        },
        "embeddings.pt",
    )
    print("Saved embeddings.pt")
