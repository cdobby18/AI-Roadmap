# ─── app/models.py ────────────────────────────────────────────────────────────
# TypedDict definitions — these describe the shape of your in-memory data.
# No SQLAlchemy or database involved. This file is purely for type hints so your
# editor can autocomplete dict keys and catch typos.
#
# What is a TypedDict?
#   A regular Python dict can hold anything — TypedDict lets you declare the
#   expected keys and their types. It's like a schema for a plain dict.
#   At runtime it is still just a dict; the types are only for static checking.
#
# Why keep this file at all without a database?
#   - It documents exactly what a "pirate" or "crew" dict looks like
#   - Your editor will warn you if you try to access a key that doesn't exist
#   - It's a stepping stone to understanding ORM models later
#
# How this compares to the old SQLAlchemy version:
#   Old: class Pirate(Base) with Column() fields → maps to a DB table
#   New: class Pirate(TypedDict) with typed keys  → just a type hint for a dict
#
# TODO: Import TypedDict from typing
#       Import Optional from typing
#
# ─── Crew TypedDict ───────────────────────────────────────────────────────────
# TODO: Create a Crew TypedDict with these keys:
#         - id         : int
#         - name       : str
#         - ship       : Optional[str]
#         - sea_region : Optional[str]
#         - is_active  : bool
#
# ─── Pirate TypedDict ─────────────────────────────────────────────────────────
# TODO: Create a Pirate TypedDict with these keys:
#         - id          : int
#         - name        : str
#         - bounty      : float
#         - devil_fruit : Optional[str]
#         - role        : Optional[str]
#         - crew_id     : Optional[int]
#
# Usage: from app.models import Pirate, Crew
#        These are used as type hints in route files:
#          pirate: Pirate = {...}  ← your editor now knows what keys are valid
