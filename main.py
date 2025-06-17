import random
from enum import Enum

# Load words
with open("words.txt") as f:
    possibilities = [word.strip().lower() for word in f if len(word.strip()) == 5]

class Colors(Enum):
    GREY = 0
    YELLOW = 1
    GREEN = 2

def analyze_guess(guess: str, result: tuple[int]):
    green = {}         
    yellow = {}        
    letter_counts = {} 
    invalid = set()

    for i, color in enumerate(result):
        letter = guess[i]

        #If Green, Save Position and Letter
        if color == Colors.GREEN.value:
            green[i] = letter
            letter_counts[letter] = letter_counts.get(letter,0) + 1

        #If Yellow,add index to forbidden positions for letter that does exist
        elif color == Colors.YELLOW.value:
            if letter not in yellow:
                yellow[letter] = []
            yellow[letter].append(i)
            letter_counts[letter] = letter_counts.get(letter, 0) + 1

    #If Value is Gray and wasn't picked up by any of the other markers, add to invalid letters
    for i, color in enumerate(result):
        letter = guess[i]
        if color == Colors.GREY.value and letter_counts.get(letter, 0) == 0:
            invalid.add(letter)
    return invalid, green, yellow

def prune_possibilities(invalid: set, green: dict, yellow: dict, guesses: list[str]) -> list[str]:
    new_possibilities = []

    for word in guesses:
        # 1. Check invalid letters
        if any(letter in word for letter in invalid):
            continue

        # 2. Check green positions
        if any(word[i] != letter for i, letter in green.items()):
            continue

        # 3. Check yellow letters
        if not all(
            letter in word and all(word[i] != letter for i in positions)for letter, positions in yellow.items()):
            continue

        new_possibilities.append(word)

    return new_possibilities

def safe_input_color(guess: str) -> tuple[int]:
    #Errir handling for User input
    while True:
        try:
            entry = input(f"Colors for '{guess}': ").strip()
            values = tuple(int(x) for x in entry.split(","))
            if len(values) != 5 or any(x not in (0,1,2) for x in values):
                raise ValueError
            return values
        except Exception:
            print(" Please enter exactly 5 numbers (0, 1, or 2), separated by commas.")

def play(previous_guess: str, guesses: list[str], tries: int = 1):
    color_result = safe_input_color(previous_guess)

    if color_result == (2, 2, 2, 2, 2):
        print(f"Wordle completed in {tries} steps!")
        return
    
    if tries == 6:
        print(f"Out of tries. Possible words are {guesses}")
        return

    previous_guess_count  = len(guesses)
    prev_guesses = guesses

    invalid, green, yellow = analyze_guess(previous_guess, color_result)
    guesses = prune_possibilities(invalid, green, yellow, guesses)

    current_guess_count=len(guesses)

    print(f"Found {current_guess_count} remaining matches")
    print(f"Reduced guesses by {previous_guess_count}")

    if not guesses:
        print("No Matches found.")
        print(f"Previous guesses {prev_guesses}")
        return

    next_guess = random.choice(guesses)
    print(f"Guess: {next_guess}")
    play(next_guess, guesses, tries + 1)


guesses = ["adieu","audio","auloi","aurei","louie","miaou","ouija","ourie","uraei"] #English words that contain at least 4 vowels

first_guess = random.choice(guesses)
print(f"First guess: {first_guess}")
play(previous_guess="miaou", guesses=possibilities)
