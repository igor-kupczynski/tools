# ECB EUR/*X* Exchange Rate Fetcher

`ecb_rate.py` is a command-line tool to fetch historical EUR/*X* exchange rates (e.g. EUR/USD, EUR/PLN, etc.) from the European Central Bank (ECB)'s Statistical Data Warehouse API.

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

1. **Fetch EUR/USD rate for a specific date:**
   ```bash
   uv run ecb_rate.py 2025-04-29
   ```
   Output:
   ```
   Fetching EURUSD rate for 2025-04-29...
   EURUSD rate for 2025-04-29: 1.1373
   ```

2. **Fetch EUR/PLN rate for a specific date:**
   ```bash
   uv run ecb_rate.py 2024-12-27 --currency PLN
   ```
   Output:
   ```
   Fetching EURPLN rate for 2024-12-27...
   EURPLN rate for 2024-12-27: 4.2753
   ```

3. **Fetch the most recent rate before a date** (useful for holidays/weekends):
   ```bash
   uv run ecb_rate.py 2025-05-01 -p -c PLN
   ```
   Output:
   ```
   Looking for rate prior to 2025-05-01 (up to 10 days back) for EURPLN...
   EURPLN rate for 2024-12-31 (1 day before 2025-01-01): 4.2750
   ```

4. **Weekend example** (Saturday, gets Friday's rate):
   ```bash
   uv run ecb_rate.py 2025-05-03 --previous --currency USD
   ```
   Output:
   ```
   Looking for rate prior to 2025-05-03 (up to 10 days back) for EURUSD...
   EURUSD rate for 2025-05-02 (1 day before 2025-05-03): 1.1343
   ```

## Command Options

```
Usage: ecb_rate.py [OPTIONS] DATE

  Fetch ECB EUR<X> exchange rate for a given date (default: EURUSD).

  DATE should be in YYYY-MM-DD format.

Options:
  -c, --currency TEXT       Target currency code (e.g., PLN, USD, GBP). Default: USD
  -p, --previous           Fetch the most recent available rate *before* the
                            specified DATE.
  --max-days-back INTEGER   Maximum number of days to look back when using
                            --previous (default: 10)
  --help                    Show this message and exit.
```

## Multi-Currency Support

You can fetch rates for any currency supported by the ECB by specifying the `--currency` or `-c` option. For example:

- EUR/USD (default): `uv run ecb_rate.py 2025-04-29`
- EUR/PLN: `uv run ecb_rate.py 2024-12-27 --currency PLN`
- EUR/GBP: `uv run ecb_rate.py 2025-04-29 -c GBP`

If a rate is not available for a given date (e.g. weekends, holidays, or missing data), the tool will report this and you can use `--previous` to get the most recent available rate.

## Testing

To run the tests:

```bash
pytest -v
```

The test suite covers both EURUSD and EURPLN pairs, including edge cases for missing data and previous rate lookup.

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