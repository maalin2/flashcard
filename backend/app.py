from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flashcards.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Deck(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    cards = db.relationship('Card', backref='deck', lazy=True)

    def __repr__(self):
        return f'<Deck {self.name}>'

class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(255), nullable=False)
    answer = db.Column(db.String(255), nullable=False)
    deck_id = db.Column(db.Integer, db.ForeignKey('deck.id'), nullable=False)

    def __repr__(self):
        return f'<Card {self.question}>'

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return 'hello world'

@app.route('/deck', methods=['POST'])
def create_deck():
    deck_name = request.json.get('name')
    if deck_name:
        new_deck = Deck(name=deck_name)
        db.session.add(new_deck)
        db.session.commit()
        return jsonify({'message': 'Deck created', 'deck': deck_name}), 201
    else:
        return jsonify({'error': 'deck name required!'}), 400

@app.route('/deck/<int:deck_id>/card', methods=['POST'])
def create_card(deck_id):
    deck = Deck.query.get_or_404(deck_id)
    question = request.json.get('question')
    ans = request.json.get('answer')

    if question and ans:
        new_card = Card(question=question, answer=ans, deck_id=deck.id)
        db.session.add(new_card)
        db.session.commit()
        return jsonify({'message': 'card created', 'card': {'question': question, 'answer': ans}}), 201
    else:
        return jsonify({'error': 'question and answer required'}), 400

@app.route('/decks', methods=['GET'])
def get_decks():
    decks = Deck.query.all()
    return jsonify({'decks': [{'id': deck.id, 'name': deck.name} for deck in decks]})

@app.route('/deck/<int:deck_id>/cards', methods=['GET'])
def get_cards(deck_id):
    deck = Deck.query.get_or_404(deck_id)
    cards = Card.query.filter_by(deck_id = deck.id).all()
    return jsonify({'cards': [{'id': card.id, 'question': card.question, 'answer': card.answer} for card in cards]})

if __name__ == '__main__':
    app.run(debug=True)
