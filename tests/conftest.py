import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))  # so `from tools.check_parity import ...` resolves


@pytest.fixture
def heading_map():
    return json.loads((ROOT / "tools" / "heading_map.json").read_text(encoding="utf-8"))


@pytest.fixture
def trees(tmp_path):
    """Return (en_dir, zh_dir, write) where write(tree, relpath, text) creates a file."""
    en = tmp_path / "en"
    zh = tmp_path / "zh"
    en.mkdir()
    zh.mkdir()

    def write(tree, relpath, text):
        p = tree / relpath
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")
        return p

    return en, zh, write
