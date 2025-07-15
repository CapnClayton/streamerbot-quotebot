import json
import pytz
import sys

from collections import OrderedDict
from datetime import datetime
from typing import List

from constants import DEFAULT_TIMEZONE_STR
from constants import TIMEZONE
from utils import write_result

try:
    timezone = pytz.timezone(TIMEZONE)
except pytz.exceptions.UnknownTimeZoneError:
    timezone = pytz.timezone(DEFAULT_TIMEZONE_STR)


def _is_direct_quote(cmd_args: List[str]) -> bool:
    if len(cmd_args) == 6:
        # Naively yes: ex// quote-add.py <user_id> CapnCeedee <game_id> "Persona 5 Royal" "This is a quote"
        return True
    return False


def _wrap_quote(quote_str: str) -> str:
    return f"\"{quote_str.replace("\"", "").replace("“", "").replace("”", "")}\""


def _get_quote_time() -> str:
    """
    Make the time format match Streamerbot's quote time format
    ex// 2023-07-25T21:47:54.6192662-05:00
    """
    dt = datetime.now(timezone)
    formatted_dt = f"{dt.strftime('%Y-%m-%dT%H:%M:%S.%f')}0{dt.strftime('%z')}"
    return f"{formatted_dt[:-2]}:{formatted_dt[-2:]}"


def format_quote(cmd_args: List[str]) -> str:
    if _is_direct_quote(cmd_args):
        return _wrap_quote(cmd_args[-1])
    data = " ".join(cmd_args[5:])
    if "@" not in data:
        return _wrap_quote(data)
    # Naively assume it's correct already
    return data


def append_to_quote_json(
        user_id: str,
        username: str,
        game_id: str,
        game: str,
        file_loc: str,
        quote_text: str,
):
    """
    JSON file exists as:
        {
          "version": 0,
          "t": "2025-05-07T17:44:31.9296476-05:00",
          "quotes": [
            {
              "timestamp": "2023-07-25T21:47:54.6192662-05:00",
              "id": 1,
              "userId": "56805015",
              "user": "CapnCeedee",
              "platform": "twitch",
              "gameId": "511864",
              "gameName": "Persona 5 Royal",
              "quote": "\"This is a quote\""
            },
            ...
          ]
        }
    """
    with open(file_loc, "r", encoding="utf8") as f:
        quote_data: dict = json.loads(f.read())
    quote_id = max(qd["id"] for qd in quote_data["quotes"]) + 1
    # Use ordered dict to ensure keys don't randomize between quotes
    new_quote_dict = OrderedDict([
        ("timestamp", _get_quote_time()),
        ("id", quote_id),
        ("userId", user_id),
        ("user", username),
        ("platform", "twitch"),
        ("gameId", game_id),
        ("gameName", game),
        ("quote", quote_text),
    ])
    quote_data["quotes"].append(new_quote_dict)
    with open(file_loc, "w", encoding="utf8") as f:
        f.write(json.dumps(quote_data, indent=2, ensure_ascii=False))
    return f"{username} has successfully added quote {str(quote_id)}!"


def add_quote(cmd_args: List[str], quote_file_loc: str) -> str:
    quote_text = format_quote(cmd_args)
    if not quote_text:
        return "You must provide text to add a quote"
    return append_to_quote_json(
        cmd_args[1],
        cmd_args[2],
        cmd_args[3],
        cmd_args[4],
        quote_file_loc,
        quote_text,
    )


def main():
    """
    Invoked as:
        - quote-add.py <user_id> <username> <game_id> <game> "<quote text>"
        - quote-add.py <user_id> <username> <game_id> <game> <quote text>
        - quote-add.py <user_id> <username> <game_id> <game> <quote text> - @<username>
    """
    quote_file = "quotes.json"
    write_result("quote_add_output.txt", add_quote(sys.argv, quote_file))


main()
