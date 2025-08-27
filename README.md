# Breaker-List

This repository provides a simple script to create a break roster from a daily
runsheet for the Private Gaming Rooms F&B department.

## Usage

1. Prepare a runsheet CSV or Excel file with the following columns:
   - `Name`: team member's name.
   - `Station`: where the team member is assigned.
   - `Start`: shift start time in `HH:MM` format.

2. Run the script to generate a sorted list (no breaks by default):

```bash
python break_list.py runsheet.csv -o break_list.csv
```

Use the `-b` option to include break columns. For example, to schedule four
breaks two hours apart:

```bash
python break_list.py runsheet.csv -b 4 -o break_list.csv
```

You can adjust the interval between breaks with the `-i` option (minutes).

An example input file `runsheet_example.csv` and the generated output
`break_list_example.csv` are included.
