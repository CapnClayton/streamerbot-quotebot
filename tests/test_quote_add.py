import re
from typing import Any

import pytest

from conftest import QuoteBot

# Streamer.bot format, ex// 2023-07-25T21:47:54.6192662-05:00
TIMESTAMP_RE = re.compile(
    r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{7}[+-]\d{2}:\d{2}$"
)


def test_add_appends_quote_with_next_id(bot: QuoteBot) -> None:
    output = bot.run(
        "quote_add", "214", "CheeseCurdLover", "999", "Celeste", "Climb the mountain"
    )

    assert output == "CheeseCurdLover has successfully added quote 4!"
    data = bot.read_quotes()
    assert data["nextId"] == 5
    new = data["quotes"][-1]
    assert new["id"] == 4
    assert new["userId"] == "214"
    assert new["user"] == "CheeseCurdLover"
    assert new["platform"] == "twitch"
    assert new["gameId"] == "999"
    assert new["gameName"] == "Celeste"
    assert new["quote"] == '"Climb the mountain"'


def test_add_keeps_existing_quotes_and_key_order(
    bot: QuoteBot, sample_quotes: dict[str, Any]
) -> None:
    bot.run("quote_add", "214", "CheeseCurdLover", "999", "Celeste", "Hello")

    data = bot.read_quotes()
    assert data["quotes"][:3] == sample_quotes["quotes"]
    assert list(data["quotes"][-1].keys()) == list(sample_quotes["quotes"][0].keys())


def test_add_without_next_id_uses_max_id(
    bot: QuoteBot, sample_quotes: dict[str, Any]
) -> None:
    del sample_quotes["nextId"]
    bot.write_quotes(sample_quotes)

    bot.run("quote_add", "214", "CheeseCurdLover", "999", "Celeste", "Hello")

    data = bot.read_quotes()
    assert data["quotes"][-1]["id"] == 4
    assert data["nextId"] == 5


def test_add_strips_smart_and_straight_quotes(bot: QuoteBot) -> None:
    bot.run(
        "quote_add",
        "214",
        "CheeseCurdLover",
        "999",
        "Celeste",
        '“Smart” and "straight"',
    )

    assert bot.read_quotes()["quotes"][-1]["quote"] == '"Smart and straight"'


def test_add_unquoted_multi_word_text_is_joined(bot: QuoteBot) -> None:
    bot.run(
        "quote_add",
        "214",
        "CheeseCurdLover",
        "999",
        "Celeste",
        "multiple",
        "loose",
        "words",
    )

    assert bot.read_quotes()["quotes"][-1]["quote"] == '"multiple loose words"'


def test_add_attributed_quote_is_kept_as_is(bot: QuoteBot) -> None:
    bot.run(
        "quote_add",
        "214",
        "CheeseCurdLover",
        "999",
        "Celeste",
        '"Nice"',
        "-",
        "@DaveViewer",
    )

    assert bot.read_quotes()["quotes"][-1]["quote"] == '"Nice" - @DaveViewer'


def test_add_timestamp_matches_streamerbot_format_in_utc_by_default(
    bot: QuoteBot,
) -> None:
    bot.run("quote_add", "214", "CheeseCurdLover", "999", "Celeste", "Hello")

    timestamp = bot.read_quotes()["quotes"][-1]["timestamp"]
    assert TIMESTAMP_RE.match(timestamp), timestamp
    assert timestamp.endswith("+00:00")


def test_add_uses_configured_timezone(bot: QuoteBot) -> None:
    bot.write_config(timezone="America/Chicago")

    bot.run("quote_add", "214", "CheeseCurdLover", "999", "Celeste", "Hello")

    timestamp = bot.read_quotes()["quotes"][-1]["timestamp"]
    assert TIMESTAMP_RE.match(timestamp), timestamp
    assert timestamp[-6:] in ("-06:00", "-05:00")  # CST or CDT


@pytest.mark.parametrize("bad_timezone", ["Not/ARealZone", '""'])
def test_add_invalid_timezone_falls_back_to_utc(
    bot: QuoteBot, bad_timezone: str
) -> None:
    bot.write_config(timezone=bad_timezone)

    bot.run("quote_add", "214", "CheeseCurdLover", "999", "Celeste", "Hello")

    assert bot.read_quotes()["quotes"][-1]["timestamp"].endswith("+00:00")


def test_add_creates_quote_file_when_missing(bot: QuoteBot) -> None:
    bot.quotes_path.unlink()

    output = bot.run("quote_add", "214", "CheeseCurdLover", "999", "Celeste", "1st")

    assert output == "CheeseCurdLover has successfully added quote 1!"
    data = bot.read_quotes()
    assert data["version"] == 0
    assert data["nextId"] == 2
    assert [q["id"] for q in data["quotes"]] == [1]
    assert data["quotes"][0]["quote"] == '"1st"'


def test_add_to_empty_quote_list_without_next_id(bot: QuoteBot) -> None:
    bot.write_quotes({"quotes": []})

    output = bot.run("quote_add", "214", "CheeseCurdLover", "999", "Celeste", "1st")

    assert output == "CheeseCurdLover has successfully added quote 1!"
    assert bot.read_quotes()["nextId"] == 2
