import re
from flask import Flask, render_template
from cards.generate import generate_card

app = Flask(__name__, static_folder='static', static_url_path='')

cost_re = re.compile('\[(\d+)\]')

def to_symbols(text):
    text = text.replace('[T]', '<img src="/assets/tap.svg" class="symbol">')
    text = cost_re.sub(r'<span class="cost-symbol">\1</span>', text)
    return text

def process_card(card):
    return {
        'name': card.name,
        'cost': to_symbols(card.cost),
        'color': card.color,
        'image': card.image,
        'type': card.type.name,
        'rarity': card.rarity.name,
        'quote': card.quote,
        'attack': getattr(card, 'attack', None),
        'defense': getattr(card, 'defense', None),
        'abilities': [to_symbols(str(a)) for a in card.abilities]
    }

@app.route('/')
def index():
    cards = [process_card(generate_card()) for _ in range(30)]
    return render_template('cards.html', cards=cards)
