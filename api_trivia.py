import requests
import pandas as pd

response = requests.get("https://opentdb.com/api.php?amount=10")
print(response.json())