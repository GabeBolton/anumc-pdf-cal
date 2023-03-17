from tabula import read_pdf
from ics import Calendar, Event
import re
import pandas as pd
df = read_pdf("2023 Yearly Booking Schedule - ANU Mountaineering Club.pdf", pages="all")

df = pd.concat(df)
df = df[(df['Date'] != 'TOTAL:')] # remove the final total hours entry

df['Start Time'] = pd.to_datetime(df['Date'].str.lstrip('MoWeFr ') + ' ' + df['From Time'], dayfirst=True)
df['Start Time'] = df['Start Time'].dt.tz_localize('Australia/ACT')
df['End Time'] = pd.to_datetime(df['Date'].str.lstrip('MoWeFr ') + ' ' + df['To Time'], dayfirst=True)
df['End Time'] = df['End Time'].dt.tz_localize('Australia/ACT')

c = Calendar()

for index, row in df.iterrows():
    e = Event()
    e.name = row['Facility Name'].removeprefix('Badminton\r')
    e.begin = row['Start Time']
    e.end = row['End Time']
    c.events.add(e)
    c.events

with open('anumc-wall-booking.ics', 'w') as my_file:
    my_file.writelines(c.serialize_iter())

pass