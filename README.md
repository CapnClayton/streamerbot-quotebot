# streamerbot-quotebot

[![CI](https://github.com/CapnClayton/streamerbot-quotebot/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/CapnClayton/streamerbot-quotebot/actions/workflows/ci.yml)
![Python 3.12 | 3.13 | 3.14](https://img.shields.io/badge/python-3.12%20%7C%203.13%20%7C%203.14-blue)
![Tested on Windows | Ubuntu](https://img.shields.io/badge/tested%20on-Windows%20%7C%20Linux-informational)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

An alternative quote system for **Streamerbot** with expanded functionality. This is a Python-based quote management system designed to integrate with Streamerbot for managing memorable moments and quotes from your stream.

CI runs on Windows and Ubuntu (Python 3.12-3.14).

## Features

- **Add quotes** with associated metadata (user, game, timestamp)
- **Retrieve quotes** by ID or get a random quote
- **Search quotes** by text
- **Delete quotes**, renumbering later quotes so IDs stay sequential
- **Quote facts** tracking and statistics
- **Timezone support** with timestamps in Streamerbot's format
- **JSON-based storage** which is backwards-compatible with Streamerbot's quote format
- **Customizable username** for colloquial references in outputs

## Installation

### Prerequisites

- Python 3.12+
- Streamerbot installation (for integration)

### Setup

1. Clone or download this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Copy and configure the config file:
   ```bash
   cp config.example.yaml config.yaml      # macOS / Linux
   copy config.example.yaml config.yaml    # Windows
   ```
4. Edit `config.yaml` with your settings (see [Configuration](#configuration) below)
5. Put your quotes file at `quotes.json` in the folder you run the scripts from (see [Quote file format](#quote-file-format)). It is **not** created automatically.

## Try it without Streamer.bot

You can check your setup in about a minute using the sample quotes the test suite uses. Run these from the repository root:

```bash
cp tests/fixtures/quotes.json quotes.json     # Windows: copy tests\fixtures\quotes.json quotes.json

python quote_get.py 2
python quote_search.py thou
python quote_add.py 214 CheeseCurdLover 999 Celeste "Climb the mountain"
python quote_latest.py
python quote_delete.py 4
```

Each script writes its result to a text file (see [Output files](#output-files)) rather than printing it. You should see:

| Command | Output file | Contents |
|---|---|---|
| `quote_get.py 2` | `quote.txt` | `Quote #2: "Take your time" [Persona 5 Royal \| 2023-07-25]` |
| `quote_search.py thou` | `quote_output.txt` | `Quote #1: "I am thou, thou art I" [Persona 5 Royal \| 2023-07-25]` |
| `quote_add.py ...` | `quote_add_output.txt` | `CheeseCurdLover has successfully added quote 4!` |
| `quote_latest.py` | `latest_quote.txt` | `Quote #4: "Climb the mountain" [Celeste \| <today's date>]` |
| `quote_delete.py 4` | `quote_delete_result.txt` | `Successfully deleted quote 4` |

Delete the sample `quotes.json` when you're done so it doesn't get mixed up with your real quotes.

## Configuration

Create a `config.yaml` file in the project root with the following settings:

```yaml
# Your username (or colloquial version used on stream)
# Used in quote fact outputs
colloquial_username: Capn

# Valid IANA timezone name
# See: https://en.wikipedia.org/wiki/List_of_tz_database_time_zones
timezone: America/Chicago
```

If `config.yaml` is not found, defaults will be used:
- `colloquial_username`: "streamer"
- `timezone`: "UTC"

An unknown or empty `timezone` falls back to UTC.

## Usage

All scripts read `quotes.json` and `config.yaml` from the **current working directory** and write their result to a text file in that same directory.

### Commands

#### Add a Quote
```bash
python quote_add.py <user_id> <username> <game_id> <game_name> "<quote_text>"
python quote_add.py <user_id> <username> <game_id> <game_name> <quote text without quotes>
python quote_add.py <user_id> <username> <game_id> <game_name> "<quote_text>" - @<username>
```
Adds a new quote with a timestamp and the given metadata. Quote marks in the text (including smart quotes) are normalized. A quote attributed with `- @username` is stored as-is.

#### Get a Quote
```bash
python quote_get.py [quote_id]
```
- `quote_get.py` - Returns a random quote
- `quote_get.py 5` - Returns quote with ID 5
- `quote_get.py -1` - Returns the latest quote. Negative numbers count back from the latest, so `-2` is the one before it.

#### Latest Quote
```bash
python quote_latest.py
```
Retrieves the most recently added quote.

#### Search Quotes
```bash
python quote_search.py <search_term>
```
Returns a random quote whose text contains the search term (case-insensitive).

#### Delete a Quote
```bash
python quote_delete.py <quote_id>
```
Removes a quote by ID. Quotes after it move down one ID so the IDs stay sequential.

#### Quote Facts
```bash
python quote_facts.py
```
Returns one random fact about your quotes, such as the total count, the top contributor, or the game with the most quotes.

> **Forking?** Edit `_generate_facts` to fit your own channel's brand and needs.

## Quote file format

`quotes.json` uses the same layout as Streamer.bot's quote data:

```json
{
  "version": 0,
  "t": "2025-05-07T17:44:31.9296476-05:00",
  "nextId": 2,
  "quotes": [
    {
      "timestamp": "2023-07-25T21:47:54.6192662-05:00",
      "id": 1,
      "userId": "56805015",
      "user": "CapnCeedee",
      "platform": "twitch",
      "gameId": "511864",
      "gameName": "Persona 5 Royal",
      "quote": "\"I can't wait to see Takemi again\""
    }
  ]
}
```

- `nextId` is optional. If it is missing, the next ID is calculated from the existing quotes, and `nextId` is added on the next add or delete.
- To start with no quotes, use `{"nextId": 1, "quotes": []}`.

See [`tests/fixtures/quotes.json`](tests/fixtures/quotes.json) for a complete example.

## File Structure

```
streamerbot-quotebot/
├── quote_add.py              # Add new quotes
├── quote_delete.py           # Delete quotes
├── quote_facts.py            # View quote statistics
├── quote_get.py              # Retrieve quotes
├── quote_latest.py           # Get most recent quote
├── quote_search.py           # Search quotes
├── constants.py              # Configuration and constants
├── utils.py                  # Shared utilities
├── config.example.yaml       # Configuration template
├── requirements.txt          # Runtime dependencies
├── requirements-dev.txt      # Test and lint dependencies
├── pyproject.toml            # Black settings
├── pytest.ini                # pytest settings
├── tests/                    # Test suite and sample quotes.json
├── .github/workflows/ci.yml  # CI: tests and lint checks
└── README.md                 # This file
```

### Output Files

Each script writes its result to a text file for Streamerbot to read. The file is created the first time the script runs, and git ignores these files to avoid accidental commits.

| Script | Output file |
|---|---|
| `quote_add.py` | `quote_add_output.txt` |
| `quote_delete.py` | `quote_delete_result.txt` |
| `quote_facts.py` | `quote_fact.txt` |
| `quote_get.py` | `quote.txt` |
| `quote_latest.py` | `latest_quote.txt` |
| `quote_search.py` | `quote_output.txt` |

## Dependencies

- **pyyaml** - Configuration file parsing
- **tzdata** - IANA timezone database for `zoneinfo` (required on Windows)

See `requirements.txt` for version details.

## Integration with Streamerbot

To use these scripts with Streamerbot, configure your action commands to call the appropriate Python scripts and read the generated output files to display results in chat or logs.

## Development

Install the development dependencies, then run the tests and checks:

```bash
pip install -r requirements-dev.txt

pytest                 # run the test suite
black .                # format the code
mypy --strict tests    # type-check the tests
```

The tests run each script in a temporary folder with the sample `tests/fixtures/quotes.json`.

[CI](.github/workflows/ci.yml) runs the same checks on every push to `main` and on every pull request.

## License

MIT. See [LICENSE](LICENSE) for details.
