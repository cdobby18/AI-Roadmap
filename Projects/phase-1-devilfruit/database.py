import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

# =========================
# CONNECTION
# =========================
def get_connection():
    try: 
        return mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
            autocommit=False
        )
    except mysql.connector.Error as e:
        print("Database connection failed: ", e)
        return None

def execute(query, params=None, fetch=False, many=False):
    db = get_connection()

    if db is None:
        return None

    cursor = db.cursor(dictionary=True)

    try:
        if many:
            cursor.executemany(query, params)
        else:
            cursor.execute(query, params or None)

        result = cursor.fetchall() if fetch else None

        db.commit()
        return result

    except Exception as e:
        db.rollback()
        print("SQL Error:", e)

    finally:
        cursor.close()
        db.close()

# =========================
# CREATE TABLES
# =========================
def create_tables():
    execute("""
    CREATE TABLE IF NOT EXISTS processed_texts (
        id INT AUTO_INCREMENT PRIMARY KEY,
        original_text TEXT NOT NULL,
        cleaned_text TEXT NOT NULL,
        language VARCHAR(20),
        word_count INT,
        unique_words INT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(100) UNIQUE NOT NULL,
        crew_role VARCHAR(100),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    execute("""
    CREATE TABLE IF NOT EXISTS processing_history (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT,
        processed_text_id INT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id),
        FOREIGN KEY (processed_text_id) REFERENCES processed_texts(id)
    )
    """)

    print("Tables created")


# =========================
# CREATE (INSERT)
# =========================
def insert_processed_text(original, cleaned, language, word_count, unique_words):
    execute("""
        INSERT INTO processed_texts (
            original_text, cleaned_text, language, word_count, unique_words
        ) VALUES (%s, %s, %s, %s, %s)
    """, (original, cleaned, language, word_count, unique_words))


# =========================
# READ (BASIC)
# =========================
def get_all_texts():
    return execute("SELECT * FROM processed_texts", fetch=True)


def get_one_text(text_id):
    return execute(
        "SELECT * FROM processed_texts WHERE id = %s",
        (text_id,),
        fetch=True
    )


def get_columns():
    return execute(
        "SELECT language, word_count FROM processed_texts",
        fetch=True
    )


# =========================
# FILTERING
# =========================
def filter_by_language(lang):
    return execute(
        "SELECT * FROM processed_texts WHERE language = %s",
        (lang,),
        fetch=True
    )


def filter_by_word_count(min_words):
    return execute(
        "SELECT * FROM processed_texts WHERE word_count > %s",
        (min_words,),
        fetch=True
    )


def search_text(keyword):
    return execute(
        "SELECT * FROM processed_texts WHERE original_text LIKE %s",
        (f"%{keyword}%",),
        fetch=True
    )


# =========================
# SORTING
# =========================
def sort_by_words(desc=False):
    order = "DESC" if desc else "ASC"
    return execute(
        f"SELECT * FROM processed_texts ORDER BY word_count {order}",
        fetch=True
    )


def sort_by_newest():
    return execute(
        "SELECT * FROM processed_texts ORDER BY created_at DESC",
        fetch=True
    )


# =========================
# AGGREGATION
# =========================
def aggregation():
    return {
        "count": execute("SELECT COUNT(*) AS total FROM processed_texts", fetch=True),
        "avg": execute("SELECT AVG(word_count) AS avg_words FROM processed_texts", fetch=True),
        "max": execute("SELECT MAX(word_count) AS max_words FROM processed_texts", fetch=True),
        "min": execute("SELECT MIN(word_count) AS min_words FROM processed_texts", fetch=True),
        "sum": execute("SELECT SUM(word_count) AS total_words FROM processed_texts", fetch=True),
    }


def group_by_language():
    return execute("""
        SELECT language, COUNT(*) AS total
        FROM processed_texts
        GROUP BY language
    """, fetch=True)


# =========================
# UPDATE
# =========================
def update_language(text_id, new_language):
    execute("""
        UPDATE processed_texts
        SET language = %s
        WHERE id = %s
    """, (new_language, text_id))


# =========================
# DELETE
# =========================
def delete_text(text_id):
    execute(
        "DELETE FROM processed_texts WHERE id = %s",
        (text_id,)
    )


# =========================
# INSERT USER (for JOIN later)
# =========================
def create_user(username, crew_role):
    execute("""
        INSERT INTO users (username, crew_role)
        VALUES (%s, %s)
    """, (username, crew_role))


# =========================
# JOIN QUERY
# =========================
def get_user_processing_history():
    return execute("""
        SELECT
            users.username,
            processed_texts.language,
            processed_texts.word_count
        FROM processing_history
        INNER JOIN users
            ON processing_history.user_id = users.id
        INNER JOIN processed_texts
            ON processing_history.processed_text_id = processed_texts.id
    """, fetch=True)


def get_users_left_join():
    return execute("""
        SELECT
            users.username,
            processing_history.id
        FROM users
        LEFT JOIN processing_history
            ON users.id = processing_history.user_id
    """, fetch=True)


# =========================
# INDEXES (run once manually or via function)
# =========================
def create_indexes():
    execute("CREATE INDEX idx_language ON processed_texts(language)")
    execute("CREATE INDEX idx_word_count ON processed_texts(word_count)")
    execute("CREATE INDEX idx_lang_wordcount ON processed_texts(language, word_count)")