# Import the required libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd


base_url = "https://www.flipkart.com/search?q=laptops&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=off&as=off"


# Launch browser and open target website
driver = webdriver.Chrome()

wait = WebDriverWait(driver, 15)

time.sleep(3)


# Lists to store scraped laptop information
names = []
processors = []
rams = []
ssds = []
systems = []
displays = []
prices = []


# Iterate through multiple pages and collect laptop data
for page in range(40):

    print(f"Scraping Page {page + 1}")

    if page==0:
        url =  base_url
    else:
        url = base_url + f"=off&page={page}"

    # open current page
    driver.get(url)
    
    # wait to load the page
    time.sleep(3)
   
    # Wait for product cards
    wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "jIjQ8S")))
    

    product_cards = driver.find_elements(By.CLASS_NAME, "jIjQ8S")


    # Extract laptop information
    for card in product_cards:

        # Laptop name
        try:
            name = card.find_element(By.CLASS_NAME, "RG5Slk").text
        except:
            name = None

        names.append(name)


        # Processor
        try:
            processor = card.find_element(By.XPATH, './/li[@class="DTBslk" and contains(text(), "Processor")]').text
        except:
            processor = None

        processors.append(processor)


        # RAM
        try:
            ram = card.find_element(By.XPATH, './/li[@class="DTBslk" and contains(text(), "RAM")]').text
        except:
            ram = None

        rams.append(ram)


        # SSD
        try:
            ssd = card.find_element(By.XPATH, './/li[@class="DTBslk" and contains(text(), "SSD")]').text
        except:
            ssd = None

        ssds.append(ssd)


        # System
        try:
            system = card.find_element(By.XPATH, './/li[@class="DTBslk" and contains(text(), "System")]').text
        except:
            system = None

        systems.append(system)


        # Display
        try:
            display = card.find_element(By.XPATH, './/li[@class="DTBslk" and contains(text(), "Display")]').text
        except:
            display = None

        displays.append(display)


        # Price
        try:
            price = card.find_element(By.CSS_SELECTOR, ".hZ3P6w.DeU9vF").text
        except:
            price = None

        prices.append(price)
    
    time.sleep(1)





# Store extracted data
data = {
    "Name": names,
    "Price": prices,
    "Ram": rams,
    "System": systems,
    "SSD": ssds,
    "Processor": processors,
    "Display": displays
}


# Make dataframe
df = pd.DataFrame(data)


# Save dataframe
df.to_csv(
    "Data/raw_data.csv",
    index=False
)


# Close browser
driver.quit()


print(f"Total Records Collected : {len(df)}")