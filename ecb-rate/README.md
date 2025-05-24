# ECB EUR/USD Exchange Rate Fetcher

`ecb_rate.py` is a command-line tool to fetch historical EUR/USD exchange rates from the European Central Bank (ECB)'s Statistical Data Warehouse API.

## Features

- Fetch exchange rate for a specific date.
- Fetch the most recent available rate *before* a specified date using the `-p` or `--previous` flag.
- Skip weekends and look back a configurable number of days for rates.

## Requirements

- Python 3.12 or higher.
- `uv` (for running the script with its dependencies managed by the `/// script` header).
- The script itself specifies its dependencies (`click`, `requests`) in its `/// script` header.

## Installation & Setup

No traditional installation is required if you have `uv` installed. The script is designed to be run directly using `uv`, which will handle the creation of an ephemeral environment with the necessary dependencies.

1.  Ensure you have Python 3.12+ and `uv` installed.
2.  Save the `ecb_rate.py` script to your desired location.
3.  Make the script executable (optional, but good practice):
    ```bash
    chmod +x ecb_rate.py
    ```

## Usage

Run the script from your terminal using `uv run`:

```bash
uv run ecb_rate.py DATE [OPTIONS]
```

**Arguments:**

-   `DATE`: The target date for which to fetch the exchange rate, in `YYYY-MM-DD` format.

**Options:**

-   `-p`, `--previous`: Fetch the most recent available rate *before* the specified `DATE`.
-   `--max-days-back INTEGER`: Maximum number of days to look back when using `--previous` (default: 10).
-   `--help`: Show the help message and exit.

**Examples:**

1.  Fetch the rate for a specific date:
    ```bash
    uv run ecb_rate.py 2025-04-29
    ```
    Output:
    ```
    Fetching EURUSD rate for 2025-04-29...
    EURUSD rate for 2025-04-29: <rate_value>
    ```

2.  Fetch the rate for the day *before* a specific date (e.g., if 2025-05-01 is a holiday, it might fetch for 2025-04-30):
    ```bash
    uv run ecb_rate.py 2025-05-01 -p
    ```
    Output:
    ```
    Looking for rate prior to 2025-05-01 (up to 10 days back)...
    EURUSD rate for 2025-04-30 (1 day before 2025-05-01): <rate_value>
    ```

3.  Fetch the rate prior to a weekend date (e.g., Saturday 2025-05-03), which should give Friday's rate (2025-05-02):
    ```bash
    uv run ecb_rate.py 2025-05-03 --previous
    ```
    Output:
    ```
    Looking for rate prior to 2025-05-03 (up to 10 days back)...
    EURUSD rate for 2025-05-02 (1 day before 2025-05-03): <rate_value>
    ```

4.  If no rate is found for a specific date (and `-p` is not used):
    ```bash
    uv run ecb_rate.py 2025-01-01 # Assuming 2025-01-01 is a holiday with no rate
    ```
    Output:
    ```
    Fetching EURUSD rate for 2025-01-01...
    No rate available for 2025-01-01. Use --previous/-p to get the most recent available rate.
    ```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
