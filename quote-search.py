import random
import sys

from quote_utils import get_quote_dicts
from quote_utils import write_result


def get_quote_text():
	try:
		search_word = sys.argv[1]
	except IndexError:
		return "You must pass a word to search quotes!"

	quote_dicts = get_quote_dicts()
	quotes = [quote for quote in quote_dicts if search_word.lower() in quote["quote"].lower()]
	random.shuffle(quotes)

	if quotes:
		q = quotes[0]
		number = q["id"]
		text = q["quote"]
		game = q["gameName"]
		date = q["timestamp"].split("T")[0]
		return f"Quote #{number}: {text} [{game} | {date}]"
	else:
		return f"No quote found with {search_word}"

def main():
	write_result("quote_output.txt", get_quote_text())

main()
