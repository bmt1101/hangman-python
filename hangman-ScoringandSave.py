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
    start_time = time.time()
    
    while not time_up:
        # Calculate the elapsed time since the countdown started
        elapsed_time = time.time() - start_time
        remaining_time = time_sec - elapsed_time

        if remaining_time <= 0:  # Time is up
            time_up = True
            sys.stdout.write(f"\rTime's up!               \n")
            sys.stdout.flush()
            break

        # Calculate minutes and seconds for remaining time
        mins, secs = divmod(int(remaining_time), 60)
        timeformat = '{:02d}:{:02d}'.format(mins, secs)

        # Clear the previous line and print the updated countdown
        sys.stdout.write(f"\rTime remaining: {timeformat}   \n")
        sys.stdout.flush()

        time.sleep(1)

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

    time_up_event = threading.Event()

    while True:
        # Check for saved game
        resume_game = input("Do you want to resume the previous game? (y/n): ").lower()
        if resume_game == 'y':
            game_state = load_game_state()
            if game_state:
                word = game_state['word']
                blank_list = game_state['blank_list']
                update_display = game_state['update_display']
                time_remaining = game_state['time_remaining']
                score = game_state['score']
                selected_category = game_state['selected_category']
                print("\nResuming your saved game...")
            else:
                print("\nNo saved game found. Starting a new game.")
                word = None
        else:
            word = None

        if not word:
            print("\nLet's play Hangman!")
            category_count = len(categories)
            while True:
                try:
                    category_choice = int(input(f"Choose a number for a category (1-{category_count}): "))
                    if 1 <= category_choice <= category_count:
                        selected_category = list(categories.keys())[category_choice - 1]
                        break
                    else:
                        print(f"Invalid choice. Please select a number between 1 and {category_count}.")
                except ValueError:
                    print("Please enter a valid number.")

            # Display difficulty levels
            print("\nChoose a difficulty level:")
            print("1. Easy (Simple and short words, 60 seconds)")
            print("2. Medium (Moderate difficulty, 90 seconds)")
            print("3. Hard (Complex and long words, 120 seconds)")

            while True:
                try:
                    difficulty_choice = int(input("Enter the number of your chosen difficulty: "))
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

            # Choose a word based on the selected category and difficulty
            word = random.choice(categories[selected_category][difficulty])

            # Game state initialization
            blank_list = ["_"] * len(word)
            update_display = 0

        # Start the countdown timer thread
        timer_thread = threading.Thread(target=countdown, args=(time_remaining,))
        timer_thread.daemon = True
        timer_thread.start()

        # Game loop
        while update_display < 8 and not time_up:
            print(f"\nHint: {selected_category}")
            print(f"Word: {' '.join(blank_list)}")
            print(HANGMANPICS[update_display])

            guess = input("Please guess a letter or the whole word: ").lower()

            if len(guess) == 1 and guess.isalpha():
                update_display, correct = making_a_guess(word, guess, update_display, blank_list)
                if correct:
                    score += 10  
                else:
                    time_remaining -= 5  
            elif len(guess) > 1 and guess.isalpha():
                if guess == word:
                    print(f"\nCongratulations, you've guessed the word correctly!")
                    score += 50  # Large score for guessing the whole word correctly
                    print(f"\nYOU WIN!")
                    time_up = True
                    break
                else:
                    print(f"\n'{guess}' is not the correct word.")
                    update_display += 1
                    print(HANGMANPICS[update_display])
            else:
                print("Invalid input. Please guess a single letter or a word.")
            print(f"{8 - update_display} attempts remaining.")

        # End of game
        if update_display == 8 or time_up:
            if not time_up:
                print(f"\nGAME OVER! All attempts used. The word was {word}.")
            time_up = True

        print(f"Your score: {score}")

        # Ask if they want to play again or save the game
        play_again = input("\nDo you want to play again? (y/n): ").lower()
        if play_again == 'y':
            time_up = False
            play_game()  # Restart the game
        else:
            save_progress = input("\nDo you want to save your progress? (y/n): ").lower()
            if save_progress == 'y':
                save_game_state(word, blank_list, update_display, time_remaining, score, selected_category)
            print("Thanks for playing!")

# Start the game
play_game()
