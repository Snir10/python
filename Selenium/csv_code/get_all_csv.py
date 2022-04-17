import os
import csv


def get_csv_files(dir):
    csv_counter = 0
    all_files = os.listdir(dir)
    csv_files = list(filter(lambda f: f.endswith('.csv'), all_files))

    # lambda returns True if filename (within `all_files`) ends with .csv or else False
    # and filter function uses the returned boolean value to filter .csv files from list files.

    csv_counter = len(csv_files)
    print(csv_files)
    return csv_files
def print_csv_content(csv_files):
    counter = 0
    for csv_file in csv_files:
        file = open('/Users/user/Downloads/Helium_10_ASIN_Grabber/' + csv_file)
        print(csv_file)
        csvreader = csv.reader(file)
        header = next(csvreader)
        # print(header)
        rows = []
        for row in csvreader:
            counter += 1
            rows.append(row)
            print(str(counter)+')'  + '\t'
                  + 'ASIN: ' + row[1] + '\t'
                  + 'price: '+row[3] + '\t\t\t'
                  + 'rev_count: ' + row[4] + '\t\t\t'
                  + 'rev_rate: '+ row[5]+ '\t'
                  + row[2]+ '\t'
                  + row[0])
        print('--> This Script has printed: '+str(counter)+' Products')

        file.close()
def create_csv_file(csv_files, head):
    with open('asins.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)

        # write the header
        writer.writerow(head)
        for csv_file in csv_files:
            # write multiple rows
            file = open('/Users/user/Downloads/Helium_10_ASIN_Grabber/' + csv_file)
            print(csv_file)
            csvreader = csv.reader(file)
            header = next(csvreader)
            rows = []
            for row in csvreader:
                writer.writerow(row)

            file.close()



            writer.writerows(csv_file)

asin_counter = 0
src_dir = '/Users/user/Downloads/Helium_10_ASIN_Grabber'
header = ['Product Name', 'ASIN', 'Brand', 'Price', 'Reviews Count', 'Reviews Rate', 'BSR']

csv_files = get_csv_files(src_dir)
print_csv_content(csv_files)
create_csv_file(csv_files, header)
