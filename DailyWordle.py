from datetime import datetime
from puzzle import Puzzle, score_to_emoji, int_to_score
import argparse

parser = argparse.ArgumentParser(description='Analyse the daily wordle.')
parser.add_argument('-d', '--day', metavar='N', type=int, dest='days', default=0, help='adjust the date by this many days')
parser.add_argument('-e', '--emoji', action='store_true' , dest='emoji', help='use emoji for the patterns')
parser.add_argument('-s', '--show', action='store_true' , dest='show', help='show the details of the analysis')
parser.add_argument('-w', '--word', action='store_true' , dest='word', help='show the word')

args = parser.parse_args()

if args.emoji:
    display_score = lambda s: score_to_emoji(int_to_score(s))
else:
    display_score = lambda s: " ".join([str(x) for x in int_to_score(s)])
    
wordle = Puzzle("Wordle", 5, True, 'wordle_guessable_words', 'wordle_guessing_words')

wordle_day = datetime.now().timetuple().tm_yday + 195 + args.days

daily_wordle = wordle.guessable_words[wordle_day]

if args.show:
    output = print
else:
    output = lambda x: None

if args.word:
    output(f'Wordle {wordle_day} {daily_wordle}')
else:
    output(f'Wordle {wordle_day}')
    

output('Frequency Analysis')
f = 1
guess = "soare"
while True:
    score = wordle.score(daily_wordle,guess)
    wordle.apply_guess(guess, score)
    pad = " " * (4 - len(str(len(wordle.current_words))))
    output(f' {guess} {pad}({len(wordle.current_words)}): {display_score(score)}')

    if wordle.is_solved():
        break
    guess = wordle.get_next_frequency_guess()
    f += 1

if guess != daily_wordle:
    f += 1

wordle.reset_scores()

guess_list = ['soare', 'linty', 'caber', 'whelp', 'vodka', 'feign', 'amaze', 'torus', 'adobe']

output('Naive Frequency Analysis')
n = 0
for guess in guess_list:
    score = wordle.score(daily_wordle,guess)
    wordle.apply_guess(guess, score)
    pad = " " * (4 - len(str(len(wordle.current_words))))
    output(f' {guess} {pad}({len(wordle.current_words)}): {display_score(score)}')

    n += 1
    if wordle.is_solved():
        break

if wordle.is_solved():
    if guess != daily_wordle:
        n += 1
else:
    n = "unsolved"    

wordle.reset_scores()

output('Minmax Analysis')
m = 1
guess = "arise"
division = 168
while True:
    score = wordle.score(daily_wordle,guess)
    pad = " " * (4 - len(str(division)))
    output(f' {guess} {pad}({division}): {display_score(score)}')
    wordle.apply_guess(guess, score)
    if wordle.is_solved():
        break
    (guess,division) = wordle.get_next_divide_guess()
    m += 1

if guess != daily_wordle:
    m += 1

print(f'Daily #Wordle ({wordle_day}) Ranking')
print(f'    Frequency: {f}')
print(f'   Guess List: {n}')
print(f'       Minmax: {m}')

zeros = {}
with open('wordle_zeros', 'r') as f:
    for l in f:
        l = l.strip()
        s = l.split(" ")
        zeros[s[0]] = [int(x) for x in s[1:]]

visible = [2315]*243
for w in zeros:
    for i in zeros[w]:
        visible[i] -= 1

todays_patterns = []
for i in range(243):
    if i not in zeros[daily_wordle]:
        todays_patterns.append(i)

todays_patterns.sort(key = lambda x: visible[x])

print("Rare patterns:")
next_pattern = 0
while True:
    pattern = display_score(todays_patterns[next_pattern])
    percentage = round(visible[todays_patterns[next_pattern]]*100/2315)
    print(f' {pattern} ({percentage}%)')
    next_pattern += 1
    if visible[todays_patterns[next_pattern]] > 232: # 10%
        break

