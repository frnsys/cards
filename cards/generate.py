import json
import random
import numpy as np
from cards.card import CardType
from urllib import request, parse


def load_lexicon(fname):
    with open('data/{}'.format(fname), 'r') as f:
        return [l.strip() for l in f.readlines()]

# https://developers.google.com/image-search/v1/jsondevguide?hl=en
image_url = 'https://ajax.googleapis.com/ajax/services/search/images?v=1.0&safe=active&q='
adjectives = load_lexicon('adjectives.txt')
animals = load_lexicon('animals.txt')
adjs = load_lexicon('wn_adjs.txt')
advs = load_lexicon('wn_advs.txt')
nouns = load_lexicon('wn_nouns.txt')
verbs = load_lexicon('wn_verbs.txt')

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

    abs, pts = abilities(pts)
    efs, pts = effects(pts)

    attrs = {
        'name': nam,
        'image': img,
        'type': typ,
        'rarity': rar,
        'cost': cst,
        'abilities': abilities,
        'effects': effects,
    }

    if typ == CardType.unit:
        attrs['attack'], attrs['defense'] = stats(pts)

    card = typ.value(**attrs)
    return card


def name(card_type):
    if card_type == CardType.unit:
        prefix = adjectives
        suffix = animals
    elif card_type in [CardType.action, CardType.event]:
        prefix = advs
        suffix = verbs
    elif card_type in [CardType.property, CardType.condition]:
        prefix = adjs
        suffix = nouns

    names = [random.choice(prefix),
            random.choice(prefix),
            random.choice(suffix).lower()]
    return ' '.join(names).title()


def image(name):
    q = parse.quote(name)
    url = image_url + q
    req = request.Request(url, headers={'User-Agent': 'Chrome'})
    resp = request.urlopen(req)
    body = resp.read()
    return json.loads(body.decode('utf-8'))['responseData']['results'][0]['url']


def rarity():
    # C,U,R
    r = np.random.multinomial(1, [0.8, 0.18, 0.02])

    # 0=C,1=U,2=R
    return np.where(r)[0][0]


def card_points(rarity):
    """
    Max points is 10
    Probability for a point is 0.8 weighted by the rarity
    """
    w = (rarity+1)/3
    return np.random.binomial(10, 0.8 * w)


def base_cost(rarity):
    l, u = 2 - rarity, 4 - rarity
    return np.random.randint(l, u)


def card_type():
    r = np.random.multinomial(1, card_type_probs)
    i = np.where(r)[0][0]
    return list(CardType)[i]


def abilities(pts):
    """
    Abilities have a cost to play
    """
    return [], pts


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