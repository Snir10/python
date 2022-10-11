import csv
from time import sleep
from aliexpress_api import AliexpressApi, models



aliexpress = AliexpressApi('34061046', '3766ae9cf22b81c88134fb56f71eb03c', models.Language.EN, models.Currency.EUR, 'sn2019')

with open("/Users/user/Desktop/Backup/products.csv", 'r') as file:
  csvreader = csv.reader(file)

  list_iterator = iter(csvreader)
  next(list_iterator)

  for row in csvreader:
    link = row[4]
    print('aliexpress src link\t'+link + '\tis going to be converted')

    affiliate_links = aliexpress.get_affiliate_links(link)
    sleep(1)
    try:
        print(affiliate_links[0].promotion_link)

    except:
        print('no aff link detected')


# aliexpress.get_products_details()

products = aliexpress.get_products_details(['1000006468625', 'https://aliexpress.com/item/1005003091506814.html'])
print(products[0].product_title, products[1].target_sale_price)



