import json
import random
import numpy as np
from cards.card import CardType, Rarity
from cards.generate.name import name
from cards.generate.image import image


# A few diff quote sources
quotes = json.load(open('data/quotes/quotes.json', 'r'))
jokes = [{'body': q, 'attr': ''} for q in json.load(open('data/quotes/jokes.json', 'r')) if len(q) <= 250]
pickups = [{'body': q, 'attr': ''} for q in sum(json.load(open('data/quotes/pickuplines.json', 'r')).values(), [])]
philo = sum(json.load(open('data/quotes/philo_quotes.json', 'r')).values(), [])

card_type_probs = [
    0.5,    # unit
    0.125,  # action
    0.125,  # property
    0.125,  # condition
    0.125,  # event
]


def generate_card():
    typ = card_type()
    rar = rarity()
    pts = card_points(rar)
    cst = base_cost(rar)
    nam = name(typ)
    img = image(nam)
    qot = quote()

    attrs = {
        'name': nam,
        'image': img,
        'type': typ,
        'rarity': rar,
        'cost': cst,
        'quote': qot
    }

    if typ == CardType.unit:
        attrs['attack'], attrs['defense'] = stats(pts)

    efs, pts = effects(pts)

    attrs['effects'] = efs

    card = typ.value(**attrs)
    return card


def quote():
    source = random.choice([quotes, philo, jokes, pickups])
    return random.choice(source)


def rarity():
    # C,U,R
    r = np.random.multinomial(1, [0.8, 0.18, 0.02])

    # 0=C,1=U,2=R
    return Rarity(np.where(r)[0][0])


def card_points(rarity):
    """
    Max points is 10, min is 1
    Probability for a point is 0.8 weighted by the rarity
    """
    w = (rarity+1)/3
    return np.random.binomial(10, 0.8 * w) + 1


def base_cost(rarity):
    l, u = 2 - rarity, 4 - rarity
    return random.randint(l, u)


def card_type():
    r = np.random.multinomial(1, card_type_probs)
    i = np.where(r)[0][0]
    return list(CardType)[i]


def effects(pts):
    """
    Effects are passive (no cost)
    """
    return [], pts


def stats(pts):
    """
    Unit stats
    """
    atk = random.randint(0, pts - 1)
    dfn = pts - atk
    return atk, dfn
