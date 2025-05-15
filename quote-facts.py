import random
import sys

from collections import Counter
from typing import Optional

from quote_utils import get_quote_dicts
from quote_utils import write_result

COLLOQUIAL_STREAMER_NAME = ""  # TODO: Pull this from config

WORDS_TO_COUNT_FOR_FACTS = [
]
WORD_COUNT_SENTENCE_VARIANTS = [
	f"{COLLOQUIAL_STREAMER_NAME} has been quoted as saying \"{word}\" precisely {count} times!",
	"Can you believe streamer has said \"{word}\" {count} times?",
	f"Of course \"{word}\" has been quoted {count} times. Would you expect any less of {COLLOQUIAL_STREAMER_NAME}?",
	f"Oh \"{word}\"! Yeah, that's something {COLLOQUIAL_STREAMER_NAME} has probably said. It's in {count} quotes after all."
]


def _get_count_of_quotes_containing_word(word: str, quote_dicts: dict, is_capn: Optional[bool] = True) -> int:
	count = 0
	for qd in quote_dicts:
		quote = qd["quote"].lower()
		if word in quote:
			# This could be collapsed into a single conditional, but this is easier to read
			if is_capn and "@" not in quote:
				count += 1
			elif not is_capn:
				count += 1
	return count

def _generate_facts(quote_dicts: dict) -> list:
	facts = [
		"The first quote was added on 2023/07/25 by CapnCeedee via a clip created by jspiscool!",
		f"There are {len(quote_dicts)} quotes!",
	]

	# User with most quotes contributed
	user, count = Counter({qd["id"]: qd["user"] for qd in quote_dicts}.values()).most_common(1)[0]
	facts.append(f"{user} has added the most quotes! {count} and counting!")

	# Amount of quote contributors
	user_count = len(set({qd["id"]: qd["userId"] for qd in quote_dicts}.values()))
	facts.append(f"{user_count} different people have contributed quotes!")

	# Date with most quotes contributed
	date, count = Counter({qd["id"]: qd["timestamp"].split("T")[0] for qd in quote_dicts}.values()).most_common(1)[0]
	facts.append(f"The most quotes in a day ({count}) occurred on {date}!")
	
	# Game with the most quotes
	game, count = Counter({qd["id"]: qd["gameName"] for qd in quote_dicts}.values()).most_common(1)[0]
	facts.append(f"The game with the most quotes is {game} with {count} quotes!")

	# Quotes from other users
	facts.append(f"There are {_get_count_of_quotes_containing_word("@", quote_dicts, is_capn=False)} quotes that are from the community, and not CAPN !")
	
	# Generate word count stats
	for word in WORDS_TO_COUNT_FOR_FACTS:
		random.shuffle(WORD_COUNT_SENTENCE_VARIANTS)
		facts.append(
			WORD_COUNT_SENTENCE_VARIANTS[0].format(
				word=word,
				count=_get_count_of_quotes_containing_word(word, quote_dicts),
			)
		)

	return facts

def get_fact_text():
	quote_dicts = get_quote_dicts()
	
	facts = _generate_facts(quote_dicts)
	random.shuffle(facts)
	return facts[0]

def main():
	write_result("quote_fact.txt", get_fact_text())

main()
