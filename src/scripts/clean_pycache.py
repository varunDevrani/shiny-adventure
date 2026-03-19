from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path("src")

for cache in ROOT.rglob("__pycache__"):
    shutil.rmtree(cache)
    print(f"Removed {cache}")
