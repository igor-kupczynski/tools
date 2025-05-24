# ECB EUR/USD Exchange Rate Fetcher

`ecb_rate.py` is a command-line tool to fetch historical EUR/USD exchange rates from the European Central Bank (ECB)'s Statistical Data Warehouse API.

## Quick Start

### Run Directly with `uv` (Recommended for Users)

The easiest way to use this tool is with `uv`, which handles dependencies automatically. You can even run it directly from GitHub without downloading anything:

```bash
# Run directly from GitHub
uv run https://raw.githubusercontent.com/igor-kupczynski/tools/main/ecb-rate/ecb_rate.py 2025-04-29

# Or if you've downloaded the script
uv run ecb_rate.py 2025-04-29
```

### Usage Examples

1. **Fetch rate for a specific date:**
   ```bash
   uv run ecb_rate.py 2025-04-29
   ```
   Output:
   ```
   Fetching EURUSD rate for 2025-04-29...
   EURUSD rate for 2025-04-29: 1.1373
   ```

2. **Fetch the most recent rate before a date** (useful for holidays/weekends):
   ```bash
   uv run ecb_rate.py 2025-05-01 -p
   ```
   Output:
   ```
   Looking for rate prior to 2025-05-01 (up to 10 days back)...
   EURUSD rate for 2025-04-30 (1 day before 2025-05-01): 1.1373
   ```

3. **Weekend example** (Saturday, gets Friday's rate):
   ```bash
   uv run ecb_rate.py 2025-05-03 --previous
   ```
   Output:
   ```
   Looking for rate prior to 2025-05-03 (up to 10 days back)...
   EURUSD rate for 2025-05-02 (1 day before 2025-05-03): 1.1343
   ```

## Command Options

```
Usage: ecb_rate.py [OPTIONS] DATE

  Fetch ECB EURUSD exchange rate for a given date.

  DATE should be in YYYY-MM-DD format.

Options:
  -p, --previous            Fetch the most recent available rate *before* the
                            specified DATE.
  --max-days-back INTEGER   Maximum number of days to look back when using
                            --previous (default: 10)
  --help                    Show this message and exit.
```

## For Contributors & Testers

If you want to contribute to the project or run the integration tests, use a Python virtual environment:

```bash
# Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the tests
pytest -v

# Deactivate when done
deactivate
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.