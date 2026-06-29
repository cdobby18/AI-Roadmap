"""
Semantic search over One Piece character bios using BERT embeddings.
Run embeddings.py first to generate embeddings.pt.
"""

import torch
import torch.nn.functional as F
from transformers import AutoTokenizer, AutoModel


def mean_pool(last_hidden_state, attention_mask):
    mask = attention_mask.unsqueeze(-1).float()
    return (last_hidden_state * mask).sum(dim=1) / mask.sum(dim=1)


def load_index(path="embeddings.pt"):
    data = torch.load(path, map_location="cpu", weights_only=False)
    return data["embeddings"], data["characters"], data["model"]


def embed_query(query, tokenizer, model):
    inputs = tokenizer(
        query,
        return_tensors="pt",
        padding=True,
        truncation=True,
        max_length=256,
    )
    with torch.no_grad():
        outputs = model(**inputs)
    embedding = mean_pool(outputs.last_hidden_state, inputs["attention_mask"])
    return F.normalize(embedding, dim=-1)


def search(query, embeddings, characters, tokenizer, model, top_k=5):
    query_embedding = embed_query(query, tokenizer, model)
    # Cosine similarity: dot product of unit vectors — O(n) over character count
    scores = (query_embedding @ embeddings.T).squeeze(0)
    top_indices = scores.topk(top_k).indices.tolist()
    return [
        {
            "name": characters[i]["name"],
            "role": characters[i]["role"],
            "bio": characters[i]["bio"],
            "score": scores[i].item(),
        }
        for i in top_indices
    ]


if __name__ == "__main__":
    print("Loading index and model...")
    embeddings, characters, model_name = load_index()
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModel.from_pretrained(model_name)
    model.eval()

    queries = [
        "a rubber man who wants to be king of the pirates",
        "the greatest swordsman who fights with three swords",
        "a blind man who controls gravity and pulls down meteors",
        "a doctor who can transform between human and animal forms",
        "someone who controls fire and is related to the pirate king",
    ]

    for query in queries:
        print(f"\nQuery: '{query}'")
        results = search(query, embeddings, characters, tokenizer, model, top_k=3)
        for rank, r in enumerate(results, 1):
            print(f"  {rank}. [{r['score']:.3f}] {r['name']} — {r['role']}")
