from fruit import DevilFruit

def print_summary(summary):
    print("\n" + "=" * 40)
    print("        PIRATE DATA SUMMARY")
    print("=" * 40)

    print(f" Word Count        : {summary['word_count']}")
    print(f" Character Count   : {summary['char_count']}")
    print(f" Avg Word Length   : {summary['avg_word_length']}")
    print(f" Unique Words      : {summary['unique_words']}")

    print("\n TOP 5 BOUNTIES ")

    for word, count in summary["top_words"]:
        print(f"  '{word}' - {count}x")

    print("=" * 40)


def main():

    # read input file
    try:
        with open("poneglyph.txt", "r", encoding="utf-8") as file:
            raw_text = file.read()
    except FileNotFoundError:
        print("File Not Found!")
        return

    print(f"Scanned Scroll: poneglyph.txt ({len(raw_text)} chars)")

    fruit = DevilFruit(raw_text)
    print(f"Power Acquired: {fruit}")

    # clean + process
    fruit.clean_all()

    print("Transformation Complete")

    # summary
    summary = fruit.get_summary()
    print_summary(summary)

    # language detection
    lang, confidence = fruit.detect_language()
    print(f"\n Log Pose Result: {lang} (confidence: {confidence}%)")

    # save output (FIXED FILE NAME)
    with open("treasures.txt", "w", encoding="utf-8") as file:
        file.write(fruit.text)

    print("Treasure Saved to 'treasures.txt'")


if __name__ == "__main__":
    main()