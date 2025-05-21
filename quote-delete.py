import json
import random
import sys

from utils import get_quote_file
from utils import write_result


def get_quote_delete_result():
	try:
		quote_id_to_delete = int(sys.argv[1])
	except IndexError:
		return "You must pass a quote id to search quotes!"
	except (ValueError, TypeError):
		return f"{sys.argv[1]} isn't a number. Try again."

	quote_file = get_quote_file()
	quote_dicts = quote_file["quotes"]
	if quote_id_to_delete < 1 or quote_id_to_delete > len(quote_dicts):
		return f"No quote with id {quote_id_to_delete} exists"
	
	quotes_to_keep = list()
	for quote in sorted(quote_dicts, key=lambda q: int(q["id"])):
		quote_id = int(quote["id"])
		if quote_id == quote_id_to_delete:
			continue
		elif quote_id > quote_id_to_delete:
			quote["id"] = quote_id - 1
		quotes_to_keep.append(quote)
	quote_file["quotes"] = quotes_to_keep

	with open("quotes.json", "w", encoding="utf-8") as outfile:
		json.dump(quote_file, outfile, indent=2, ensure_ascii=False)

	return f"Successfully deleted quote {quote_id_to_delete}"
	

def main():
	write_result("quote_delete_result.txt", get_quote_delete_result())

main()
