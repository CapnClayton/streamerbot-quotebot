import random
import sys

from quote_utils import get_quote_dicts
from quote_utils import write_result

RANDOM_QUOTE_IDENTIFIER = -1
IMPROPER_TYPE = -2
ERROR = 0


def parse_quote_id():
	try:
		return int(sys.argv[1])
	except IndexError:
		return RANDOM_QUOTE_IDENTIFIER
	except (TypeError, ValueError):
		return IMPROPER_TYPE
	except Exception:
		return ERROR


def get_quote_text(quote_id: int):
	quote_dicts = get_quote_dicts()
	max_id = max(qd["id"] for qd in quote_dicts)
	if quote_id == RANDOM_QUOTE_IDENTIFIER:
		quote_id = random.randint(1, max_id)
	elif quote_id > max_id:
		return f"Quote with id {quote_id} does not exist! We only have {max_id} quotes."

	for qd in quote_dicts:
		if qd["id"] == quote_id:
			break
	
	number = qd["id"]
	text = qd["quote"]
	game = qd["gameName"]
	date = qd["timestamp"].split("T")[0]
	return f"Quote #{number}: {text} [{game} | {date}]"

def main():
	quote_id = parse_quote_id()
	if quote_id == ERROR:
		text = "Something went wrong with the quote bot D: "
	elif quote_id == IMPROPER_TYPE:
		# This also gets invoked on quote add so bail out with an 
		#  empty string so we don't post a message
		text = ""
	else:
		text = get_quote_text(quote_id)
	write_result("quote.txt", text)

main()
