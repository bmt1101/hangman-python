import random
import threading
import time
import sys
import os
import pickle
from categories import categories

# Global variables
time_up = False
score = 0

# Function for making a guess
def making_a_guess(word, guess, update_display, blank_list):
    correct_guess = False

    for x, letter in enumerate(word):
        if guess.lower() == letter:
            blank_list[x] = guess.lower()
            correct_guess = True

    if not correct_guess:
        print(f"\nThere is no '{guess}', sorry.")
        update_display += 1
        print(HANGMANPICS[update_display])
        return update_display, False
    return update_display, True

# Timer function to display countdown in real-time
def countdown(time_sec):
    global time_up
    while time_sec and not time_up:
        mins, secs = divmod(time_sec, 60)
        timeformat = '{:02d}:{:02d}'.format(mins, secs)
        sys.stdout.write(f"\rTime remaining: {timeformat} | Guess a letter or the word:     ")
        sys.stdout.flush()
        time.sleep(1)
        time_sec -= 1

        if time_sec == 0 and not time_up:
            time_up = True
            break_message = "GAME OVER! Time's up. The word was {word}."
            sys.stdout.write(f"\r{break_message}               \n")
        sys.stdout.flush()
        

# Hangman pictures
HANGMANPICS = [''' 
   ---+ 
      | 
      | 
      | 
      | 
      | 
=========''',
''' 
  +---+ 
      | 
      | 
      | 
      | 
      | 
=========''',
''' 
  +---+ 
  |   | 
      | 
      | 
      | 
      | 
=========''',
''' 
  +---+ 
  |   | 
  O   | 
      | 
      | 
      | 
=========''',
''' 
  +---+ 
  |   | 
  O   | 
 /    | 
      | 
      | 
=========''',
''' 
  +---+ 
  |   | 
  O   | 
 /|   | 
      | 
      | 
=========''',
''' 
  +---+ 
  |   | 
  O   | 
 /|\\ | 
      | 
      | 
=========''',
''' 
  +---+ 
  |   | 
  O   | 
 /|\\ | 
 /    | 
      | 
=========''',
''' 
  +---+ 
  |   | 
  O   | 
 /|\\ | 
 / \\ | 
      | 
=========''']

# Save game state to a file
def save_game_state(word, blank_list, update_display, time_remaining, score, selected_category):
    game_state = {
        'word': word,
        'blank_list': blank_list,
        'update_display': update_display,
        'time_remaining': time_remaining,
        'score': score,
        'selected_category': selected_category
    }
    with open('hangman_save.pickle', 'wb') as f:
        pickle.dump(game_state, f)
    print("\nGame saved successfully!")

# Load game state from a file
def load_game_state():
    if os.path.exists('hangman_save.pickle'):
        try:
            with open('hangman_save.pickle', 'rb') as f:
                return pickle.load(f)
        except (EOFError, pickle.UnpicklingError):
            print("Save file is empty or corrupted. Starting a new game.")
            os.remove('hangman_save.pickle')  # Delete corrupted file
    return None  # No valid saved game

def play_game():
    global score, time_up

    # Load game state if it exists
    game_state = load_game_state()
    if game_state:
        score += game_state['score']  # Add previous score to current score

    time_up_event = threading.Event()

    print("\nLet's play Hangman!")
    print("Mechanics:\n1. You have to guess the word before the timer runs out or before you run out of attempts.\n2. You can guess a letter or the whole word.")
    print("\nScoring:\nFor Letter Guess: +1 point\nFor Word Guess: Easy (+10 points), Medium (+15 points), Hard (+20 points)")
    print(f"\nYour score: {score}")

    while True:
        word = None

        category_count = len(categories)
        while True:
            try:
                category_choice = int(input(f"\nChoose a number for a category (1-{category_count}): "))
                if 1 <= category_choice <= category_count:
                    selected_category = list(categories.keys())[category_choice - 1]
                    break
                else:
                    print(f"Invalid choice. Please select a number between 1 and {category_count}.")
            except ValueError:
                print("Please enter a valid number.")

        print("\nChoose a difficulty level:")
        print("1. Easy (Simple and short words, 60 seconds)")
        print("2. Medium (Moderate difficulty, 90 seconds)")
        print("3. Hard (Complex and long words, 120 seconds)")

        while True:
            try:
                difficulty_choice = int(input("\nEnter the number of your chosen difficulty: "))
                if difficulty_choice == 1:
                    difficulty = "easy"
                    time_remaining = 60
                elif difficulty_choice == 2:
                    difficulty = "medium"
                    time_remaining = 90
                elif difficulty_choice == 3:
                    difficulty = "hard"
                    time_remaining = 120
                else:
                    print("Invalid choice. Please select 1, 2, or 3.")
                    continue
                break
            except ValueError:
                print("Please enter a valid number.")

        word = random.choice(categories[selected_category][difficulty])
        blank_list = ['_' if char != ' ' else ' ' for char in word]
        update_display = 0

        while update_display < 8 and not time_up:
            print(f"\nHint: {selected_category}")
            print(f"Word: {' '.join(blank_list)}")
            print(f"Your score: {score}")
            print(HANGMANPICS[update_display])

            timer_thread = threading.Thread(target=countdown, args=(time_remaining,))
            timer_thread.daemon = True
            timer_thread.start()

            guess = input().lower()
            if len(guess) == 1 and guess.isalpha():
                update_display, correct = making_a_guess(word, guess, update_display, blank_list)
                if correct:
                    score += 1 
                else:
                    time_remaining -= 3
            elif len(guess) > 1 and guess.replace(' ', '').isalpha():
                if guess == word:
                    print(f"\nCONGRATULATIONS! YOU GUESSED THE WORD CORRECTLY!")
                    if difficulty == "easy":
                        score += 10
                    elif difficulty == "medium":
                        score += 15
                    elif difficulty == "hard":
                        score += 20
                    print(f"HANGMAN IS FREE!")
                    time_up = True
                    break
                else:
                    print(f"\n'{guess}' is not the correct word.")
                    update_display += 1
                    print(HANGMANPICS[update_display])
            else:
                print("Invalid input. Letter or word must be entered.")
            print(f"{8 - update_display} attempts remaining.")

        if update_display == 8 or time_up:
            if not time_up:
                print(f"\nGAME OVER! All attempts used. The word was {word}.")
            time_up = True

        print(f"Your score: {score}")

        # Automatically save the game state after each round
        save_game_state(word, blank_list, update_display, time_remaining, score, selected_category)

        # Ask if they want to play again
        play_again = input("\nDo you want to play again? (y/n): ").lower()
        if play_again == 'y':
            time_up = False
            continue  # Restart the game loop
        else:
            print(f"Your Final Score: {score} points")
            print("Thanks for playing!")
            break

# Start the game
play_game()