# Calendar Generator
A Python script that converts schedule data from csv to ics calendar file.

**Author**: c4ssiopeia 
Contact me by: mailto:feedback+github@cypeia.de

## Features
- Converts CSV/Excel schedule data to ICS format
- Handles timezone conversion -> just change `berlin` to any timezone you prefer
- Fills out empty time slots depending on whether it's a weekday or weekend.

## Requirements 
```bash
pip install -r requirements
```

## Usage
Prepare your schedule data with columns, use the `example.xlsx` file.
- `Date`: Date of the event (use the date format in excel)
- `Start`: Start time - example `17:00:00` (optional)
- `End`: End time (optional)
- `Type`: Event type/name
- `Description`: Event description (optional)

Save the excel file as `input.csv`.
The `input.csv` has to be separated by comma!

Run the script:
`python3 generate_ics.py`