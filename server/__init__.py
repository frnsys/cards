from flask import Flask, render_template
from cards.generate import generate_card

app = Flask(__name__, static_folder='static', static_url_path='')

@app.route('/')
def index():
    card = generate_card()
    return render_template('card.html', card=card)
