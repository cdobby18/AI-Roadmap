# ─── app/models.py ────────────────────────────────────────────────────────────
# SQLAlchemy ORM models — these map directly to database tables.
# Think of each class as a table and each Column as a column in that table.
#
# Important distinction:
#   ORM models (here)    → describe the DATABASE shape (SQLAlchemy)
#   Pydantic schemas     → describe the API request/response shape (FastAPI)
#   They look similar but serve different purposes — don't merge them.
#
# TODO: Import Column, Integer, String, Float, Boolean, ForeignKey from sqlalchemy
#       Import relationship from sqlalchemy.orm
#       Import Base from app.database
#
# ─── Crew Model ───────────────────────────────────────────────────────────────
# TODO: Create a Crew class that inherits from Base
#       __tablename__ = "crews"
#       Columns:
#         - id          : Integer, primary key, auto-increment
#         - name        : String, unique, not nullable  (e.g. "Straw Hat Pirates")
#         - ship        : String, nullable              (e.g. "Thousand Sunny")
#         - sea_region  : String, nullable              (e.g. "New World")
#         - is_active   : Boolean, default True
#       Relationship:
#         - pirates     : one-to-many back-ref to Pirate (one crew has many pirates)
#
# ─── Pirate Model ─────────────────────────────────────────────────────────────
# TODO: Create a Pirate class that inherits from Base
#       __tablename__ = "pirates"
#       Columns:
#         - id          : Integer, primary key, auto-increment
#         - name        : String, unique, not nullable  (e.g. "Monkey D. Luffy")
#         - bounty      : Float, default 0.0            (in Belly)
#         - devil_fruit : String, nullable              (e.g. "Gomu Gomu no Mi")
#         - role        : String, nullable              (e.g. "Captain", "Swordsman")
#         - crew_id     : Integer, ForeignKey → crews.id, nullable
#       Relationship:
#         - crew        : many-to-one back-ref to Crew
