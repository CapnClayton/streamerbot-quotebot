import pytest

from conftest import QuoteBot

MISSING_MESSAGE = (
    "Can't find the quote file (quotes.json). Adding a quote will create it."
)


@pytest.mark.parametrize(
    ("script", "args"),
    [
        ("quote_get", ()),
        ("quote_get", ("2",)),
        ("quote_get", ("-1",)),
        ("quote_latest", ()),
        ("quote_search", ("thou",)),
        ("quote_facts", ()),
        ("quote_delete", ("1",)),
    ],
)
def test_missing_quote_file_reports_message(
    bot: QuoteBot, script: str, args: tuple[str, ...]
) -> None:
    bot.quotes_path.unlink()

    assert bot.run(script, *args) == MISSING_MESSAGE
    assert not bot.quotes_path.exists()


def test_add_after_missing_message_creates_file(bot: QuoteBot) -> None:
    bot.quotes_path.unlink()
    assert bot.run("quote_get") == MISSING_MESSAGE

    bot.run("quote_add", "214", "CheeseCurdLover", "999", "Celeste", "Test...")

    assert bot.run("quote_get", "1").startswith('Quote #1: "Test..." [Celeste | ')
