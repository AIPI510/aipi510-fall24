### REQUIREMENTS - PUT IN TEXT BOX OF PR
# $ python -m pip install requests
# https://httpbin.org/#/

# import packages
import requests

website = ""

# GET method - retrieve data
response = requests.get(website)

# send data into url query string
payload = {'key1': 'value1', 'key2': 'value2'}
requests.get(website, params=payload)
print()

# url 
response.url

# Status code
response.status_code

# content in bytes
response.content

# convert to string
response.text

# headers
response.headers

# dictionary
response.json()

# authentication

# cookies