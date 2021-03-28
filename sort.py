from os import times
import re
import pandas as pd
from geopy.geocoders import Nominatim


locator = Nominatim(user_agent="myGeocoder")
columns = ['Nature', 'address', 'description', 'Date', 'occ', 'case status', 'speech text', 'Times', 'Latitude', 'Longitude']
df = pd.DataFrame(columns=columns)
file1 = open('incidents.txt', 'r')
Lines = file1.readlines()

for i in range(0, len(Lines), 5):
    arr = []
    line1 = Lines[i]
    line1 = re.sub('  +', '(', line1)
    line1_s = line1.split('(')
    type = line1_s[0].split("-")[0]
    address = line1_s[0].split("-")[1]

    description = Lines[i+1]

    line3 = Lines[i+2]
    line3 = re.sub('  +', ',', line3)
    line3 = re.sub(': ', ':', line3)
    line3_s = line3.split(",")
    rpt = line3_s[0].split(":")[1]
    occ = line3_s[1].split(":")[1]

    line4 = Lines[i+3]
    line4 = re.sub(': ', ':', line4)
    case_status = line4.split(":")[1]

    # print("Type " + type)
    type = type.strip('\n')
    arr.append(type)

    # print("Address "  + address)
    address = address.strip('\n')
    arr.append(address)

    # print("Description " + description)
    description = re.sub('\s+',' ',description)
    description = description.strip('\n')
    arr.append(description)

    # print("RPT " + rpt)
    date = rpt.strip('\n').split(' ')[1]
    time = rpt.strip('\n').split(' ')[0]
    arr.append(date)

    # print("OCC " + occ)
    occ = occ.strip('\n')
    arr.append(occ)
    # print("Case Status " + case_status)

    case_status = case_status.strip('\n')
    arr.append(case_status)

    speech_text = type + ": " + description + " on " + address + " at " + time + ". Case Status: " + case_status
    arr.append(speech_text)

    day_time = ""
    if 0000 < int(time) < 600:
        day_time = 'Late Night'
    elif 600 <= int(time) < 1200:
        day_time = 'Morning'
    elif 1200 < int(time) < 1800:
        day_time = 'Afternoon'
    else:
        day_time = 'Night'
    arr.append(day_time)

    location = locator.geocode(address + ", Charlottesville,  VA")
    if location is None:
        continue
    latitude = location.latitude
    arr.append(latitude)
    longitude = location.longitude
    arr.append(longitude)

    df.loc[len(df)] = arr


df.to_csv('incidents_final.csv')