import json

from typing import Dict
from typing import List

QUOTE_FILE = "quotes.json"
MISSING_QUOTE_FILE_MESSAGE = (
    f"Can't find the quote file ({QUOTE_FILE}). Adding a quote will create it."
)


class QuoteFileNotFoundError(FileNotFoundError):
    pass


def get_quote_file() -> Dict:
    try:
        with open(QUOTE_FILE, "r", encoding="utf8") as quote_file:
            quote_file_raw = quote_file.read()
    except FileNotFoundError as e:
        raise QuoteFileNotFoundError(e.errno, e.strerror, e.filename) from e
    return json.loads(quote_file_raw)


def get_quote_dicts() -> List[Dict]:
    return get_quote_file()["quotes"]


def write_result(outfile_name: str, data: str):
    with open(outfile_name, "w", encoding="utf-8") as outfile:
        outfile.write(data)
