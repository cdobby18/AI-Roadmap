import json
from pathlib import Path
from typing import List, Dict, Any

# Path to storage file
STORAGE_FILE = Path(__file__).parent / "issues.json"


def load_data() -> List[Dict[str, Any]]:
    """Load issues from JSON file"""
    if not STORAGE_FILE.exists():
        return []
    with open(STORAGE_FILE, "r") as f:
        return json.load(f)


def save_data(data: List[Dict[str, Any]]) -> None:
    """Save issues to JSON file"""
    with open(STORAGE_FILE, "w") as f:
        json.dump(data, f, indent=2)
