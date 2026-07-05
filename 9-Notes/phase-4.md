# Phase 4 — NLP + Transformers

## What this phase covers
- Text preprocessing and tokenization
- Word representation with TF-IDF and embeddings
- NLP applications like sentiment analysis, NER, summarization
- Pre-trained transformers: BERT, GPT, Hugging Face models
- Transformer architecture concepts: attention, positional encoding, encoder/decoder

## Key terms and meaning
- `tokenization`: splitting text into tokens the model can process. In interviews, explain that tokenization turns raw text into pieces the model can understand, often subwords instead of whole words.
- `BPE`: byte-pair encoding. It is a subword tokenization strategy that balances vocabulary size and rare word handling.
- `TF-IDF`: term frequency–inverse document frequency. It is a classic way to turn text into numbers by scoring words that are common in one document but rare across the corpus.
- `embedding`: dense vector representation of text or words. Embeddings capture semantic meaning so similar text maps to similar vectors.
- `self-attention`: a mechanism that lets each token look at every other token in the sequence. It is how transformers decide which words matter for each prediction.
- `encoder`: a transformer block that reads all tokens bidirectionally. Use encoder models like BERT for understanding and classification tasks.
- `decoder`: a transformer block that predicts next tokens autoregressively. Use decoder models like GPT for generation.
- `fine-tuning`: adapting a pre-trained model to a specific task. This is the most practical way to get good results without training from scratch.
- `context window`: the number of tokens the model can consider at once. Interviewers often ask why long documents need chunking for RAG.
- `attention head`: one parallel attention mechanism in multi-head attention. Multiple heads let the model learn different relations at once.

## When to use
- Use these notes when you need to understand how language is represented inside models
- Use NLP apps when you need extraction, classification, or summarization of text
- Use transformers when the problem requires understanding context or generating text

## Interview review
- Describe tokenization as a preprocessing step that directly affects the number of tokens and cost for LLMs.
- When asked about transformers, explain the basic flow: embedding + position + attention + feed-forward.
- Mention that encoder-only models are best for understanding and classification, while decoder-only models are best for generation.
- If asked about TF-IDF vs embeddings, say TF-IDF is sparse and faster, while embeddings capture semantics and work better for similarity search.

## What to use
- `transformers` library for tokenization and pre-trained models
- `sklearn.feature_extraction.text.TfidfVectorizer` for TF-IDF baselines
- `sentence-transformers` or `transformers` for embeddings
- `pipeline()` for quick inference on sentiment, NER, summarization

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

### Embeddings example
```python
from transformers import AutoTokenizer, AutoModel
import torch

tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
model = AutoModel.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
inputs = tokenizer("hello world", return_tensors="pt")
outputs = model(**inputs)
embedding = outputs.last_hidden_state.mean(dim=1)
```

### Hugging Face pipeline
```python
from transformers import pipeline
summarizer = pipeline("summarization")
print(summarizer("This is a long sentence.", max_length=30))
```
