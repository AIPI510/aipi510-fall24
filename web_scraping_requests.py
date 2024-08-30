### REQUIREMENTS - PUT IN TEXT BOX OF PR
# $ python -m pip install requests
# https://httpbin.org/#/

# import packages
import requests

website = ""

# GET method - retrieve data
data = requests.get(website)

# url 
data.url

# Status code
data.status_code

# content in bytes
data.content

# convert to string
data.text

# headers
data.headers

# dictionary
data.json()

# authentication