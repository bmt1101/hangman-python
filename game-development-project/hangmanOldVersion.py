import random
import threading
import time
import sys
import os
from categories import categories  # Import categories from the external file

# Global variable for time_up
time_up = False

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
        print(HANGMANPICS[update_display])  # Display hangman image for incorrect guesses
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


def play_game():
    global time_up  # Ensure time_up is globally accessible

    print("Let's play Hangman!")

    # Display category
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

        # Always display the Hangman picture
        print(HANGMANPICS[update_display])

        guess = input("Please guess a letter or the whole word: ").lower()

        if len(guess) == 1 and guess.isalpha():
            update_display, correct = making_a_guess(word, guess, update_display, blank_list)  # Pass word and guess to making_a_guess()
            if not correct:
                time_remaining -= 5
        elif len(guess) > 1 and guess.isalpha():
            if guess == word:
                print(f"\nCongratulations, you've guessed the word correctly!")
                print(f"\nYOU WIN!")
                time_up = True  # Set time_up to True to exit the game loop early
                break  # Exit the loop since the game is won
            else:
                print(f"\n'{guess}' is not the correct word.")
                update_display += 1
                print(HANGMANPICS[update_display])
        else:
            print("Invalid input. Please guess a single letter or a word.")
        print(f"{8 - update_display} attempts remaining.")

    # End of game (after exiting loop)
    if update_display == 8 or time_up:
        if not time_up:
            print(f"\nGAME OVER! All attempts used. The word was {word}.")
        time_up = True

    # Ask if they want to play again
    play_again = input("\nDo you want to play again? (y/n): ").lower()
    if play_again == 'y':
        time_up = False  # Reset the global time_up variable
        play_game()  # Restart the game
    else:
        print("Thanks for playing!")


# Start the game again
play_game()
