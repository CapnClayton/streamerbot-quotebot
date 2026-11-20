from conftest import QuoteBot

QUOTE_1 = 'Quote #1: "I am thou, thou art I" [Persona 5 Royal | 2023-07-25]'
QUOTE_2 = 'Quote #2: "Take your time" [Persona 5 Royal | 2023-07-25]'
QUOTE_3 = 'Quote #3: "That was a great play" - @DakPrescottNo2Fan [Rocket League | 2024-01-02]'
ALL_QUOTES = {QUOTE_1, QUOTE_2, QUOTE_3}


def test_get_by_id(bot: QuoteBot) -> None:
    assert bot.run("quote_get", "2") == QUOTE_2


def test_get_without_id_returns_a_random_quote(bot: QuoteBot) -> None:
    assert bot.run("quote_get") in ALL_QUOTES


def test_get_id_too_large(bot: QuoteBot) -> None:
    assert (
        bot.run("quote_get", "99")
        == "Quote with id 99 does not exist! We only have 3 quotes."
    )


def test_get_non_numeric_writes_empty_output(bot: QuoteBot) -> None:
    assert bot.run("quote_get", "add") == ""


def test_latest_returns_last_quote(bot: QuoteBot) -> None:
    assert bot.run("quote_latest") == QUOTE_3


def test_latest_after_add(bot: QuoteBot) -> None:
    bot.run(
        "quote_add", "214", "CheeseCurdLover", "999", "Celeste", "Climb the mountain"
    )

    assert bot.run("quote_latest").startswith(
        'Quote #4: "Climb the mountain" [Celeste | '
    )


def test_search_is_case_insensitive(bot: QuoteBot) -> None:
    assert bot.run("quote_search", "THOU") == QUOTE_1


def test_search_matches_one_of_several(bot: QuoteBot) -> None:
    assert bot.run("quote_search", "t") in ALL_QUOTES


def test_search_no_match(bot: QuoteBot) -> None:
    assert bot.run("quote_search", "zebra") == "No quote found with zebra"


def test_search_without_term(bot: QuoteBot) -> None:
    assert bot.run("quote_search") == "You must pass a word to search quotes!"


def test_facts_returns_a_known_fact(bot: QuoteBot) -> None:
    expected = {
        "The first quote was added on 2023/07/25 by CapnCeedee via a clip created by jspiscool!",
        "There are 3 quotes!",
        "WiglettsAnonymous has added the most quotes! 2 and counting!",
        "2 different people have contributed quotes!",
        "The most quotes in a day (2) occurred on 2023-07-25!",
        "The game with the most quotes is Persona 5 Royal with 2 quotes!",
        "There are 1 quotes that are from the community, and not CAPN !",
    }

    assert bot.run("quote_facts") in expected
