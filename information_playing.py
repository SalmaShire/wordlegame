import heapq
from collections import Counter
import random

def game_instruction():
    print("""Wordle is a single player game 
A player has to guess a five letter hidden word 
There is no limit to the number of attempts
Your Progress Guide "✔❌❌✔➕"  
"✔" Indicates that the letter at that position was guessed correctly 
"➕" indicates that the letter at that position is in the hidden word, but in a different position 
"❌" indicates that the letter at that position is wrong, and isn't in the hidden word   
Each guess must be exactly 5 letters long. No more, no less. """)

game_instruction()

def wordle_feedback(guess, hidden_word):
    feedback = []
    for i, letter in enumerate(guess):
        if letter == hidden_word[i]:
            feedback.append('✔')  
        elif letter in hidden_word:
            feedback.append('➕')  
        else:
            feedback.append('❌')  
    return feedback

def information_heuristic(guess, possible_words):
    letter_freq = Counter(letter for word in possible_words for letter in word)
    
    score = 0
    unique_letters = set(guess)
    for letter in unique_letters:
        score += letter_freq[letter]  
    
    return -score  

def filter_possible_words(guess, feedback, possible_words):
    return [word for word in possible_words if is_valid_word(word, feedback, guess)]

def is_valid_word(word, feedback, guess):
    for i, char in enumerate(guess):
        if feedback[i] == '✔' and word[i] != char:
            return False
        elif feedback[i] == '➕' and (char not in word or word[i] == char):
            return False
        elif feedback[i] == '❌' and char in word:
            return False
    return True

def play_wordle_with_heuristic(hidden_word, possible_words):
    attempt = 0  
    path = [] 

    first_guess = "biome"
    guess = first_guess  
    path.append(guess)
    attempt += 1 

    if guess == hidden_word:
        print(f"You guessed the word correctly in {attempt} attempt(s)! WIN 🕺🕺🕺 ")
        print("Guess Path:", path)
        return attempt 
    
    feedback = wordle_feedback(guess, hidden_word)
    print(f"Attempt {attempt}: Guess = {guess}, Feedback = {feedback}")
    possible_words = filter_possible_words(guess, feedback, possible_words)

    while True:  
        guess = min(possible_words, key=lambda word: information_heuristic(word, possible_words))
        path.append(guess)
        attempt += 1 

        if guess == hidden_word:
            print(f"You guessed the word correctly in {attempt} attempt(s)! WIN 🕺🕺🕺 ")
            print("Guess Path:", path)
            return attempt 

        feedback = wordle_feedback(guess, hidden_word)
        print(f"Attempt {attempt}: Guess = {guess}, Feedback = {feedback}")
        possible_words = filter_possible_words(guess, feedback, possible_words)

def run_trials(word_list, possible_words, trials=20):
    successes = 0
    attempts_per_trial = [] 
    
    for i in range(trials):
        hidden_word = word_list[i]
        trial_possible_words = possible_words.copy() 
        
        print(f"\nTrial {i + 1} with hidden word: {hidden_word}")
        attempt_count = play_wordle_with_heuristic(hidden_word, trial_possible_words)
        
        attempts_per_trial.append(attempt_count)
        if attempt_count <= 6:  
            successes += 1

    accuracy = (successes / trials) * 100
    print(f"\nAccuracy: {accuracy}% of trials found the word within 6 guesses.")
    print("Attempts per trial:", attempts_per_trial)
    return accuracy, attempts_per_trial

def load_word_list(filename):
    with open(filename, 'r') as file:
        words = [line.strip().lower() for line in file]
    return words

word_list = [
    "rossa", "jetty", "wizzo", "cuppa", "cohoe", "gurks", "squad", 
    "beisa", "shrug", "fossa", "fluyt", "camus", "speed", "mamil", 
    "array", "polio", "barns", "panes", "souts", "limas"
]
possible_words = load_word_list('words.txt')  # Load larger word list for possible guesses

# Run trials
run_trials(word_list, possible_words)
