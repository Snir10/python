
import requests



API_key = ''



params = {
    'access_key': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiI0IiwianRpIjoiOWI1Y2Q1ZDNlMWQ5Yjk5ZjNmYTA0MTMwNzE5M2M1MGU5MjJiMjExYWJhNTFlNGQwNWY4YmZkNWYwMmY0MjU5Y2IxNzcwY2VlM2Q3ODQyOWEiLCJpYXQiOjE2Nzc0Mzk5NzcsIm5iZiI6MTY3NzQzOTk3NywiZXhwIjoxNzA4OTc1OTc3LCJzdWIiOiIyMDI2NiIsInNjb3BlcyI6W119.nHym7Y1oO6R4E2mfh7yaSWTm8jryB8WKQy8lY2Zdq7886lbqQnGVRlkp8P-vN5xZ3kBQNoK_FIj8jF5Q87bgOg'
}

# api_result = requests.get('https://app.goflightlabs.com/flights', params)




api_result

api_response = api_result.json()



print(api_response)
