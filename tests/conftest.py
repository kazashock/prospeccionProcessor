import json
from pathlib import Path

import pytest

CONFIG_DIR = Path(__file__).resolve().parent.parent / "config"


@pytest.fixture
def headers_config():
    return json.loads((CONFIG_DIR / "headers.json").read_text(encoding="utf-8"))


@pytest.fixture
def rules_config():
    return json.loads((CONFIG_DIR / "rules.json").read_text(encoding="utf-8"))
