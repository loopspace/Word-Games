from datetime import datetime
from puzzle import Puzzle

def int_to_score(n):
    s = []
    for i in range(5):
        s.insert(0,n%3)
        n //= 3

    return s

wordle = Puzzle("Wordle", 5, True, 'wordle_guessable_words', 'wordle_guessing_words')

wordle_day = datetime.now().timetuple().tm_yday + 195

daily_wordle = wordle.guessable_words[wordle_day]

print('Frequency Analysis')
f = 0
while not wordle.is_solved():
    guess = wordle.get_next_frequency_guess()
    score = wordle.score(daily_wordle,guess)
    print(f' {guess}: {" ".join([str(s) for s in int_to_score(score)])}')
    wordle.apply_guess(guess, score)
    f += 1

if guess != daily_wordle:
    f += 1


wordle.reset_scores()

print('Minmax Analysis')
m = 0
while not wordle.is_solved():
    (guess,division) = wordle.get_next_divide_guess()
    score = wordle.score(daily_wordle,guess)
    print(f' {guess} ({division}): {" ".join([str(s) for s in int_to_score(score)])}')
    wordle.apply_guess(guess, score)
    m += 1

if guess != daily_wordle:
    m += 1

print("Daily Wordle Ranking")
print(f'Frequency: {f}')
print(f'   Minmax: {m}')

