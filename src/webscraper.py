from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np

URL = "https://www.amazon.ca/s?k=apple+watch&rh=n%3A21204935011%2Cp_123%3A110955&dc&ds=v1%3AvWUjp7zRQaroET3KP58QQ3W2LnV%2FMr7jwBUsZ%2Bq6e9g&crid=1GWC8RCVDH93P&qid=1740559484&rnid=119962390011&sprefix=%2Caps%2C100&ref=sr_nr_p_123_1"

# Headers for request

HEADERS = ({'User-Agent':'YourUserAgent', 'Accept-Language': 'en-US, en;q=0.5'})

# HTTP Request
webpage = requests.get(URL, headers=HEADERS)

# Soup Containing all the data
soup = BeautifulSoup(webpage.content, "html.parser")

links = soup.find_all("a", attrs={'class':'a-link-normal s-line-clamp-2 s-link-style a-text-normal'})

links_list = []

for link in links:
    links_list.append(link.get('href'))

d = {"title":[ ], "price":[ ]}

for link in links_list:
    
    new_webpage = requests.get("https://www.amazon.ca" + link, headers=HEADERS)

    new_soup = BeautifulSoup(new_webpage.content, "html.parser")

    try:
        title = new_soup.find("span", attrs={'id':'productTitle'})
        title_value = title.text
        title_string = title_value.strip()
    
    except AttributeError:
        title_string = ""

    try:
        price_whole = new_soup.find("span", attrs={'class':'a-price-whole'}).text

    except AttributeError:
        price_whole = ""

    try:
        price_fraction = new_soup.find("span", attrs={'class':'a-price-fraction'}).text

    except AttributeError:
        price_fraction = ""
    
    price = price_whole + price_fraction

    d['title'].append(title_string)
    d['price'].append(price)

# Export it as CSV 

amazon_df = pd.DataFrame.from_dict(d)
amazon_df['title'].replace('', np.nan, inplace=True)
amazon_df = amazon_df.dropna(subset=['title'])
amazon_df.to_csv("amazon_data.csv", header=True, index=False)