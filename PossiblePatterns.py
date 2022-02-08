zeros = []

with open("wordle_zeros", "r") as f:
    for l in f:
        l = l.strip()
        s = l.split(" ")
        zeros.append( set([int(x) for x in s[1:]]) )

days = [0]*2315
days[0] += 1

done = False

total = 0

while not done:
    z = set()
    s = -1
    for i in range(len(days)):
        if days[i] == 1:
            z = z.union(zeros[i])
            s *= -1

    n = 243 - len(z) - 1
    total += s * int( (n**7 - 1)/(n - 1) )

    print(f"\r{total}", end='')
    
    days[0] += 1
    i = 0
    while days[i] == 2:
        days[i] = 0
        i += 1
        if i == len(days):
            done = True
            break
        days[i] += 1

print(f'\r{" " * 80}', end='')
print(f'\r{total}')
