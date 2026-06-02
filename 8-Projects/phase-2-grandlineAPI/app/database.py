# ─── app/database.py ──────────────────────────────────────────────────────────
# Sets up the SQLAlchemy connection to SQLite and provides two things:
#   1. Base       — the declarative base all ORM models inherit from
#   2. get_db()   — a FastAPI dependency that yields a DB session per request
#
# How SQLAlchemy works (mental model):
#   Engine      → the physical connection to the database file
#   SessionLocal → a factory that creates individual sessions (like transactions)
#   Base        → the class your models inherit from so SQLAlchemy knows about them
#
# TODO: Import create_engine, sessionmaker, and declarative_base from sqlalchemy
#
# TODO: Import settings from app.config
#
# TODO: Create the engine using settings.database_url
#       For SQLite only, add: connect_args={"check_same_thread": False}
#       (SQLite wasn't built for concurrent access — this disables the guard)
#
# TODO: Create SessionLocal using sessionmaker
#       Set autocommit=False, autoflush=False, bind=engine
#
# TODO: Create Base = declarative_base()
#
# TODO: Write a get_db() generator function
#       - Create a db session with SessionLocal()
#       - yield db  (FastAPI injects this into route functions via Depends)
#       - close the session in a finally block so it always closes on request end
#
# TODO: Write a create_tables() function
#       - Call Base.metadata.create_all(bind=engine)
#       - This is called once at startup (in main.py lifespan) to create tables
