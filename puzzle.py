def score_words(source_word, guess_word, multiplier = 1):
    stars = 0
    dots = 0
    not_matched = []
    source_not_matched = []
    for i in range(len(source_word)):
        stars *= multiplier
        if source_word[i] == guess_word[i]:
            stars += 1
        else:
            not_matched.append(i)
            source_not_matched.append(source_word[i])
    for i in range(len(source_word)):
        dots *= multiplier
        if i in not_matched and guess_word[i] in source_not_matched:
            dots += 1
            source_not_matched.remove(guess_word[i])
      
    return (dots,stars)

def dots_and_stars_score(source_word, guess):
  (dots,stars) = score_words(source_word, guess, 1)
  return dots + stars*(len(source_word) + 1)

def wordle_score(source_word, guess):
  (dots,stars) = score_words(source_word, guess, 3)
  return dots + stars*2

def readDictionary(dictionary, word_length, repetition):
    words = []
    with open(dictionary,'r') as f:
        for w in f:
            w = w.strip()
            if len(w) == word_length and (repetition or len(set(w)) == word_length):
                words.append(w)
    return words
            

class Puzzle:
    'A word-guessing puzzle'

    def __init__(
            self,
            style,
            word_length,
            repetitions,
            allowed_words,
            guessing_words
    ):
        if style == "Wordle":
            self.score_function = wordle_score
        else:
            self.score_function = dots_and_stars_score

        self.word_length = word_length

        self.guessable_words = readDictionary(
            allowed_words,
            word_length,
            repetitions
        )

        self.current_words = []
        for w in self.guessable_words:
            self.current_words.append(w)
        
        self.guessing_words = readDictionary(
            guessing_words,
            word_length,
            repetitions
        )
        self.guesses = []
        self.all_scores = {}

    def score(self,w,g):
        if w in self.all_scores:
            if g in self.all_scores[w]:
                return self.all_scores[w][g]
        return self.score_function(w,g)

    def load_scores(self, score_file):
        all_scores = {}
        for w in self.guessable_words:
            all_scores[w] = {}

        with open(score_file,'r') as f:
            for w in f:
                w = w.strip()
                s = w.split(" ")
                all_scores[ s[0] ][ s[1] ] = int(s[2])

        self.all_scores = all_scores

    def generate_scores(self):
        all_scores = {}
        for w in self.guessable_words:
            all_scores[w] = {}
            for g in self.guessing_words:
                all_scores[w][g] = self.score_function(w,g)

        self.all_scores = all_scores

    def save_scores(self,score_file):
        with open(score_file, 'w') as f:
            for w in self.guessable_words:
                for ww in self.guessing_words:
                    f.write(f"{w} {ww} {self.all_scores[w][ww]}\n")

        
    def apply_guess(self,g,s):
        self.guesses.append([g,s])
        words_to_keep = []
        for w in self.current_words:
            if self.score_function(w,g) == s:
                words_to_keep.append(w)
        self.current_words = words_to_keep

    def apply_guesses(self,guesses):
        for g in guesses:
            self.apply_guess(g[0],g[1])

    def reset_scores(self):
        self.current_words = []
        self.guesses = []
        for w in self.guessable_words:
            self.current_words.append(w)
            
    def is_solved(self):
        if len(self.current_words) == 1:
            return True
        else:
            return False

    def divide_current_words(self,g):
      divisions = []
      for i in range(243):
        divisions.append([])
      for w in self.current_words:
        divisions[self.score(w,g)].append(w)
      return divisions
          
    def get_next_divide_guess(self,matching = 1):
        # Matching says: when the number of matching words is at most this number then choose from that list instead of all words
        # Verbose means it prints out lots of interesting information

        if self.is_solved():
            return (self.current_words[0],1)

        # Now we iterate through the words, working out how each splits the search space
        divisions = {}

        for g in self.guessing_words:
            answers = [0]*243
            for w in self.current_words:
                answers[
                    self.score(w,g)
                ] += 1
            divisions[g] = max(answers)
        # Remove any words we've already guessed
        for s in self.guesses:
            divisions.pop(s[0],None)

        # Order the words by least worst size of group
        word_order = {k: v for k, v in sorted(divisions.items(), key=lambda item: item[1])}

  
        # Sort the allowed words by score
        current_word_order = sorted(self.current_words, key=lambda x: divisions[x])

        # The best overall guess
        if len(self.current_words) <= matching or word_order[ current_word_order[0] ] == word_order[ list(word_order.keys())[0] ] :
            best_guess = current_word_order[0]
        else:
            best_guess = list(word_order.keys())[0]

        return (best_guess,divisions[best_guess])

    def get_next_divide_guesses(self,number_to_return,matching = 1):
        # Matching says: when the number of matching words is at most this number then choose from that list instead of all words
        # Verbose means it prints out lots of interesting information

        if self.is_solved():
            return self.current_words[0]

        # Now we iterate through the words, working out how each splits the search space
        divisions = {}

        m = 0
        for g in self.guessing_words:
            m += 1
            answers = [0]*243
            for w in self.current_words:
                answers[
                    self.score(w,g)
                ] += 1
            divisions[g] = max(answers)
        # Remove any words we've already guessed
        for s in self.guesses:
            divisions.pop(s[0],None)

        # Order the words by least worst size of group
        word_order = {k: v for k, v in sorted(divisions.items(), key=lambda item: item[1])}

  
        # Sort the allowed words by score
        current_word_order = sorted(self.current_words, key=lambda x: divisions[x])

        # The best overall guess
        if len(self.current_words) <= matching or word_order[ current_word_order[0] ] == word_order[ list(word_order.keys())[0] ] :
            best_guesses = current_word_order
        else:
            best_guesses = list(word_order.keys())

        best_guesses = {k: divisions[k] for k in best_guesses[:10]}
            
        return best_guesses

    def get_next_two_divide_guesses(self,matching = 1):
        # Matching says: when the number of matching words is at most this number then choose from that list instead of all words
        # Verbose means it prints out lots of interesting information

        if self.is_solved():
            return self.current_words[0]

        # Now we iterate through the words, working out how each splits the search space
        divisions = {}

        for g in self.guessing_words:
          for gg in self.guessing_words:
            answers = [0]*243*243
            for w in self.current_words:
                answers[
                    self.score(w,g)*243 + self.score(w,gg)
                ] += 1
            divisions[g + " " + gg] = max(answers)
        # Remove any words we've already guessed
        for s in self.guesses:
            divisions.pop(s[0],None)

        # Order the words by least worst size of group
        word_order = {k: v for k, v in sorted(divisions.items(), key=lambda item: item[1])}

  
        # Sort the allowed words by score
        current_word_order = sorted(self.current_words, key=lambda x: divisions[x])

        # The best overall guess
        if len(self.current_words) <= matching or word_order[ current_word_order[0] ] == word_order[ list(word_order.keys())[0] ] :
            best_guess = current_word_order[0]
        else:
            best_guess = list(word_order.keys())[0]

        return best_guess

    def get_next_frequency_guess(self):

        # Array of frequency-by-position
        freq_pos = []
        # Seed it with a dictionary for each position
        for i in range(self.word_length):
            freq_pos.append({})

            # Each dictionary has letters for keys and 0 for initial value
            for c in range(97,123):
                freq_pos[i][chr(c)] = 0

            # Spacer to find letters that actually occur
            freq_pos[i][" | "] = 0.5

        # Iterate through the current words
        for w in self.current_words:
            for i in range(self.word_length):
                freq_pos[i][w[i]] += 1

        # If we know a letter is in a certain location then all our matching words will have that letter in that location, so we remove that from the frequency list
        # We do this by seeing how many letters there are in a given position.
        # Might consider adjusting this so that the positions with many options are given higher priority than the positions with fewer.
        for i in range(self.word_length):
            letters = [k for k, v in sorted(freq_pos[i].items(), key=lambda item: -item[1])] # sort letters by frequency
            nz = letters.index(" | ")
            for j in range(nz):
                freq_pos[i][letters[j]] *= (nz - 1)

        # These are the total letter frequencies
        letter_freqs = {}
        for c in range(97,123):
            f = 0
            for i in range(self.word_length):
                f += freq_pos[i][chr(c)]
            letter_freqs[chr(c)] = f

        # Now we iterate through the guessing words, scoring each one
        word_scores = {}

        for w in self.guessing_words:
            # Ignore words we've already guessed
            if w not in self.guesses:
                score = 0
                # The score is the sum of the positional frequencies
                for i in range(len(w)):
                    score += freq_pos[i][w[i]]
                # And add the overall frequency for each letter (ignoring repetitions)
                for c in set(w):
                    score += letter_freqs[c]
                word_scores[w] = score


        # Order the words by score from highest to lowest
        word_order = {k: v for k, v in sorted(word_scores.items(), key=lambda item: -item[1])}

        best_guess = list(word_order.keys())[0]

        return best_guess

    
