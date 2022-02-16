from puzzle import Puzzle, wordle_score

#
# This program produces a file of all the patterns that *don't* occur
# with a particular word.
#

wordle = Puzzle('wordle_guessable_words', 'wordle_guessing_words')

patterns = {}
zeros = {}
visible = [0]*243

for w in wordle.guessable_words:
    patterns[w] = [0]*243
    zeros[w] = []
    for g in wordle.guessing_words:
        s = wordle_score(w,g)
        patterns[w][s] += 1
    for i in range(243):
        if patterns[w][i] == 0:
            zeros[w].append(i)
        else:
            visible[i] += 1

print("Patterns to ignore: ", end="")
for i in range(243):
    if visible[i] == 0:
        print(i, end=", ")
print()

sorted_patterns = list(range(243))
sorted_patterns.sort(key=lambda x: visible[x])

for i in sorted_patterns:
    print(f'{i}: {visible[i]}')

with open('wordle_zeros', 'w') as f:
    for w in zeros:
        f.write(f'{w} {" ".join([str(z) for z in zeros[w]])}\n')
