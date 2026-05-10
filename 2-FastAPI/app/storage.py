from pathlib import Path
import json

# Create data folder path
DATA_DIR = Path("data")

# Create JSON file path
DATA_FILE = DATA_DIR / "issues.json"

# Load data from JSON file
def load_data():

    # Check if file exists
    if DATA_FILE.exists():

        # Open file in read mode
        with open(DATA_FILE, "r") as f:

            # Read file content
            content = f.read()

            # Check if file is not empty
            if content.strip():

                # Convert JSON string into Python object
                return json.loads(content)

    # Return empty list if no data exists
    return []

# Save data into JSON file
def save_data(data):

    # Create folder if it does not exist
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    # Open file in write mode
    with open(DATA_FILE, "w") as f:

        # Convert Python object into JSON format
        json.dump(data, f, indent=2)