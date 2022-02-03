from datetime import datetime
from puzzle import Puzzle

def int_to_score(n):
    s = []
    for i in range(5):
        s.insert(0,n%3)
        n //= 3

    return s

wordle = Puzzle("Wordle", 5, True, 'wordle_guessable_words', 'wordle_guessing_words')

wordle_day = datetime.now().timetuple().tm_yday + 195 + 1

daily_wordle = wordle.guessable_words[wordle_day]

print('Frequency Analysis')
f = 1
guess = "soare"
while True:
    score = wordle.score(daily_wordle,guess)
    print(f' {guess}: {" ".join([str(s) for s in int_to_score(score)])}')
    wordle.apply_guess(guess, score)

    if wordle.is_solved():
        break
    guess = wordle.get_next_frequency_guess()
    f += 1

if guess != daily_wordle:
    f += 1

wordle.reset_scores()

guess_list = ['soare', 'linty', 'caber', 'whelp', 'vodka', 'feign', 'amaze', 'torus', 'adobe']

print('Naive Frequency Analysis')
n = 0
for guess in guess_list:
    score = wordle.score(daily_wordle,guess)
    print(f' {guess}: {" ".join([str(s) for s in int_to_score(score)])}')
    wordle.apply_guess(guess, score)
    n += 1
    if wordle.is_solved():
        break

if wordle.is_solved():
    if guess != daily_wordle:
        n += 1
else:
    n = "unsolved"    

wordle.reset_scores()

print('Minmax Analysis')
m = 1
guess = "arise"
division = 168
while True:
    score = wordle.score(daily_wordle,guess)
    pad = " " * (3 - len(str(division)))
    print(f' {guess} {pad}({division}): {" ".join([str(s) for s in int_to_score(score)])}')
    wordle.apply_guess(guess, score)
    if wordle.is_solved():
        break
    (guess,division) = wordle.get_next_divide_guess()
    m += 1

if guess != daily_wordle:
    m += 1

print("Daily Wordle Ranking")
print(f' Frequency: {f}')
print(f'Guess List: {n}')
print(f'    Minmax: {m}')

