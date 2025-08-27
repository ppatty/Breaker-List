# Breaker-List

This repository provides a simple script to create a break roster from a daily
runsheet for the Private Gaming Rooms F&B department.

## Usage

1. Prepare a runsheet CSV or Excel file with at least the following columns:
   - `Name`: team member's name.
   - `Start`: shift start time in `HH:MM` format.

2. Run the script to generate a break list:

```bash
python break_list.py runsheet.csv -o break_list.csv
```

By default, the script schedules four breaks per team member at 120‑minute
intervals. Use `-b` and `-i` options to adjust the number of breaks and the
interval in minutes.

An example input file `runsheet_example.csv` and the generated output
`break_list_example.csv` are included.
