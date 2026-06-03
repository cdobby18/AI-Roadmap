# ─── app/store.py ─────────────────────────────────────────────────────────────
# In-memory data store — replaces the database for this practice project.
# Data lives here as plain Python lists of dicts. It resets every time the
# server restarts, which is fine for a practice project.
#
# Think of this as a fake database:
#   pirates_db  → like a "pirates" table (a list of dicts)
#   crews_db    → like a "crews" table (a list of dicts)
#
# Why dicts and not objects?
#   Dicts are the simplest Python data structure. Route handlers read from and
#   write to these lists directly — no ORM, no sessions, no SQL.
#
# ─── Dummy Crews ──────────────────────────────────────────────────────────────
# TODO: Create a list called crews_db with at least 3 pre-loaded crew dicts.
#       Each dict should have these keys:
#         - id        : int    (start at 1 and increment)
#         - name      : str    (e.g. "Straw Hat Pirates")
#         - ship      : str    (e.g. "Thousand Sunny")
#         - sea_region: str    (e.g. "New World")
#         - is_active : bool   (True)
#
#       Example crews to use (One Piece theme):
#         Straw Hat Pirates, Thousand Sunny, New World
#         Heart Pirates, Polar Tang, North Blue
#         Beast Pirates, Onigashima, New World
#
# ─── Dummy Pirates ────────────────────────────────────────────────────────────
# TODO: Create a list called pirates_db with at least 5 pre-loaded pirate dicts.
#       Each dict should have these keys:
#         - id         : int
#         - name       : str    (e.g. "Monkey D. Luffy")
#         - bounty     : float  (in Belly — e.g. 3000000000.0)
#         - devil_fruit: str | None  (e.g. "Gomu Gomu no Mi", or None)
#         - role       : str | None  (e.g. "Captain", "Swordsman")
#         - crew_id    : int | None  (must match an id in crews_db, or None)
#
#       Example pirates to use:
#         Monkey D. Luffy — 3,000,000,000 — Gomu Gomu no Mi — Captain — crew_id 1
#         Roronoa Zoro    — 1,111,000,000 — None             — Swordsman — crew_id 1
#         Trafalgar Law   — 3,000,000,000 — Ope Ope no Mi   — Captain — crew_id 2
#         Kaido           — 4,611,100,000 — Uo Uo no Mi     — Captain — crew_id 3
#         Nami            — 366,000,000   — None             — Navigator — crew_id 1
#
# ─── ID Counter Helper ────────────────────────────────────────────────────────
# TODO: Create two counter variables to track the next available ID:
#         next_pirate_id : int  (set to len(pirates_db) + 1 after defining the list)
#         next_crew_id   : int  (set to len(crews_db) + 1 after defining the list)
#
#       When a new pirate is created in the POST route:
#         1. Assign next_pirate_id as the new pirate's id
#         2. Increment next_pirate_id by 1
#       Same pattern for crews.
#
#       Hint: routes will need to use `global next_pirate_id` before modifying it
#             OR you can increment it inside store.py helper functions (see below)
#
# ─── Optional Helper Functions ────────────────────────────────────────────────
# These are optional but make your route code cleaner:
#
# TODO (optional): Write get_pirate_by_id(pirate_id: int) -> dict | None
#       Loop through pirates_db and return the dict where dict["id"] == pirate_id
#       Return None if not found
#       Routes can call this instead of repeating the loop logic each time
#
# TODO (optional): Write get_crew_by_id(crew_id: int) -> dict | None
#       Same pattern as above but for crews_db
