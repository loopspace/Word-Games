from puzzle import Puzzle, wordle_score

def score_to_int(s):
    n = 0
    for c in s:
        n *= 3
        n += int(c)
    return n

wordle = Puzzle("Wordle", 5, True, 'wordle_guessable_words', 'wordle_guessing_words')



#wordle.generate_scores()
#wordle.save_scores("wordle_scores")
#exit()

#wordle.load_scores('wordle_scores')

first_guess = wordle.get_next_divide_guess()

print(f'Guess: {first_guess}')
score = score_to_int(input("Score :"))

wordle.apply_guess(first_guess, score)


while not wordle.is_solved():
    print(f' Words left: {len(wordle.current_words)}')
    g = wordle.get_next_divide_guess()
    print(f' Next guess: {g}')
    score = score_to_int(input("Score :"))
    wordle.apply_guess(g, score)

print(f'Solution: {wordle.current_words[0]}')

