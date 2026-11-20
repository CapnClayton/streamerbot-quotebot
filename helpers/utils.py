import json

from helpers.types import Quote
from helpers.types import QuoteFile

QUOTE_FILE = "quotes.json"
MISSING_QUOTE_FILE_MESSAGE = (
    f"Can't find the quote file ({QUOTE_FILE}). Adding a quote will create it."
)


class QuoteFileNotFoundError(FileNotFoundError):
    pass


def get_quote_file() -> QuoteFile:
    try:
        with open(QUOTE_FILE, "r", encoding="utf8") as quote_file:
            quote_file_raw = quote_file.read()
    except FileNotFoundError as e:
        raise QuoteFileNotFoundError(e.errno, e.strerror, e.filename) from e
    quote_file_data: QuoteFile = json.loads(quote_file_raw)
    return quote_file_data


def get_quote_dicts() -> list[Quote]:
    quotes: list[Quote] = get_quote_file()["quotes"]
    return quotes


def write_result(outfile_name: str, data: str) -> None:
    with open(outfile_name, "w", encoding="utf-8") as outfile:
        outfile.write(data)
