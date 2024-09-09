
## Pre-Requisite: 
"""
The requirements.txt file from the original repository pretty much contains all the required libraries, 
but optionally you can run this command to install all the required libraries if you run into dependency errors:

`pip install beautifulsoup4 pandas numpy requests`

We are using the version : 
-> numpy==2.1.0
-> pandas==2.2.2
-> requests==2.32.3
-> beautifulsoup4==4.12.3

"""


## Importing the necessary libraries:
import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np



# List of URLs to scrape faculty information from
url_list = [
    "https://cs.duke.edu/people/appointed-faculty/primary-faculty",
    "https://cs.duke.edu/people/appointed-faculty/secondary-faculty", 
    "https://cs.duke.edu/people/other-faculty/adjunct-and-visiting-faculty",
    "https://cs.duke.edu/people/other-faculty/emeriti",
    "https://cs.duke.edu/people/postdoctoral-fellows",
    "https://cs.duke.edu/people/staff"
]

# Creating a folder to save the HTML files
html_folder = 'html_files'
os.makedirs(html_folder, exist_ok=True)

# adding a list to store all faculty data
all_data = []

# Downloading HTML content from each URL and save it as a HTML file
for url in url_list:
    file_name = os.path.join(html_folder, url.split('/')[-2] + '.html')  # Saving the files 
    response = requests.get(url)
    
    with open(file_name, 'w') as file:
        file.write(response.text)
    
    # Parsing the saved HTML file and extracting faculty data
    data = []
    with open(file_name, 'r', encoding='utf-8') as f:  # Opening the file in read mode
        soup = BeautifulSoup(f, 'html.parser')
    
    faculty_list = soup.find_all('li', class_='grid list-group-item')
    
    for faculty in faculty_list:
        name = np.nan  # Setting a default value as NAN
        name_tag = faculty.find('div', class_='h4', role='heading')
        if name_tag:
            name = name_tag.get_text(strip=True)  # The faculty name is usually enclosed in the "h4" tag
        
        designation = np.nan  # Setting a default value
        for tag in faculty.find_all('div', class_='h6'):  # Designation is usually enclosed in a "h6" tag
            text = tag.get_text(strip=True)
            if text:
                designation = text
                
        
        email_tag = faculty.find('a', href=lambda href: href and 'mailto:' in href)  # Emails were a bit trickier since they were in the href and had to be key matched before using them
        email = email_tag.get_text(strip=True) if email_tag else "None Provided"  # Setting a default value

         #Getting the URL to each faculty members page
        faculty_url_tag = faculty.find('a', href=True)
        faculty_url = faculty_url_tag['href'] if faculty_url_tag else np.nan

        #some issues with incomplete URLs, ensuring that all are given the correct format if they are not already
        base_url = "https://scholars.duke.edu/person"
        if faculty_url and not faculty_url.startswith("http"):
            faculty_url = base_url + faculty_url
        
        data.append({'Name': name, 'Email': email, 'Designation': designation, 'URL': faculty_url})
    
    # Append the extracted data to the main data list
    all_data.extend(data)

# Save the extracted data to a CSV file
df = pd.DataFrame(all_data)
df.to_csv('duke_faculty_info_2.csv', index=False)
print("Data saved to duke_faculty_info_2.csv")