import os
import csv

all_files = os.listdir('/Users/user/Downloads/Helium_10_ASIN_Grabber')
csv_files = list(filter(lambda f: f.endswith('.csv'), all_files))
asin_counter = 0
csv_counter = len(csv_files)
print(csv_files)

# lambda returns True if filename (within `all_files`) ends with .csv or else False
# and filter function uses the returned boolean value to filter .csv files from list files.

for csv_file in csv_files:
    file = open('/Users/user/Downloads/Helium_10_ASIN_Grabber/'+csv_file)
    print(csv_file)
    csvreader = csv.reader(file)
    header = next(csvreader)
    #print(header)
    rows = []
    for row in csvreader:
        rows.append(row)
        asin_counter += 1
        print(row[1]+'\tCounter:'+str(asin_counter))
    # print(rows)

    file.close()

print('CSV Files Count is: '+str(csv_counter))