from puzzle import Puzzle, wordle_score, score_to_int

wordle = Puzzle('wordle_guessable_words', 'wordle_guessing_words')

frequency_guess = "soare"
divide_guess = "arise"

while not wordle.is_solved():
    if len(wordle.current_words) == 0:
        print("No solution found")
        break
    print(f' Words left: {len(wordle.current_words)}')
    show_words = input(" Show words (y/n) ")
    if show_words.lower() == "y":
        print(" ".join(wordle.current_words))
    print(f'Suggested guesses, frequency: {frequency_guess}, divide: {divide_guess}')
    guess = input("Guess: ")
    if guess == "":
        break
    score = score_to_int(input("Score: "))

    wordle.apply_guess(guess, score)
    frequency_guess = wordle.get_next_frequency_guess()
    divide_guess = wordle.get_next_divide_guess()[0]

if wordle.is_solved():
    print(f'Solution: {wordle.current_words[0]}')

