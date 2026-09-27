import csv
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).parent
SCRIPT = ROOT / "clean_csv.py"

with tempfile.TemporaryDirectory() as temporary:
    folder = Path(temporary)
    source = folder / "source.csv"
    destination = folder / "clean.csv"
    source.write_text(" Full Name , Email Address \n Alice , alice@example.com \nAlice,alice@example.com\n,\n Bob , bob@example.com \n", encoding="utf-8")
    preview = subprocess.run([sys.executable, str(SCRIPT), str(source), str(destination)], capture_output=True, text=True, check=True)
    assert "Would write 2 rows" in preview.stdout
    assert not destination.exists()
    subprocess.run([sys.executable, str(SCRIPT), str(source), str(destination), "--apply"], capture_output=True, text=True, check=True)
    with destination.open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream))
    assert rows == [{"full_name": "Alice", "email_address": "alice@example.com"}, {"full_name": "Bob", "email_address": "bob@example.com"}]

print("CSV cleaner test passed")
