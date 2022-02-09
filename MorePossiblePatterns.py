zeros = {}
words = []

# Read in the sets of zeros - these are patterns that are impossible
# for a given word.  The possible patterns for a given word are the
# complement of this set.
with open("wordle_zeros", "r") as f:
    for l in f:
        l = l.strip()
        s = l.split(" ")
        zeros[s[0]] = set([int(x) for x in s[1:]])
        words.append(s[0])

# Some of the words have the property that their possible patterns are
# a (strict) subset of the possible patterns of another word.  We
# don't need to consider them so we remove them.
singletons = []
for w in words:
    subset = False
    for ww in words:
        if w < ww:
            if zeros[ww].issubset(zeros[w]):
                subset = True
                break
    if not subset:
        singletons.append(w)

# this reduces the number of words from 2315 to 2195, not a lot - but
# it's a little help.
words = singletons

# Now let's look for all the patterns
patterns = []
for i in range(7):
    patterns.append([])


# This will index a given pattern; we count through all the patterns
# by incrementing each index one by one from -1 to 241 (pattern 242 is
# the "all green" pattern which we don't allow in general position).
# The -1 represents "no pattern", so when the count "wraps round" then
# it wraps round to 0 so that we don't have gaps in the patterns.
pattern = [-1]*6
pattern[0] = 0

patterns = []

while True:
    found = False
    for w in words:
        found_here = True
        for p in pattern:
            if p in zeros[w]:
                found_here = False
                break
        if found_here:
            found = True
            break
    if found:
        patterns.append(pattern)
        print(f'\r{len(patterns)}', end= '')
    i = 0
    pattern[i] += 1
    while pattern[i] == 241:
        pattern[i] = 0
        i += 1
        if i == len(pattern):
            break
        if pattern[i] == -1:
            print(f'\rThere are {len(patterns)} patterns of length up to {i}')
        pattern[i] += 1

print(f'There are {len(patterns)} patterns in total')
