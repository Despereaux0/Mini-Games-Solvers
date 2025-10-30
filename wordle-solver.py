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

# Function to enter a guess and submit
def enter_guess(guess):
    for letter in guess:
        input_box = driver.find_element(By.TAG_NAME, 'body')
        input_box.send_keys(letter)
    input_box.send_keys(Keys.RETURN)

# Function to get feedback for the guess
def get_feedback():
    time.sleep(2)  # Adjust if necessary
    feedback_elements = driver.find_elements(By.CLASS_NAME, 'Tile')
    feedback = [el.get_attribute('data-state') for el in feedback_elements[-5:]]
    print(f"Feedback elements: {feedback_elements[-5:]}")  # Debug statement
    print(f"Feedback: {feedback}")  # Debug statement
    return feedback

# Load a list of possible words (example list)
possible_words = ['brick', 'glent', 'jumpy', 'vozhd', 'waqfs']

# Basic word filtering function based on feedback
def filter_words(words, guess, feedback):
    print(f"Filtering words based on guess: {guess} and feedback: {feedback}")  # Debug statement
    new_words = []
    for word in words:
        valid = True
        for i in range(len(guess)):
            if feedback[i] == 'correct' and word[i] != guess[i]:
                valid = False
            elif feedback[i] == 'present' and (word[i] == guess[i] or guess[i] not in word):
                valid = False
            elif feedback[i] == 'absent' and guess[i] in word:
                valid = False
        if valid:
            new_words.append(word)
    return new_words

# Main solver loop
for _ in range(6):
    guess = possible_words[0]
    enter_guess(guess)
    feedback = get_feedback()
    if feedback == ['correct'] * 5:
        print(f'Wordle solved with the word: {guess}')
        break
    possible_words = filter_words(possible_words, guess, feedback)
    if not possible_words:
        print('No valid words left!')
        break

# Close the browser
driver.quit()



