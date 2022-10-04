import configparser
import linecache

path = '/Users/user/Desktop/Backup/'

with open(path + 'new_file.txt',"a+") as f:
    f.write('Abcd')
    f.seek(0)
    f.readable()
    print(f.readline())


config = configparser.ConfigParser()
config.read("config.ini")

api_id = config['Telegram']['last_id']
print(api_id)

config['Telegram']['last_id'] = 'snir oded'
print(config['Telegram']['last_id'])



# file = '/Users/user/Desktop/Backup/first_id.txt'
# f = open('/Users/user/Desktop/Backup/first_id.txt')
# print(f.readline())
#
#
# print(linecache.getline(file,1))