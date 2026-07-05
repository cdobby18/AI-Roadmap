# DevilFruit Text Processor — Context

**Phase:** 1 — Python Foundations + DSA + SQL
**Theme:** One Piece — raw text is a weak pirate, cleaned text is Yonko-level, each processing step is a Devil Fruit ability.

---

## What It Is

A CLI script that reads a raw text file, runs it through an OOP text-cleaning pipeline, detects its language, prints summary statistics, and persists every run to a MySQL database.

---

## Files

| File | Role |
|---|---|
| `grandline.py` | Entry point. Reads `poneglyph.txt`, runs the pipeline, prints the summary, saves the result, reads it back. |
| `fruit.py` | `DevilFruit` class — the text-cleaning pipeline. |
| `database.py` | MySQL access layer — connection handling, CRUD, filtering, sorting, aggregation, joins, indexes. |
| `poneglyph.txt` | Sample input text. |

---

## The `DevilFruit` Class (`fruit.py`)

Holds `original_text` (untouched), `text` (mutated by each step), and `tokens`.

| Method | Returns | Does |
|---|---|---|
| `.lowercase()` | self | Lowercases text |
| `.remove_punctuation()` | self | Strips punctuation via regex |
| `.remove_extra_space()` | self | Collapses whitespace |
| `.remove_numbers()` | self | Strips digits |
| `.remove_stopwords()` | self | Drops a fixed stopword set |
| `.tokenize()` | list | Splits into words, stores on `self.tokens` |
| `.clean_all()` | self | Runs all of the above in order |
| `.get_summary()` | dict | word_count, unique_words, avg_word_length, top 5 words (`Counter.most_common`) |
| `.detect_language()` | tuple | `(language, confidence)` via the `langdetect` library |

Every mutating method returns `self`, so the pipeline chains: `fruit.clean_all()` is really `lowercase → remove_punctuation → remove_extra_space → remove_numbers → remove_stopwords → tokenize`, all in one call.

---

## The Database Layer (`database.py`)

Uses `mysql.connector` with credentials from a `.env` file (`DB_HOST`, `DB_USER`, `DB_PASSWORD`, `DB_NAME`). A single `execute(query, params, fetch, many)` helper opens a connection, runs the query, commits or rolls back, and always closes the connection/cursor — every other function in the file calls through it.

**Tables:** `processed_texts` (the main record), `users`, `processing_history` (join table linking users to texts they've processed, with foreign keys).

**Operations implemented:** insert, read (all / by id / by column), filter (`WHERE ... = / LIKE`), sort (`ORDER BY ... ASC/DESC`), aggregation (`COUNT`, `AVG`, `MAX`, `MIN`, `SUM`), `GROUP BY`, update, delete, `INNER JOIN` (processing_history → users → processed_texts), `LEFT JOIN` (users → processing_history, keeps users with no history), and manual index creation on `language`, `word_count`, and the composite `(language, word_count)`.

---

## How to Run

```bash
pip install mysql-connector-python python-dotenv langdetect

# .env file needed:
# DB_HOST=... DB_USER=... DB_PASSWORD=... DB_NAME=...

python grandline.py
```

`grandline.py` will create the tables if they don't exist, process `poneglyph.txt`, print the summary, save the row, then print every row currently in `processed_texts` as proof the round-trip worked.

---

## Author

**Carl Joshua M. Coloma** — Computer Science, Software Engineering — AI Engineering Track — Phase 1 Project
