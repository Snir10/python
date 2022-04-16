import csv

#file = open('/Users/user/Downloads/snir-asins-.csv')
file = open('/Users/user/Downloads/Helium_10_ASIN_Grabber_2022-04-16 (15).csv')
csvreader = csv.reader(file)
header = next(csvreader)
print(header)
rows = []
for row in csvreader:
    rows.append(row)
    print(row)
#print(rows)

file.close()