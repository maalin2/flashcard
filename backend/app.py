from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from gpt import prompt_gemini

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flashcards.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Deck(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    cards = db.relationship('Card', backref='deck', cascade="all, delete-orphan")

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


@app.route('/deck/<int:deck_id>', methods=['DELETE'])
def delete_deck(deck_id):
    deck = Deck.query.get_or_404(deck_id)
    if deck:
        db.session.delete(deck)
        db.session.commit()
        return jsonify({'message': f'deck with id {deck_id} deleted'}), 200
    else:
        return jsonify({'error': 'deck not found'}), 404

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

@app.route('/deck/<int:deck_id>/card/<int:card_id>', methods=['DELETE'])
def delete_card(deck_id, card_id):
    deck = Deck.query.get_or_404(deck_id)
    card = Card.query.filter_by(id=card_id, deck_id=deck_id).first()
    if not card:
        return jsonify({'error': 'card not found'}), 404

    db.session.delete(card)
    db.session.commit()

    return jsonify({'message': f'card with id {card_id} deleted from deck {deck_id}'}), 200

@app.route('/decks', methods=['GET'])
def get_decks():
    decks = Deck.query.all()
    return jsonify({'decks': [{'id': deck.id, 'name': deck.name} for deck in decks]})

@app.route('/gpt', methods=['POST'])
def gpt():
    question = request.json.get('question')
    resp = request.json.get('resp')
    e_resp = request.json.get('e_resp')

    t = prompt_gemini(question, resp, resp)
    return jsonify({'response': t}), 200

@app.route('/deck/<int:deck_id>/cards', methods=['GET'])
def get_cards(deck_id):
    deck = Deck.query.get_or_404(deck_id)
    cards = Card.query.filter_by(deck_id = deck.id).all()
    return jsonify({'cards': [{'id': card.id, 'question': card.question, 'answer': card.answer} for card in cards]})

if __name__ == '__main__':
    app.run(debug=True)
