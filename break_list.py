import argparse
import pandas as pd


def load_runsheet(path: str) -> pd.DataFrame:
    """Load runsheet CSV or Excel file.

    The file must contain 'Name', 'Station', and 'Start' columns with start
    times in HH:MM format.
    """
    if path.lower().endswith(('.xls', '.xlsx')):
        df = pd.read_excel(path)
    else:
        df = pd.read_csv(path)
    required = {'Name', 'Station', 'Start'}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(
            f"Runsheet missing required columns: {', '.join(sorted(missing))}"
        )
    # Normalise column types
    df['Start'] = pd.to_datetime(df['Start'], format='%H:%M')
    return df[['Name', 'Station', 'Start']]


def generate_break_schedule(df: pd.DataFrame, breaks: int = 0,
                             interval_minutes: int = 120) -> pd.DataFrame:
    """Generate a break schedule for each team member.

    Break times are computed at `interval_minutes` intervals after the start
    time. With ``breaks=0`` only the sorted list of team members is produced.
    """
    df = df.copy()
    df.sort_values('Start', inplace=True)
    for i in range(1, breaks + 1):
        df[f'Break{i}'] = df['Start'] + pd.to_timedelta(interval_minutes * i, unit='m')
    # Format time columns
    time_cols = ['Start'] + [f'Break{i}' for i in range(1, breaks + 1)]
    for col in time_cols:
        df[col] = df[col].dt.strftime('%H:%M')
    return df


def main(argv=None):
    parser = argparse.ArgumentParser(description='Generate break list from runsheet')
    parser.add_argument(
        'input',
        help='Input runsheet file (CSV or Excel with Name, Station, and Start columns)'
    )
    parser.add_argument('-o', '--output', default='break_list.csv', help='Output CSV file')
    parser.add_argument('-b', '--breaks', type=int, default=0,
                        help='Number of breaks to schedule (default: 0)')
    parser.add_argument('-i', '--interval', type=int, default=120,
                        help='Minutes between breaks (default: 120)')
    args = parser.parse_args(argv)

    df = load_runsheet(args.input)
    schedule = generate_break_schedule(df, breaks=args.breaks, interval_minutes=args.interval)
    schedule.to_csv(args.output, index=False)
    print(f"Break list written to {args.output}")


if __name__ == '__main__':
    main()
