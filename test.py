from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Set up the WebDriver
driver = webdriver.Chrome()

# URL of the webpage to scrape
url = "https://gist.github.com/cfreshman/d97dbe7004522f7bc52ed2a6e22e2c04"

# Open the URL with the WebDriver
driver.get(url)

# Find the parent element that contains all <td> elements
parent_element = driver.find_element(By.ID, "file-wordle-nyt-words-14855-txt")

# Find all <td> elements within the parent element
td_elements = parent_element.find_elements(By.TAG_NAME, 'td')

# Open a file to write the results
with open('possible_answers.txt', 'w') as file:
    # Write each <td> text content into the file
    for td in td_elements:
        file.write(td.text + '\n')

# Close the WebDriver
driver.quit()




