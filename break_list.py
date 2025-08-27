import argparse
import pandas as pd


def load_runsheet(path: str) -> pd.DataFrame:
    """Load runsheet CSV or Excel file.

    The file must contain at least a 'Name' column and a 'Start' column with
    times in HH:MM format.
    """
    if path.lower().endswith(('.xls', '.xlsx')):
        df = pd.read_excel(path)
    else:
        df = pd.read_csv(path)
    if 'Start' not in df.columns or 'Name' not in df.columns:
        raise ValueError("Runsheet must contain 'Name' and 'Start' columns")
    # Normalise column types
    df['Start'] = pd.to_datetime(df['Start'], format='%H:%M')
    return df[['Name', 'Start']]


def generate_break_schedule(df: pd.DataFrame, breaks: int = 4,
                             interval_minutes: int = 120) -> pd.DataFrame:
    """Generate a break schedule for each team member.

    Break times are computed at `interval_minutes` intervals after the start
    time. By default, four breaks every two hours are scheduled.
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
    parser.add_argument('input', help='Input runsheet file (CSV or Excel with Name and Start columns)')
    parser.add_argument('-o', '--output', default='break_list.csv', help='Output CSV file')
    parser.add_argument('-b', '--breaks', type=int, default=4, help='Number of breaks to schedule')
    parser.add_argument('-i', '--interval', type=int, default=120,
                        help='Minutes between breaks (default: 120)')
    args = parser.parse_args(argv)

    df = load_runsheet(args.input)
    schedule = generate_break_schedule(df, breaks=args.breaks, interval_minutes=args.interval)
    schedule.to_csv(args.output, index=False)
    print(f"Break list written to {args.output}")


if __name__ == '__main__':
    main()
