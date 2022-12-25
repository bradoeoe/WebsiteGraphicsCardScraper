from selenium import webdriver
from bs4 import BeautifulSoup
import re

# Read the list of websites from the config file
with open("config.txt", "r") as config_file:
    websites = config_file.read().splitlines()

# Initialize a list to store the prices and websites
prices = []

# Initialize a variable to store the lowest price found
lowest_price = float("inf")

# Start a webdriver (e.g., Chrome)
driver = webdriver.Edge()

# Scrape each website in the list
for website in websites:
    # Load the website in the webdriver
    driver.get(website)

    # Wait for the page to fully load
    # You may need to adjust this value depending on the speed of your internet connection and the size of the page
    driver.implicitly_wait(5)

    # Retrieve the HTML of the page
    html = driver.page_source

    # Parse the HTML with Beautiful Soup
    soup = BeautifulSoup(html, "html.parser")

    # Try each class name in the list to find the price element
    price_element = None
    class_names = [
        "price",
        "goods-price ele-goods-price",
        "current",
        "detail-product-price",
        "saleprice",
    ]
    for class_name in class_names:
        # Find all elements with the current class name in both span and div elements
        price_elements = soup.find_all(["span", "div"], class_=class_name)
        # If any elements are found, update the price_element variable
        if price_elements:
            price_element = price_elements
            break

    # Extract the price from the element if it was found
    if price_element:
        # Initialize a flag to indicate whether any prices were found
        found_price = False
        # Iterate through all the elements found
        for element in price_element:
            # Extract the price from the element
            price = element.text.strip()
            # Remove any dollar signs or commas
            price = price.replace('$', '')
            price = price.replace(',', '')
            # Remove any trailing zeros
            price = price.rstrip('0')
            price = re.sub(r'\s+', ' ', price)
            price = price.replace('\n', '')
            price = ' '.join(price.split())
            price_parts = re.findall(r'\d+', price)
            price = price_parts[0]
            # Convert the price to a float
            price = float(price)
            print(str(price) + website)

            # Add the price and website to the list
            prices.append((price, website))
            # Set the flag to indicate that a price was found
            found_price = True

        # If no prices were found, print an error message
        if not found_price:
            print(f"No prices were found on {website}.")

# Close the webdriver
driver.close()

# Find the lowest price
lowest_price = min(prices, key=lambda x: x[0])[0]

# Find the website with the lowest price
lowest_price_website = min(prices, key=lambda x: x[0])[1]

# Print the lowest price and website
print(f"The lowest price for an RTX 4090 is ${lowest_price} on {lowest_price_website}.")