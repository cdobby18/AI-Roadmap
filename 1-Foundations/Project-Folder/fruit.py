import re
from collections import Counter
import requests
from langdetect import detect


class DevilFruit:

    STOPWORDS = {
        "the", "is", "a", "an", "and", "or", "in", "on", "at", "to",
        "for", "of", "with", "by", "it", "this", "that", "from"
    }

    def __init__(self, text: str):
        self.original_text = text
        self.text = text
        self.tokens = []

    def __repr__(self):
        return f"DevilFruit(tokens={len(self.tokens)}, chars={len(self.text)})"

    def __len__(self):
        return len(self.text)

    def lowercase(self):
        self.text = self.text.lower()
        return self

    def remove_punctuation(self):
        self.text = re.sub(r'[^\w\s]', '', self.text)
        return self

    def remove_extra_space(self):
        self.text = re.sub(r"\s+", " ", self.text).strip()
        return self

    def remove_numbers(self):
        self.text = re.sub(r'\d+', '', self.text)
        return self

    def remove_stopwords(self):
        words = self.text.split()
        words = [w for w in words if w not in self.STOPWORDS]
        self.text = " ".join(words)
        return self

    def tokenize(self):
        self.tokens = self.text.split()
        return self.tokens   # FIXED (was wrong before)

    def most_common(self, n=5):
        return Counter(self.tokens).most_common(n)

    def get_summary(self):

        if not self.tokens:
            self.tokenize()

        word_lengths = [len(w) for w in self.tokens]

        return {
            "word_count": len(self.tokens),
            "char_count": len(self.text),
            "unique_words": len(set(self.tokens)),
            "avg_word_length": round(sum(word_lengths) / len(word_lengths), 2) if word_lengths else 0,
            "top_words": self.most_common(5)
        }

    def detect_language(self):

        try:
            url = "https://libretranslate.de/detect"
            response = requests.post(url, data={"q": self.text}, timeout=5)

            if response.status_code == 200:
                data = response.json()
                if data:
                    lang = data[0]["language"]
                    confidence = round(data[0]["confidence"] * 100, 2)
                    return lang, confidence

            raise Exception()

        except Exception:
            try:
                return detect(self.text), 100
            except Exception:
                return "unknown", 0

    def clean_all(self):
        self.lowercase()
        self.remove_punctuation()
        self.remove_extra_space()
        self.remove_numbers()
        self.remove_stopwords()
        self.tokenize()
        return self

    def reset(self):
        self.text = self.original_text
        self.tokens = []
        return self