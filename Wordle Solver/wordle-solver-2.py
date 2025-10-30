from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Initialize the WebDriver
driver = webdriver.Chrome()

# Open the Wordle game
driver.get('https://www.nytimes.com/games/wordle/index.html')

# Wait for the 'Play' button to be clickable and then click it
play_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-testid="Play"]'))
)
play_button.click()

# Wait for the close button to be clickable and then click it
close_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, 'svg[data-testid="icon-close"]'))
)
close_button.click()

# Wait for the game to start
time.sleep(2)

# List of words to guess
words_to_guess = ['brick', 'glent', 'jumpy', 'vozhd', 'waqfs']

# Loop through each word and input it into the game
for word in words_to_guess:
    for letter in word:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'body'))
        ).send_keys(letter)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, 'body'))
    ).send_keys(Keys.ENTER)
    time.sleep(2)  # Wait for the game to process the input

# Scrape the `data-key` and `data-state` values and filter by state
keys = driver.find_elements(By.CSS_SELECTOR, 'button[data-key][data-state]')
for key in keys:
    data_key = key.get_attribute('data-key')
    data_state = key.get_attribute('data-state')
    if data_state in ['present', 'correct']:
        correct_letter = data_key
        correct_location = data_state
        print(f"Correct Letter: {correct_letter}, Location: {correct_location}")








