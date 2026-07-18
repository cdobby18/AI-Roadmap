"""Phase 6 - FAISS basics: index types, building, searching, persistence.

FAISS is NOT a vector database. It is an in-memory index library.
No persistence (unless you save/load manually). No metadata filtering.
Use it when: you need fast search, data fits in memory, persistence isn't critical.
"""

import faiss
import numpy as np

rng = np.random.default_rng(42)
DIM = 64
N = 1000

vectors = rng.random((N, DIM), dtype=np.float32)
query = rng.random((1, DIM), dtype=np.float32)

faiss.normalize_L2(vectors)
faiss.normalize_L2(query)

index = faiss.IndexFlatIP(DIM)
index.add(vectors)
print(f"IndexFlatIP — {index.ntotal} vectors, {index.d} dimensions")

scores, indices = index.search(query, 5)
print(f"Top 5 nearest neighbors: indices {indices[0]}, scores {scores[0].round(3)}")

nlist = 10
quantizer = faiss.IndexFlatIP(DIM)
ivf = faiss.IndexIVFFlat(quantizer, DIM, nlist, faiss.METRIC_INNER_PRODUCT)
ivf.train(vectors)
ivf.add(vectors)
ivf.nprobe = 3

scores_ivf, indices_ivf = ivf.search(query, 5)
print(f"IndexIVFFlat (nprobe={ivf.nprobe}): indices {indices_ivf[0]}, scores {scores_ivf[0].round(3)}")

faiss.write_index(index, "faiss_demo.index")
loaded = faiss.read_index("faiss_demo.index")
print(f"\nSaved and reloaded index — {loaded.ntotal} vectors")

import os
os.remove("faiss_demo.index")
