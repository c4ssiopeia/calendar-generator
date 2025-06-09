#!/usr/bin/env python3

import pandas as pd
import pytz
from ics import Calendar, Event
from datetime import datetime  
from zoneinfo import ZoneInfo

# input
input_file = 'input.csv'

# define formating columns
date_column = 'Date'
string_columns = ['Type','Description']
timedelta_columns = ['Start','End']
start_time = ['07:00:00','17:30:00']
end_time = ['15:00:00','22:00:00']

# set timezone
berlin = 'Europe/Berlin'

# definition of functions
def import_csv():
    # Read the file
    df = pd.read_csv(input_file)

    # delete all rows that are completely full with NaN
    df = df.dropna(how="all")

    # format the columns
    df[date_column] = pd.to_datetime(df[date_column], dayfirst=True)
    for col in string_columns:
         df[col] = df[col].astype(pd.StringDtype())
    for col in timedelta_columns:
        df[col] = pd.to_timedelta(df[col], unit="h")

    return df

def return_hour_depending_on_weekday(df,counter,row,start_end):
    # insert 0 for start and 1 for end
    row_hour = df[timedelta_columns[start_end]][counter]
    # check if it's the start or the end time
    if start_end == 0:
        time = start_time
    elif start_end == 1:
        time = end_time
    # if the row is True, and the hour is NaN, then set the time accordingly for weekdays
    if row == True and pd.isna(row_hour):
        row_hour = time[1]
    elif row == False and pd.isna(row_hour):
        row_hour = time[0]
    df.loc[counter, timedelta_columns[start_end]] = row_hour

def fillout_empty_timeslots():
    df = import_csv()
    # append a column only for verifying if it's a weekday or weekend day -> weekday = True 
    weekdays = []
    for row in df[date_column]:
        if row.dayofweek < 5:
            weekdays.append(True)
        else:
            weekdays.append(False)
    df["weekday"] = weekdays
    # go throw every row and fill the hours if none where there before
    counter = 0
    for row in df["weekday"]:
        return_hour_depending_on_weekday(df,counter,row,0)
        return_hour_depending_on_weekday(df,counter,row,1)
        counter += 1
    return df

def adding_correct_timezone(time):
    dt = str(time)
    dt_iso = datetime.fromisoformat(dt) # make datetime aware
    output_time = dt_iso.astimezone(ZoneInfo(berlin))
    return output_time

def make_calendar():
    calendar = Calendar()
    df = fillout_empty_timeslots()
    for index,row in df.iterrows():
        new_start = adding_correct_timezone(row['Date'] + row['Start'])
        new_end = adding_correct_timezone(row['Date'] + row['End'])

        event = Event()
        event.name = row['Type']
        event.begin = new_start
        event.end = new_end
        
        if pd.notna(row['Description']):
            event.description = row['Description'] 

        calendar.events.add(event)        
    with open('thw_calender.ics','w') as ics_file:
        ics_file.writelines(calendar.serialize_iter())

# execution
if __name__ == "__main__":
    make_calendar()

