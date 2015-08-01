import random
from glob import glob
from cards.card import CardType
from collections import defaultdict

def load_lexicon(fname):
    with open(fname, 'r') as f:
        return [l.lower().strip() for l in f.readlines()]

def load_lexicons(pattern):
    return sum([load_lexicon(f) for f in glob(pattern)], [])

animals = load_lexicon('data/animals.txt')
adjs = load_lexicons('data/adjectives/*.txt')
advs = load_lexicons('data/adverbs/*.txt')
cnt_nouns = load_lexicons('data/countable_nouns/*.txt')
ucnt_nouns = load_lexicons('data/uncountable_nouns/*.txt')
verbs = load_lexicons('data/verbs/*.txt')
prefixes = load_lexicon('data/prefixes.txt')


def name(card_type):
    if card_type == CardType.unit:
        vocabs = [
            random.choice([adjs, nationalities]),
            animals
        ]
    elif card_type in [CardType.action, CardType.event]:
        vocabs = [
            advs,
            verbs
        ]
    elif card_type in [CardType.property, CardType.condition]:
        vocabs = [
            adjs,
            ucnt_nouns
        ]

    names = [random.choice(vocab) for vocab in vocabs]

    if random.random() >= 0.98:
        names[0] = random.choice(prefixes) + names[0]

    return ' '.join(names).title()


def weighted_choice(choices):
    """
    Random selects a key from a dictionary,
    where each key's value is its probability weight.
    """
    # Randomly select a value between 0 and
    # the sum of all the weights.
    rand = random.uniform(0, sum(choices.values()))

    # Seek through the dict until a key is found
    # resulting in the random value.
    summ = 0.0
    for key, value in choices.items():
        summ += value
        if rand < summ: return key

    # If this returns False,
    # it's likely because the knowledge is empty.
    return False


class Markov():
    def __init__(self, fname, state_size=3):
        """
        Recommended `state_size` in [2,5]
        """
        terms = load_lexicon(fname)
        mem = defaultdict(lambda: defaultdict(int))

        for t in terms:
            # Beginning & end
            mem['^'][t[:state_size]] += 1
            mem[t[-state_size:]]['$'] += 1

            for i in range(len(t) - state_size):
                prev = t[i:i+state_size]
                next = t[i+1:i+1+state_size]
                mem[prev][next] += 1

        self.mem = mem
        self.state_size = state_size

    def generate(self):
        ch = weighted_choice(self.mem['^'])
        out = [ch]
        while True:
            ch = weighted_choice(self.mem[ch])
            if ch == '$':
                break
            out.append(ch[self.state_size-1])
        return ''.join(out)


nation_mkv = Markov('data/countries.txt')

def nationality():
    nation = nation_mkv.generate()
    if nation[-1] == 'a':
        return nation + 'n'
    if nation[-1] == 'i':
        return nation + random.choice(['', 'c', 'sh', 'an'])
    if nation[-1] == 'e':
        return nation + random.choice(['se', 'an'])
    if nation[-1] == 'y':
        return nation[:-1] + 'ian'
    if nation[-1] == 'u':
        return nation + 'vian'
    else:
        return nation + random.choice(['ian', 'ean', 'ese', 'an', 'ish', 'ic', 'i'])

nationalities = [nationality() for n in range(16)]
