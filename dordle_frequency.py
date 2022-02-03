from puzzle import Puzzle, wordle_score

dordleL = Puzzle("Wordle", 5, True, 'wordle_guessable_words', 'wordle_guessing_words')
dordleR = Puzzle("Wordle", 5, True, 'wordle_guessable_words', 'wordle_guessing_words')


frequencies = [0]*20

for wL in dordleL.guessable_words:
    for wR in dordleR.guessable_words:
        if wL < wR:
            dordleL.reset_scores()
            dordleR.reset_scores()

            n = 0
            while not dordleL.is_solved() or not dordleR.is_solved():
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
                scoreL = wordle_score(wL,guess)
                scoreR = wordle_score(wR,guess)

                dordleL.apply_guess(guess, scoreL)
                dordleR.apply_guess(guess, scoreR)

                n += 1

            if guess != wL:
                n += 1
            if guess != wR and wL != wR:
                n += 1

            frequencies[n] += 1

print(frequencies)

