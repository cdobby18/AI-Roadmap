# Phase 4 — NLP + Transformers

## What this phase covers
- Text preprocessing and tokenization
- Word representation: TF-IDF, word2vec, and contextual embeddings
- NLP applications like sentiment analysis, NER, summarization, simple chatbots
- Pre-trained transformers: BERT, GPT, Hugging Face models
- Transformer architecture concepts: attention, multi-head attention, positional encoding, encoder/decoder
- Fine-tuning and sharing models on the Hugging Face Hub

## Key terms and meaning
- `tokenization`: splitting text into tokens the model can process. Turns raw text into pieces the model understands, often subwords instead of whole words.
- `BPE`: byte-pair encoding. A subword tokenization strategy that balances vocabulary size and rare/unseen word handling.
- `TF-IDF`: term frequency–inverse document frequency. A classic way to turn text into numbers by scoring words that are common in one document but rare across the corpus. Sparse, fast, no notion of meaning.
- `word2vec`: learns dense word vectors by predicting a word from its context (CBOW) or context from a word (skip-gram). Captures some semantic relationships (e.g. `king - man + woman ≈ queen`) but produces one fixed vector per word regardless of context.
- `embedding`: dense vector representation of text or words. Similar meaning maps to similar vectors — the foundation for search, clustering, and RAG retrieval.
- `contextual embedding`: unlike word2vec, models like BERT produce a different vector for the same word depending on its surrounding sentence (e.g. "bank" of a river vs a "bank" account).
- `self-attention`: a mechanism letting each token look at every other token in the sequence and weigh how relevant they are. How transformers decide which words matter for each prediction.
- `multi-head attention`: running several attention mechanisms ("heads") in parallel, each learning to focus on different relationships (e.g. syntax vs coreference), then combining the results.
- `Query, Key, Value (Q, K, V)`: the three vectors attention computes from each token. A token's Query is compared against every other token's Key to get attention weights, which are used to combine the Values.
- `positional encoding`: since attention has no built-in sense of word order, a signal (often sinusoidal) is added to embeddings to tell the model each token's position in the sequence.
- `encoder`: a transformer block that reads all tokens bidirectionally. Use encoder models like BERT for understanding/classification tasks.
- `decoder`: a transformer block that predicts next tokens autoregressively (each token only sees previous ones). Use decoder models like GPT for generation.
- `fine-tuning`: adapting a pre-trained model to a specific task by continuing training on task-specific data — the most practical way to get good results without training from scratch.
- `context window`: the number of tokens the model can consider at once. Long documents need chunking (relevant for RAG) because they exceed this window.
- `push to hub`: uploading a trained/fine-tuned model and tokenizer to the Hugging Face Hub so it can be versioned, shared, and loaded by name elsewhere.

## When to use
- Use these notes when you need to understand how language is represented inside models.
- Use TF-IDF for a fast, interpretable baseline on small text classification tasks with no GPU.
- Use word2vec-style embeddings when you need lightweight, static word vectors and don't need context sensitivity.
- Use contextual embeddings / transformers when meaning depends on context, or for semantic search and RAG retrieval.
- Use NLP apps when you need extraction, classification, or summarization of text.
- Use encoder-only models (BERT) for classification/understanding; use decoder-only models (GPT) for generation and chat.
- Use fine-tuning when a pre-trained model is close but not accurate enough on your specific domain/labels.

## Interview review
- Describe tokenization as a preprocessing step that directly affects the number of tokens and cost for LLMs — more tokens means higher latency and API cost.
- If asked about TF-IDF vs word2vec vs transformer embeddings, give the progression: TF-IDF is sparse counting with no meaning; word2vec gives dense static vectors with some semantics; transformer embeddings are contextual, changing per sentence.
- When asked about transformers, explain the basic flow: token embedding + positional encoding → multi-head self-attention → feed-forward → repeat across layers.
- Be ready to explain attention conceptually without heavy math: each token asks "which other tokens matter to me right now" (Query vs Key) and pulls information from them weighted by relevance (Value).
- Explain why multi-head attention is used instead of one large attention: different heads can specialize in different relationships (e.g. one head tracks subject-verb agreement, another tracks pronoun references).
- Mention that encoder-only models are best for understanding/classification, decoder-only for generation, and encoder-decoder (like T5) for sequence-to-sequence tasks like translation/summarization.
- If asked why transformers need positional encoding but RNNs don't, explain that RNNs process tokens sequentially (order is implicit), while attention looks at all tokens at once (order must be added explicitly).
- If asked about fine-tuning vs prompting a large LLM, mention that fine-tuning is worth it for narrow, high-volume tasks with labeled data; prompting/few-shot is faster to iterate and better when data is scarce.

## What to use
- `transformers` library for tokenization and pre-trained models.
- `sklearn.feature_extraction.text.TfidfVectorizer` for TF-IDF baselines.
- `gensim` or `sentence-transformers`/`transformers` for word2vec-style and contextual embeddings.
- `pipeline()` for quick inference on sentiment, NER, summarization.
- Hugging Face Hub (`push_to_hub`) for sharing and versioning fine-tuned models.

## How to use

### Tokenization
```python
from transformers import AutoTokenizer
tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
text = "AI engineering is fun."
ids = tokenizer(text, return_tensors="pt")
print(ids)
```

### TF-IDF example
```python
from sklearn.feature_extraction.text import TfidfVectorizer
texts = ["hello world", "hello AI"]
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(texts)
print(X.toarray())
```

### word2vec example
```python
from gensim.models import Word2Vec

sentences = [["hello", "world"], ["hello", "ai", "engineer"]]
model = Word2Vec(sentences, vector_size=50, window=2, min_count=1, sg=1)  # sg=1 -> skip-gram
print(model.wv["hello"])
print(model.wv.most_similar("hello"))
```

### Contextual embeddings example
```python
from transformers import AutoTokenizer, AutoModel
import torch

tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
model = AutoModel.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
inputs = tokenizer("hello world", return_tensors="pt")
outputs = model(**inputs)
embedding = outputs.last_hidden_state.mean(dim=1)
```

### Scaled dot-product attention (from scratch)
```python
import torch
import torch.nn.functional as F

def attention(Q, K, V):
    scores = Q @ K.transpose(-2, -1) / (Q.size(-1) ** 0.5)
    weights = F.softmax(scores, dim=-1)
    return weights @ V
```

### Hugging Face pipeline
```python
from transformers import pipeline
summarizer = pipeline("summarization")
print(summarizer("This is a long sentence.", max_length=30))
```

### Push a fine-tuned model to the Hub
```python
model.push_to_hub("your-username/your-model-name")
tokenizer.push_to_hub("your-username/your-model-name")
```
