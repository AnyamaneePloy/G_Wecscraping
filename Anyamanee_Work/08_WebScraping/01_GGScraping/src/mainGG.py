from bs4 import BeautifulSoup
import requests
import pandas as pd
import os 

# lst_url = input("Enter Google URL for get price: ")
lst_url = ['https://www.google.com/travel/search?q=tinidee&g2lb=2502548%2C2503771%2C2503781%2C2504375%2C2504510%2C4258168%2C4284970%2C4291517%2C4814050%2C4874190%2C4893075%2C4965990%2C10208620%2C10209060%2C72277293%2C72280816%2C72302247%2C72317059%2C72406588%2C72414906%2C72421566%2C72430562%2C72440517%2C72448541%2C72458060%2C72462234%2C72469155%2C72470440%2C72470899%2C72471280%2C72472051%2C72473738%2C72473841%2C72479991%2C72480010%2C72482825%2C72483525%2C72484083%2C72484736%2C72485656%2C72485658%2C72486593&hl=en-TH&gl=th&ssta=1&ts=CAESCgoCCAMKAggDEAAaOgocEhoKDS9nLzExZmZsMXc0eV86CUJhbmcgS2FkaRIaEhQKBwjoDxADGAISBwjoDxADGAMYATICCAIqBwoFOgNUSEI&qs=CAAgACgBMidDaGtJdFBTdHJQLWdpNWxsR2cwdlp5OHhNV1ptYkRGM05IbGZFQUU4DUgA&ap=KigKEgmt-jI29-4rQBGkBmr-eyJZQBISCeEEXnbo-ytAEaQGagIdI1lAMABoAboBBnByaWNlcw&ictx=1&ved=0CAAQ5JsGahgKEwjQi7q525WEAxUAAAAAHQAAAAAQtwI']
url = lst_url[0]

# Add mapping hotel

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36',
    'Accept-Language': 'en-US, en;q=0.5'
}

response  = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')

# Define the filename for the CSV file where data will be stored
filename = 'hotels_data.csv'
# Check if the file exists. If not, create it and write headers
if not os.path.isfile(filename):
    df = pd.DataFrame(columns=['name', 'comment', 'price1', 'price2', 'price3', 'pricetext'])
    df.to_csv(filename, index=False, mode='w', encoding='utf-8-sig')

# Find all the hotel elements in the HTML document
hotels = soup.findAll('div', {'class': 'IJxDxc'})

hotels_data = []
# Loop over the hotel elements and extract the desired data
for hotel in hotels:
    # Extract the hotel name
    name_element = hotel.find('span', {'data-click-type': '268'})
    webname = name_element.get_text(strip=True) if name_element else 'No name found'

    # Extract the hotel location
    comment_element = hotel.find('span', {'class': 'niTXmc x4RNH'})
    comment = comment_element.get_text(strip=True) if comment_element else 'No location found'

    # Extract the price text
    pricetext_element = hotel.find('span', {'class': 'ly5mBf'})
    pricetext = pricetext_element.get_text(strip=True).replace(u'\xa0', u' ') if pricetext_element else 'No price text found'

    # Initialize price variables
    price1, price2, price3 = 'No price found', 'No price found', 'No price found'

    # Find the outermost span that seems to contain the price-related spans
    price_container = hotel.find('span', class_='QoBrxc')
    if price_container:
        # Within this container, find the specific spans for price
        price_elements = price_container.find_all('span')
        # Map the found price elements to the price variables if they exist
        if price_elements:
            prices = [pe.get_text(strip=True).replace(u'\xa0', u' ') for pe in price_elements if pe.get_text(strip=True)]
            if len(prices) >= 3:
                price1, price2, price3 = prices[:3]

    # Append hotels_data with info about hotel
    hotels_data.append({
        'name': webname,
        'comment': comment,
        'price1': price1,
        'price2': price2,
        'price3': price3,
        'pricetext': pricetext
    })

    # Convert the list of dictionaries to a DataFrame
    df = pd.DataFrame(hotels_data)
    df.to_csv(filename, index=False, mode='a', header=False, encoding='utf-8-sig')

# Read the entire file to check the data
df = pd.read_csv(filename)
print(df.head(3))
# # Now you can print the results or work with the hotels_data list
# for hotel_info in hotels_data:
#     print(hotel_info)