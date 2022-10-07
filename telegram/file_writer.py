import configparser
import linecache

path = '/Users/user/Desktop/Backup/'

with open(path + 'new_file.txt',"a+") as f:
    f.write('Abcd')
    f.close()


with open(path + 'new_file.txt',"a+") as f:
    f.seek(0)
    print(f.readline())
    f.close()







