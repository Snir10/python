import csv
from time import sleep
from aliexpress_api import AliexpressApi, models



aliexpress = AliexpressApi('34061046', '3766ae9cf22b81c88134fb56f71eb03c', models.Language.EN, models.Currency.EUR, 'sn2019')


# aliexpress.get_products_details()

products = aliexpress.get_products_details(['1000006468625', 'https://aliexpress.com/item/1005003091506814.html'])

#example from our code
#products = aliexpress.get_products_details(['1000006468625', 'https://he.aliexpress.com/item/1005005008281133.html'])




print(str(products[0])+'\n\n')
print(f'\t\tITEM DETAILS\n\n'
      f'product_id: {products[0].product_id}\n'
      f'product_title: {products[0].product_title[:30]}\n\n'
      
      
      f'original_price: {products[0].original_price}\n'
      f'sale_price: {products[0].sale_price}\n\n'


      f'target_original_price: {products[0].target_original_price}\n'   
      f'target_sale_price: {products[0].target_sale_price} {products[0].target_sale_price_currency}\n'
      f'target_app_sale_price: {products[0].target_app_sale_price} {products[0].target_app_sale_price_currency}\n\n'


      f'discount: {products[0].discount}\n\n'

      
      f'first_level_category_name: {products[0].first_level_category_name}\n'

      

      
      # f'target_sale_price_currency: {products[0].target_sale_price_currency}\n'

      f'product_detail_url: {products[0].product_detail_url}\n'
      f'shop_url: {products[0].shop_url}\n'
      f'product_main_image_url: {products[0].product_main_image_url}\n'
      f'product_small_image_urls: {products[0].product_small_image_urls}\n'
      f'product_detail_url: {products[0].product_detail_url}\n'

      )



