import csv


def csv_check_id_exists(id):
    with open('/Users/user/Desktop/Backup_1/products.csv') as csv_file:
        for line in csv.DictReader(csv_file):
            if line is not None and line['id'] == id:
                return 'ID founded! -> '+id





# num = input('Input an ID Number: ')
num = '4232894'
print(csv_check_id_exists(num))


