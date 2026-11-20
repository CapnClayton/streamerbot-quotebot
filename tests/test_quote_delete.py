from typing import Any

import pytest

from conftest import QuoteBot


def test_delete_middle_quote_renumbers_later_quotes(bot: QuoteBot) -> None:
    assert bot.run("quote_delete", "2") == "Successfully deleted quote 2"

    data = bot.read_quotes()
    assert [q["id"] for q in data["quotes"]] == [1, 2]
    assert (
        data["quotes"][1]["gameName"] == "Rocket League"
    )  # Quote shifted back/updated
    assert data["nextId"] == 3


def test_delete_last_quote(bot: QuoteBot) -> None:
    bot.run("quote_delete", "3")

    data = bot.read_quotes()
    assert [q["id"] for q in data["quotes"]] == [1, 2]
    assert data["nextId"] == 3


def test_add_after_delete_uses_updated_next_id(bot: QuoteBot) -> None:
    bot.run("quote_delete", "1")

    assert bot.run(
        "quote_add", "214", "CheeseCurdLover", "999", "Celeste", "Hello"
    ) == "CheeseCurdLover has successfully added quote 3!"


@pytest.mark.parametrize("quote_id", ["0", "4", "-1"])
def test_delete_out_of_range_leaves_file_unchanged(
    bot: QuoteBot, sample_quotes: dict[str, Any], quote_id: str
) -> None:
    assert bot.run("quote_delete", quote_id) == f"No quote with id {quote_id} exists"
    assert bot.read_quotes() == sample_quotes


def test_delete_non_numeric(bot: QuoteBot, sample_quotes: dict[str, Any]) -> None:
    assert bot.run("quote_delete", "abc") == "abc isn't a number. Try again."
    assert bot.read_quotes() == sample_quotes


def test_delete_without_id(bot: QuoteBot) -> None:
    assert bot.run("quote_delete") == "You must pass a quote id to search quotes!"
