from time import sleep

from instapi import bind
from instapi import User


username = 'superhiddenbrands'
password = 'Alma233490564'

bind(username, password)


# Get user profile by username


#instagram_profile = User.from_username('chen__oded')
instagram_profile = User.from_username('username')


# Like all posts
for feed in instagram_profile.iter_feeds():
  feed.like()
  sleep(5)
  #feed.comment('wow')

