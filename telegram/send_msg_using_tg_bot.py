import requests

def send_message(text):
    token = '5536338381:AAGn8sPu__OmyDW3RLusbDc8BYTP0ybh7tg'
    chat_id = '-1001677673014'
    utl_req = 'https://api.telegram.org/bot' + token + '/sendMessage'+'?chat_id=' + chat_id + '&text='+text
    result = requests.get(utl_req)
    print(result.text)


send_message('chen')

