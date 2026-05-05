# 🏴‍☠️ DevilFruit Text Processor

A Python text preprocessing tool built using OOP principles, inspired by the world of One Piece.  
Transforms raw, chaotic text into clean, structured data—just like gaining power from a Devil Fruit.

---

## ⚓ Concept

In the Grand Line:

- Raw text = Weak Pirate  
- Cleaned text = Yonko-Level Data  
- Processing steps = Devil Fruit Abilities  

This project simulates a **text transformation system** where each method acts as a unique power.

---

## 🧭 What it does

- Converts text to lowercase *(Gomu Gomu no Normalize)*
- Removes punctuation, numbers, and extra spaces *(Blade Cleanse)*
- Removes common stopwords *(Haki Filter)*
- Tokenizes text into individual words *(Crew Split)*
- Returns summary statistics:
  - Word count
  - Unique words
  - Average word length
  - Top 5 most frequent words
- Detects the language of the text using a free public API *(Log Pose)*

---

## 🗺️ Example Output
🏴‍☠️ DevilFruit Processor — Grand Line Edition
---------------------------------------------
========================================
        PIRATE DATA SUMMARY
========================================
  Crew Size (Words)   : 98
  Log Length (Chars)  : 612
  Unique Pirates      : 76
  Avg Word Bounty     : 6.24
  Top 5 Bounties      :
    'learning' — 4x
    'text' — 3x
    'language' — 3x
    'data' — 2x
    'ai' — 2x
========================================

Log Pose Result: English (confidence: 99%)

Treasure saved to 'treasure.txt' 🏴‍☠️

---

## 🏝️ Project Structure
devilfruit_processor/
├── fruit.py # DevilFruit class
├── grandline.py # entry point
├── poneglyph.txt # raw text input
├── .env # API keys (optional)
├── .gitignore
└── README.md

---

## ⚔️ Methods (Devil Fruit Abilities)

| Method | Returns | Description |
|--------|--------|-------------|
| `.lowercase()` | self | Convert text to lowercase |
| `.remove_punctuation()` | self | Remove punctuation |
| `.remove_extra_spaces()` | self | Clean whitespace |
| `.remove_numbers()` | self | Remove digits |
| `.remove_stopwords()` | self | Remove common words |
| `.tokenize()` | list | Split into words |
| `.word_count()` | int | Total word count |
| `.most_common(n)` | list | Top n frequent words |
| `.get_summary()` | dict | Full text statistics |
| `.detect_language()` | tuple | Language + confidence |
| `.clean_all()` | self | Run all steps |
| `.reset()` | self | Restore original text |

---

## 🧠 What I Learned

- Object-Oriented Programming (OOP):
  - Classes, `__init__`, `__repr__`, `__len__`
- Method chaining by returning `self`
- File I/O with proper error handling
- Making HTTP API calls using `requests`
- Handling API errors (timeouts, connection issues, HTTP errors)

---

## 👑 Author

**Carl Joshua M. Coloma**  
Computer Science — Software Engineering  
AI Engineering Track | Phase 1 Project