from puzzle import Puzzle, wordle_score

def score_to_int(s):
    n = 0
    for c in s:
        n *= 3
        n += int(c)
    return n

dordleL = Puzzle("Wordle", 5, True, 'wordle_guessable_words', 'wordle_guessing_words')
dordleR = Puzzle("Wordle", 5, True, 'wordle_guessable_words', 'wordle_guessing_words')

first_guess = dordleL.get_next_frequency_guess()

print(f'Guess: {first_guess}')
scoreL = score_to_int(input(" Left Score: "))
scoreR = score_to_int(input("Right Score: "))

dordleL.apply_guess(first_guess, scoreL)
dordleR.apply_guess(first_guess, scoreR)

while not dordleL.is_solved() or not dordleR.is_solved():
    print(f' Words left: {len(dordleL.current_words)} and {len(dordleR.current_words)}')
    if dordleL.is_solved():
        guesses = dordleR.get_guess_scores()
    elif dordleR.is_solved():
        guesses = dordleL.get_guess_scores()
    else:
        guesses = dordleL.get_guess_scores()
        right_guesses = dordleR.get_guess_scores()
        
        for g in guesses:
            guesses[g] += right_guesses[g]
        guesses = {k: v for k, v in sorted(guesses.items(), key=lambda item: -item[1])}
    guess = list(guesses)[0]
    print(f' Next guess: {guess}')

    scoreL = score_to_int(input(" Left Score: "))
    scoreR = score_to_int(input("Right Score: "))

    dordleL.apply_guess(guess, scoreL)
    dordleR.apply_guess(guess, scoreR)
    
print(f'Solutions: {dordleL.current_words[0]} {dordleR.current_words[0]}')
