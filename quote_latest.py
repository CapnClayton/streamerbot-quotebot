"""
This could be replaced with reading a latest_quote.txt file
if adding quotes just updates that file in the future.
"""

from helpers.utils import MISSING_QUOTE_FILE_MESSAGE
from helpers.utils import QuoteFileNotFoundError
from helpers.utils import get_quote_dicts
from helpers.utils import write_result


def get_quote_text() -> str:
    quote_dicts = get_quote_dicts()
    # Naively assume last item is latest quote
    q = quote_dicts[-1]
    number = q["id"]
    text = q["quote"]
    game = q["gameName"]
    date = q["timestamp"].split("T")[0]
    return f"Quote #{number}: {text} [{game} | {date}]"


def main() -> None:
    try:
        text = get_quote_text()
    except QuoteFileNotFoundError:
        text = MISSING_QUOTE_FILE_MESSAGE
    write_result("latest_quote.txt", text)


main()
