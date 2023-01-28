import regex
import re



myString = "This is a link http://www.google.com $$$"
print(re.search("(?P<url>https?://[^\s]+)", myString).group("url"))