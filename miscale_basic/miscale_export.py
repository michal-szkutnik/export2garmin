#!/usr/bin/python3

import os
import csv
from datetime import datetime as dt, date
from garminconnect import Garmin

# Version info
print("""
===============================================
Export 2 Garmin Connect v2.0 (miscale_export.py
===============================================
""")

class User():
    def __init__(self, sex, height, birthdate, email, max_weight, min_weight):
        self.sex = sex
        self.height = height
        self.birthdate = birthdate
        self.email = email
        self.max_weight = max_weight
        self.min_weight = min_weight

    # Calculating age
    @property
    def age(self):
        today = date.today()
        calc_date = dt.strptime(self.birthdate, "%d-%m-%Y")
        return today.year - calc_date.year

# Importing user variables from a file
path = os.path.dirname(os.path.dirname(__file__))
users = []
with open(path + '/user/export2garmin.cfg', 'r') as file:
    for line in file:
        line = line.strip()
        if line.startswith('miscale_basic_export_'):
            user_data = eval(line.split('=')[1].strip())
            users.append(User(*user_data))

# Import data variables from a file
with open(path + '/user/miscale_basic_backup.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=';')
    for row in csv_reader:
        if str(row[0]) in ["failed", "to_import"]:
            mitdatetime = int(row[1])
            weight = float(row[2])
            # miimpedance = float(row[3])
            break

# Matching Garmin Connect account to weight
selected_user = None
for user in users:
    if user.min_weight <= weight <= user.max_weight:
        selected_user = user
        break

# Calcuating body metrics
if selected_user is not None and 'email@email.com' not in selected_user.email:
    # Print to temp.log file
    formatted_time = dt.fromtimestamp(mitdatetime).strftime("%d.%m.%Y;%H:%M")
    print(f"MISCALE_BASIC * Import data: {mitdatetime};{weight:.1f}")
    print(f"MISCALE_BASIC * Calculated data: {formatted_time};{weight:.1f};{selected_user.email};{dt.now().strftime('%d.%m.%Y;%H:%M')}")

    # Login to Garmin Connect
    with open(path + '/user/' + selected_user.email, 'r') as token_file:
        tokenstore = token_file.read()
        garmin = Garmin()
        garmin.login(tokenstore)

        # Upload data to Garmin Connect
        # garmin.add_body_composition(dt.fromtimestamp(mitdatetime).isoformat(),weight=weight)
        print("MISCALE_BASIC * Upload status: OK")
else:

    # Print to temp.log file
    print(f"MISCALE_BASIC * Import data: {mitdatetime};{weight:.1f}")
    print("MISCALE_BASIC * There is no user with given weight or undefined user email@email.com, check users section in export2garmin.cfg")