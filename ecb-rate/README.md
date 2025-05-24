# ECB EUR/USD Exchange Rate Fetcher

`ecb_rate.py` is a command-line tool to fetch historical EUR/USD exchange rates from the European Central Bank (ECB)'s Statistical Data Warehouse API.

---

## Quick Start Options

You can use this project in two ways:

### 1. Full Development & Testing (Recommended)

This approach uses a Python virtual environment and requirements.txt for a robust, reproducible workflow. It is ideal if you want to run tests or develop further.

#### **Setup**

```bash
# Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### **Run the Script**

```bash
python ecb_rate.py DATE [OPTIONS]
```

#### **Run the Tests**

```bash
pytest -v
```

#### **Deactivate when done**

```bash
deactivate
```

---

### 2. Quick Script Run with uv (No Setup)

If you only want to run the script and have `uv` installed, you can run it directly—`uv` will handle dependencies automatically:

```bash
uv run ecb_rate.py DATE [OPTIONS]
```

---

## Usage

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
    # or, if using venv:
    python ecb_rate.py 2025-04-29
    ```
    Output:
    ```
    Fetching EURUSD rate for 2025-04-29...
    EURUSD rate for 2025-04-29: <rate_value>
    ```

2.  Fetch the rate for the day *before* a specific date (e.g., if 2025-05-01 is a holiday, it might fetch for 2025-04-30):
    ```bash
    uv run ecb_rate.py 2025-05-01 -p
    # or
    python ecb_rate.py 2025-05-01 -p
    ```
    Output:
    ```
    Looking for rate prior to 2025-05-01 (up to 10 days back)...
    EURUSD rate for 2025-04-30 (1 day before 2025-05-01): <rate_value>
    ```

3.  If no rate is found for a specific date (and `-p` is not used):
    ```bash
    uv run ecb_rate.py 2025-01-01
    # or
    python ecb_rate.py 2025-01-01
    ```
    Output:
    ```
    Fetching EURUSD rate for 2025-01-01...
    No rate available for 2025-01-01. Use --previous/-p to get the most recent available rate.
    ```

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.