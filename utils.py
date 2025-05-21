import json

from typing import Dict
from typing import List

QUOTE_FILE = "quotes.json"

def get_quote_file() -> Dict:
	with open(QUOTE_FILE, "r", encoding="utf8") as quote_file:
		quote_file_raw = quote_file.read()
		return json.loads(quote_file_raw)

def get_quote_dicts() -> List[Dict]:
	return get_quote_file()["quotes"]

def write_result(outfile_name: str, data: str):
	with open(outfile_name, "w", encoding="utf-8") as outfile:
		outfile.write(data)
