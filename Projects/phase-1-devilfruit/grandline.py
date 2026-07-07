from fruit import DevilFruit
from database import create_tables, insert_processed_text, get_all_texts


def print_summary(summary):
    print("\n" + "=" * 40)
    print("        PIRATE DATA SUMMARY")
    print("=" * 40)

    print(f" Word Count        : {summary['word_count']}")
    print(f" Unique Words      : {summary['unique_words']}")
    print(f" Avg Word Length   : {summary['avg_word_length']}")

    print("\n TOP 5 BOUNTIES ")

    for word, count in summary["top_words"]:
        print(f"  '{word}' - {count}x")

    print("=" * 40)


def main():

    # 1. CREATE TABLES (safe to call every run)
    create_tables()

    # 2. READ FILE
    try:
        with open("poneglyph.txt", "r", encoding="utf-8") as file:
            raw_text = file.read()
    except FileNotFoundError:
        print("File Not Found!")
        return

    print(f"Scanned Scroll: poneglyph.txt ({len(raw_text)} chars)")

    # 3. NLP PROCESSING
    fruit = DevilFruit(raw_text)
    print(f"Power Acquired: {fruit}")

    fruit.clean_all()
    print("Transformation Complete")

    summary = fruit.get_summary()
    print_summary(summary)

    # 4. LANGUAGE DETECTION
    lang, confidence = fruit.detect_language()
    print(f"\n Log Pose Result: {lang} (confidence: {confidence}%)")

    # 5. SAVE TO DATABASE 
    insert_processed_text(
        raw_text,
        fruit.text,
        lang,
        summary["word_count"],
        summary["unique_words"]
    )

    print("\nSaved to One Piece Database!")

    # 6. READ BACK FROM DATABASE (PROOF IT WORKS)
    print("\n=== DATABASE CONTENT ===")
    records = get_all_texts()

    for r in records:
        print(r)


if __name__ == "__main__":
    main()