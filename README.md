# streamerbot-quotebot

An alternative quote system for **Streamerbot** with expanded functionality. This is a Python-based quote management system designed to integrate with Streamerbot for managing memorable moments and quotes from your stream.

## Features

- **Add quotes** with associated metadata (user, game, timestamp)
- **Retrieve quotes** by ID or get a random quote
- **Search quotes** by various criteria
- **Delete quotes** with automatic ID optimization
- **Quote facts** tracking and statistics
- **Timezone support** with automatic timestamp conversion
- **JSON-based storage** for easy backup and integration
- **Customizable username** for colloquial references in outputs

## Installation

### Prerequisites

- Python 3.7+
- Streamerbot installation (for integration)

### Setup

1. Clone or download this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Copy and configure the config file:
   ```bash
   cp config.example.yaml config.yaml
   ```
4. Edit `config.yaml` with your settings (see [Configuration](#configuration) below)

## Configuration

Create a `config.yaml` file in the project root with the following settings:

```yaml
# Your username (or colloquial version used on stream)
# Used in quote fact outputs
colloquial_username: Capn

# Valid timezone from pytz
# See: https://gist.github.com/heyalexej/8bf688fd67d7199be4a1682b3eec7568
timezone: America/Chicago
```

If `config.yaml` is not found, defaults will be used:
- `colloquial_username`: "streamer"
- `timezone`: "UTC"

## Usage

### Commands

#### Add a Quote
```bash
python quote-add.py <user_id> <username> <game_id> <game_name> "<quote_text>"
```
Adds a new quote with timestamp and associated metadata.

#### Get a Quote
```bash
python quote-get.py [quote_id]
```
- `quote-get.py` - Returns a random quote
- `quote-get.py 5` - Returns quote with ID 5

#### Latest Quote
```bash
python quote-latest.py
```
Retrieves the most recently added quote.

#### Search Quotes
```bash
python quote-search.py <search_term>
```
Searches quotes by content, user, or game.

#### Delete a Quote
```bash
python quote-delete.py <quote_id>
```
Removes a quote by ID and optimizes remaining IDs.

#### Quote Facts
```bash
python quote-facts.py
```
Displays statistics and facts about your quotes.

## File Structure

```
streamerbot-quotebot/
├── quote-add.py              # Add new quotes
├── quote-delete.py           # Delete quotes
├── quote-facts.py            # View quote statistics
├── quote-get.py              # Retrieve quotes
├── quote-latest.py           # Get most recent quote
├── quote-search.py           # Search quotes
├── constants.py              # Configuration and constants
├── utils.py                  # Shared utilities
├── config.example.yaml       # Configuration template
├── requirements.txt          # Python dependencies
├── quotes.json              # Quote database (auto-created)
└── README.md                # This file
```

### Output Files

The scripts generate output files for Streamerbot integration:
- `quote.txt` - Quote output
- `latest_quote.txt` - Latest quote
- `quote_add_output.txt` - Add operation result
- `quote_delete_result.txt` - Delete operation result
- `quote_fact.txt` - Quote facts
- `quote_output.txt` - General quote output

## Dependencies

- **pytz** - Timezone handling
- **pyyaml** - Configuration file parsing

See `requirements.txt` for version details.

## Integration with Streamerbot

To use these scripts with Streamerbot, configure your action commands to call the appropriate Python scripts and read the generated output files to display results in chat or logs.

## License

See LICENSE file for details.
