import random
import sys

from utils import MISSING_QUOTE_FILE_MESSAGE
from utils import Quote
from utils import QuoteFileNotFoundError
from utils import get_quote_dicts
from utils import write_result


def parse_quote_id(args: list[str]) -> int | None:
    """
    Return the requested quote number, or None when no number was given.

    Raises ValueError when the argument is not a whole number.
    """
    if len(args) < 2:
        return None
    return int(args[1])


def format_quote(quote: Quote) -> str:
    number = quote["id"]
    text = quote["quote"]
    game = quote["gameName"]
    date = quote["timestamp"].split("T")[0]
    return f"Quote #{number}: {text} [{game} | {date}]"


def get_quote_text(quote_id: int | None) -> str:
    """
    - None: a random quote
    - Positive: the quote with that id
    - Negative: counts back from the latest quote (-1 is the latest)
    - 0: Special case // no quote
    """
    quote_dicts = sorted(get_quote_dicts(), key=lambda qd: int(qd["id"]))
    if not quote_dicts:
        return "There are no quotes yet!"

    if quote_id is None:
        return format_quote(random.choice(quote_dicts))

    if quote_id == 0:
        return "There is no quote #0! Quotes start at #1."

    if quote_id < 0:
        if -quote_id > len(quote_dicts):
            return f"Quote {quote_id} does not exist! We only have {len(quote_dicts)} quotes."
        return format_quote(quote_dicts[quote_id])

    max_id = int(quote_dicts[-1]["id"])
    if quote_id > max_id:
        return f"Quote with id {quote_id} does not exist! We only have {max_id} quotes."

    for quote in quote_dicts:
        if int(quote["id"]) == quote_id:
            return format_quote(quote)
    return f"Quote with id {quote_id} does not exist!"


def main() -> None:
    try:
        quote_id = parse_quote_id(sys.argv)
    except ValueError:
        # This also gets invoked on quote add so bail out with an
        #  empty string so we don't post a message
        write_result("quote.txt", "")
        return
    try:
        text = get_quote_text(quote_id)
    except QuoteFileNotFoundError:
        text = MISSING_QUOTE_FILE_MESSAGE
    write_result("quote.txt", text)


main()
