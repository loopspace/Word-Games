from puzzle import Puzzle, wordle_score

def score_to_int(s):
    n = 0
    for c in s:
        n *= 3
        n += int(c)
    return n

def save_max_divisions(div_file):
    divisions = {}
    with open(div_file, 'w') as f:

        for g in wordle.guessing_words:
            d = wordle.divide_current_words(g)
            m = [len(x) for x in d]
            mx = max(m)
            p = m.index(mx)
            divisions[g] = [mx,p]
            mpad = " " * (4 - len(str(mx)))
            ppad = " " * (3 - len(str(p)))
            print(f"\r> {g} {mpad}{mx} {ppad}{p}", end='')
            f.write(f"{g} {mx} {p}\n")
    return divisions


def load_max_divisions(div_file):
    divisions = {}
    with open(div_file, 'r') as f:
        for l in f:
            l = l.strip()
            s = l.split(" ")
            divisions[s[0]] = [int(s[1]), int(s[2])]
    return divisions


def save_level_two_divisions(divisions, div_file):
    level_two_divisions = {}

    with open(div_file, 'w') as f:
        for k,v in divisions.items():
            if v[0] <= 243:
                wordle.reset_scores()
                wordle.apply_guess(k, v[1])
                for g in wordle.guessing_words:
                    d = wordle.divide_current_words(g)
                    m = [len(x) for x in d]
                    mx = max(m)
                    p = m.index(mx)
                    level_two_divisions[k + " " + g] = [mx,p]
                    mpad = " " * (4 - len(str(mx)))
                    ppad = " " * (3 - len(str(p)))
                    print(f"\r>{k} {g} {mpad}{mx} {ppad}{p}", end='')
                    f.write(f"{k} {g} {mx} {p}\n")


def search_level_two_divisions(divisions,div_file):
    with open(div_file, 'r') as f:
        for l in f:
            l = l.strip()
            s = l.split(" ")
            print(f"\r{s[0]} {s[1]}", end='')
            if int(s[3]) == 0:
                if divisions[s[0]][1] == 0:
                    wordle.reset_scores()
                    wordle.apply_guess(s[0],0)
                    wordle.apply_guess(s[1],0)
                    (ng,mx) = wordle.get_next_divide_guess()
                    if mx == 1:
                        print(f" {ng} {mx}")
            

                    
wordle = Puzzle("Wordle", 5, True, 'wordle_guessable_words', 'wordle_guessing_words')

absurdle_file = "absurdle_divisions.txt"
absurdle_second_file = "absurdle_small_divisions.txt"

#save_max_divisions(absurdle_file)
divisions = load_max_divisions(absurdle_file)

#save_level_two_divisions(divisions, absurdle_second_file)
search_level_two_divisions(divisions,absurdle_second_file)
