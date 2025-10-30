from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from plyer import notification
import time
import subprocess

def open_wordle(driver):
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

def guess_words(driver, words):
    for word in words:
        for letter in word:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, 'body'))
            ).send_keys(letter)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'body'))
        ).send_keys(Keys.ENTER)
        time.sleep(2)  # Wait for the game to process the input

def check_last_row_all_correct(driver):
    # Wait for the 6th row to be present
    row_6 = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div[aria-label="Row 6"] div[data-testid="tile"]'))
    )
    
    # Check if all tiles in the 6th row have `data-state="correct"`
    for tile in row_6:
        data_state = tile.get_attribute('data-state')
        if data_state != 'correct':
            return False
    
    return True

# Initialize the WebDriver
driver = webdriver.Chrome()

# Open the first Wordle game and make guesses
open_wordle(driver)

# List of words to guess
words_to_guess = ['brick', 'glent', 'jumpy', 'vozhd', 'waqfs']

# Loop through each word and input it into the game
guess_words(driver, words_to_guess)

# Scrape the `data-key` and `data-state` values and filter by state
keys = driver.find_elements(By.CSS_SELECTOR, 'button[data-key][data-state]')
hints = []

for key in keys:
    data_key = key.get_attribute('data-key')
    data_state = key.get_attribute('data-state')
    if data_state in ['present', 'correct']:
        hints.append({'letter': data_key, 'state': data_state, 'position': None})

# Load the possible answers from the file
with open('possible_answers.txt', 'r') as file:
    possible_words = file.read().splitlines()

# Define letter position values
position_values = {
    'q': 3, 'w': 1, 'e': 3, 'r': 2, 't': 5, 'y': 5, 'u': 2, 'i': 3, 'o': 2,
    'p': 4, 'a': 2, 's': 5, 'd': 5, 'f': 4, 'g': 1, 'h': 4, 'j': 1, 'k': 5,
    'l': 2, 'z': 3, 'x': 5, 'c': 4, 'v': 1, 'b': 1, 'n': 4, 'm': 3
}

# Filter the possible words based on the hints
filtered_words = []

for word in possible_words:
    match = True
    if len(word) != 5:
        continue

    # Check for correct letters in correct positions
    for hint in hints:
        letter = hint['letter']
        state = hint['state']
        if state == 'correct':
            if letter not in word:
                match = False
                break
            if word[position_values[letter] - 1] != letter:
                match = False
                break
        elif state == 'present':
            if letter not in word:
                match = False
                break
            if word[position_values[letter] - 1] == letter:
                match = False
                break

    if match:
        filtered_words.append(word)

# Print the filtered words
print("Filtered words:", filtered_words)

# Try the filtered words in the new game
guess_words(driver, filtered_words)

# Check if the last row is all correct
if check_last_row_all_correct(driver):
    print("The last row is all correct!")
  
    notification.notify(
        title='The Wordle Of The Day Is:',
        message=', '.join(filtered_words).upper(),  # Convert list to a comma-separated string
        timeout=10  # Notification stays for 10 seconds
    )
else:
    print("The last row is not all correct.")
    driver.quit()
    driver = webdriver.Chrome()

    # Open the first Wordle game and make guesses
    open_wordle(driver)

    # Try the filtered words in the new game
    # Try the filtered words in the new game
guess_words(driver, filtered_words)

# Initialize correct_word variable
correct_word = None

try:
    # Scan through each row to check if all letters are correct
    for row_num in range(1, 7):  # Assuming the game has up to 6 rows
        row = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, f'div[aria-label="Row {row_num}"] div[data-testid="tile"]'))
        )

        # Check if all tiles in the current row have `data-state="correct"`
        all_correct = True
        for tile in row:
            data_state = tile.get_attribute('data-state')
            if data_state != 'correct':
                all_correct = False
                break

        # If all letters are correct, save the word
        if all_correct:
            correct_word = ''.join([tile.text for tile in row])
            print(f"The Wordle Of The Day: {correct_word}")
            break

    # Notify if the correct word is found
    if correct_word:
        notification.notify(
            title='The Wordle Of The Day Is:',
            message=correct_word.upper(),  # Display the correct word in uppercase
            timeout=10  # Notification stays for 10 seconds
        )
    else:
        print("No row with all letters correct was found.")
finally:
    # Quit the driver in all cases
    driver.quit()

