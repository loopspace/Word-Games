from puzzle import Puzzle, wordle_score

wordle = Puzzle("Wordle", 5, True, 'wordle_guessable_words', 'wordle_guessing_words')

#wordle.generate_scores()
#wordle.save_scores("wordle_scores")
#exit()

wordle.load_scores('wordle_scores')

first_guess = wordle.get_next_divide_guess()
guesses = {}
n = 0
# Iterate through the possible words we can guess
for w in wordle.guessable_words:
    # Keep track of how many words we've done
    n += 1
    # Reset the scores
    wordle.reset_scores()
    # Initialise with the first guess, as it is always 'aloes'
    m = 1
    g = first_guess
    wordle.apply_guess(g, wordle_score(w,g))
    # Show where we're at
    print(f"\rWord: {w} ({n}) guess {m}", end='')
    # While we haven't solved it
    while not wordle.is_solved():
        # Increment the guess counter
        m += 1
        # Get the next guess
        g = wordle.get_next_divide_guess()
        # Apply it
        wordle.apply_guess(g, wordle_score(w,g))
        # Say where we are
        print(f"\rWord: {w} ({n}) guess {m}", end='')
    # The puzzle is solved, in that there's only one word left
    # If it *wasn't* our current guess, we need one more guess to say what it is
    if g != w:
        m += 1
        print(f"\rWord: {w} ({n}) guess {m}", end='')
    # Save the number of guesses
    guesses[w] = m
    print("\n", end='')

guess_order = {k: v for k, v in sorted(guesses.items(), key=lambda item: -item[1])}

for k in list(guess_order.keys())[:10]:
    print(f'{k} {guess_order[k]}')

number_of_guesses = [0]*10
for k,v in guesses.items():
    number_of_guesses[v] += 1

print(number_of_guesses)
