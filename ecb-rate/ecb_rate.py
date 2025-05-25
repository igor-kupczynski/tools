# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "click",
#     "requests",
# ]
# ///

import click
import requests
import json
from datetime import datetime, timedelta
from typing import Optional

def fetch_ecb_rate(date: str, target_currency: str = "USD") -> Optional[float]:
    """Fetch ECB EUR<target_currency> rate for a specific date using ECB's Statistical Data Warehouse API."""
    # ECB API endpoint for daily <target_currency>/EUR exchange rates
    # Example: https://sdw-wsrest.ecb.europa.eu/service/data/EXR/D.PLN.EUR.SP00.A
    url = f"https://sdw-wsrest.ecb.europa.eu/service/data/EXR/D.{target_currency}.EUR.SP00.A"

    params = {
        'startPeriod': date,
        'endPeriod': date,
        'format': 'jsondata'
    }

    try:
        response = requests.get(url, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()

        # Navigate through the ECB JSON structure to extract the rate
        if (
            'dataSets' in data and
            len(data['dataSets']) > 0 and
            'series' in data['dataSets'][0]
        ):
            dataset = data['dataSets'][0]
            series = dataset['series']
            for series_key, series_data in series.items():
                if 'observations' in series_data and series_data['observations']:
                    for obs_key, obs_data in series_data['observations'].items():
                        if obs_data and obs_data[0] is not None:
                            return float(obs_data[0])
        return None
    except (requests.RequestException, json.JSONDecodeError, KeyError, ValueError, IndexError):
        return None

def find_previous_rate(target_date: datetime, max_days_back: int = 10, target_currency: str = "USD") -> tuple[Optional[float], Optional[str]]:
    """Find the most recent available rate before the target date for a given currency."""
    current_date = target_date - timedelta(days=1)  # Start from the day before

    for _ in range(max_days_back):
        # Skip weekends (Saturday=5, Sunday=6)
        if current_date.weekday() < 5:  # Monday=0 to Friday=4
            date_str = current_date.strftime('%Y-%m-%d')
            rate = fetch_ecb_rate(date_str, target_currency=target_currency)
            if rate is not None:
                return rate, date_str
        current_date -= timedelta(days=1)
    return None, None

@click.command()
@click.argument('date_str_arg', type=str, metavar='DATE')
@click.option('--currency', '-c', type=str, default='USD', show_default=True, help='Target currency code (e.g., PLN, USD, GBP)')
@click.option('--previous', '-p', is_flag=True, 
              help='Fetch the most recent available rate *before* the specified DATE.')
@click.option('--max-days-back', default=10, 
              help='Maximum number of days to look back when using --previous (default: 10)')
def main(date_str_arg: str, currency: str, previous: bool, max_days_back: int):
    """Fetch ECB EUR<currency> exchange rate for a given date.
    
    DATE should be in YYYY-MM-DD format.

    If -p/--previous is used, it fetches the rate for the day *before* DATE.
    
    Examples:
        python ecb_rate.py 2025-04-29 --currency PLN
        python ecb_rate.py 2025-05-01 --previous --currency PLN
        python ecb_rate.py 2025-05-03 -p -c PLN
    """
    try:
        initial_target_date_obj = datetime.strptime(date_str_arg, '%Y-%m-%d')
    except ValueError:
        click.echo(f"Error: Invalid date format '{date_str_arg}'. Please use YYYY-MM-DD format.", err=True)
        return 1
    
    if initial_target_date_obj.date() > datetime.now().date():
        click.echo(f"Error: Cannot fetch rates for future date '{date_str_arg}'.", err=True)
        return 1

    if previous:
        click.echo(f"Looking for rate prior to {date_str_arg} (up to {max_days_back} days back) for EUR{currency}...")
        prev_rate, prev_date_found_str = find_previous_rate(initial_target_date_obj, max_days_back, target_currency=currency)
        
        if prev_rate is not None:
            days_diff = (initial_target_date_obj - datetime.strptime(prev_date_found_str, '%Y-%m-%d')).days
            click.echo(f"EUR{currency} rate for {prev_date_found_str} ({days_diff} day{'s' if days_diff != 1 else ''} before {date_str_arg}): {prev_rate:.4f}")
            return 0
        else:
            click.echo(f"No EUR{currency} rate found within {max_days_back} days before {date_str_arg}", err=True)
            return 1
    else: # Not using --previous flag
        click.echo(f"Fetching EUR{currency} rate for {date_str_arg}...")
        rate = fetch_ecb_rate(date_str_arg, target_currency=currency)
        
        if rate is not None:
            click.echo(f"EUR{currency} rate for {date_str_arg}: {rate:.4f}")
            return 0
        else:
            click.echo(f"No EUR{currency} rate available for {date_str_arg}. Use --previous/-p to get the most recent available rate.", err=True)
            return 1

if __name__ == '__main__':
    exit(main())