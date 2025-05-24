import json
from pathlib import Path

def load_test_data(filename):
    path = Path(__file__).parent.parent / "testdata" / filename
    with open(path, "r") as f:
        return json.load(f)
