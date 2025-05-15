"""
This could be replaced with reading a latest_quote.txt file
if adding quotes just updates that file in the future.
"""

from quote_utils import get_quote_dicts
from quote_utils import write_result


def get_quote_text():
	quote_dicts = get_quote_dicts()
	# Naively assume last item is latest quote
	q = quote_dicts[-1]
	number = q["id"]
	text = q["quote"]
	game = q["gameName"]
	date = q["timestamp"].split("T")[0]
	return f"Quote #{number}: {text} [{game} | {date}]"

def main():
	write_result("latest_quote.txt", get_quote_text())

main()
