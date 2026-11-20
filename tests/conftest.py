import copy
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
FIXTURES = Path(__file__).resolve().parent / "fixtures"

OUTPUT_FILES = {
    "quote_add": "quote_add_output.txt",
    "quote_delete": "quote_delete_result.txt",
    "quote_facts": "quote_fact.txt",
    "quote_get": "quote.txt",
    "quote_latest": "latest_quote.txt",
    "quote_search": "quote_output.txt",
}


@pytest.fixture
def sample_quotes() -> dict[str, Any]:
    with open(FIXTURES / "quotes.json", encoding="utf8") as f:
        quotes: dict[str, Any] = json.load(f)
    return quotes


class QuoteBot:
    def __init__(self, workdir: Path, quotes: dict[str, Any]) -> None:
        self.workdir = workdir
        self.quotes_path = workdir / "quotes.json"
        self.write_quotes(quotes)

    def write_quotes(self, quotes: dict[str, Any]) -> None:
        self.quotes_path.write_text(json.dumps(quotes, indent=2), encoding="utf8")

    def read_quotes(self) -> dict[str, Any]:
        quotes: dict[str, Any] = json.loads(self.quotes_path.read_text(encoding="utf8"))
        return quotes

    def write_config(self, **settings: str) -> None:
        lines = [f"{key}: {value}" for key, value in settings.items()]
        (self.workdir / "config.yaml").write_text(
            "\n".join(lines) + "\n", encoding="utf8"
        )

    def run(self, script: str, *args: str) -> str:
        """Run a script and return the contents of its output file."""
        result = subprocess.run(
            [sys.executable, str(REPO_ROOT / f"{script}.py"), *args],
            cwd=self.workdir,
            capture_output=True,
            text=True,
            encoding="utf8",
        )
        assert (
            result.returncode == 0
        ), f"{script} exited {result.returncode}:\n{result.stderr}"
        return (self.workdir / OUTPUT_FILES[script]).read_text(encoding="utf8")


@pytest.fixture
def bot(tmp_path: Path, sample_quotes: dict[str, Any]) -> QuoteBot:
    return QuoteBot(tmp_path, copy.deepcopy(sample_quotes))
