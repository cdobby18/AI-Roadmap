from typing import Optional

crews_db = [
    {"id": 1, "name": "Straw Hat Pirates", "ship": "Thousand Sunny", "sea_region": "New World", "is_active": True},
    {"id": 2, "name": "Heart Pirates", "ship": "Polar Tang", "sea_region": "North Blue", "is_active": True},
    {"id": 3, "name": "Beast Pirates", "ship": "Onigashima", "sea_region": "New World", "is_active": True},
]

pirates_db = [
    {"id": 1, "name": "Monkey D. Luffy", "bounty": 3000000000.0, "devil_fruit": "Gomu Gomu no Mi", "role": "Captain", "crew_id": 1},
    {"id": 2, "name": "Roronoa Zoro", "bounty": 1111000000.0, "devil_fruit": None, "role": "Swordsman", "crew_id": 1},
    {"id": 3, "name": "Trafalgar Law", "bounty": 3000000000.0, "devil_fruit": "Ope Ope no Mi", "role": "Captain", "crew_id": 2},
    {"id": 4, "name": "Kaido", "bounty": 4611100000.0, "devil_fruit": "Uo Uo no Mi", "role": "Captain", "crew_id": 3},
    {"id": 5, "name": "Nami", "bounty": 366000000.0, "devil_fruit": None, "role": "Navigator", "crew_id": 1},
]

next_crew_id = len(crews_db) + 1
next_pirate_id = len(pirates_db) + 1


def get_crew_by_id(crew_id: int) -> Optional[dict]:
    return next((c for c in crews_db if c["id"] == crew_id), None)


def get_pirate_by_id(pirate_id: int) -> Optional[dict]:
    return next((p for p in pirates_db if p["id"] == pirate_id), None)
