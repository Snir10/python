import urllib

import requests

key = '02b01b13c04d19c7906be88ad387bf8fee96c'

url = urllib.parse.quote('https://mail.google.com/mail/u/0/#inbox')
name = '[wewedwececcbbc1241]'
r = requests.get('http://cutt.ly/api/api.php?key={}&short={}&name={}'.format(key, url, name))
print(r.text)