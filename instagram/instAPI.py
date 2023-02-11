from instapi import Client

username = 'superhiddenbrands'
password = 'Alma233490564'


bot = Client(username=username, password=password)
bot.login()

albumPath = ['/Users/user/Desktop/Backup_2/Item_482549/482541.png', '/Users/user/Desktop/Backup_2/Item_482549/482542.png', '/Users/user/Desktop/Backup_2/Item_482549/482543.png']

text = 'multiple photo test'
bot.post_album(medias=albumPath, caption=text)
