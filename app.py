from flask import Flask, render_template, request
from poker_odds import calculate_odds, Card

app = Flask(__name__)

SUIT_SHAPES = {'H': '♥', 'D': '♦', 'C': '♣', 'S': '♠', 'h': '♥', 'd': '♦', 'c': '♣', 's': '♠'}

def card_str_shape(card):
    return f"{card.rank}{SUIT_SHAPES.get(card.suit, card.suit)}"

@app.route('/', methods=['GET', 'POST'])
def index():
    odds = None
    selected = {}
    input_summary = None
    if request.method == 'POST':
        # Your hand
        your_hand = [
            Card(request.form['your_hand_rank1'], request.form['your_hand_suit1'].upper()),
            Card(request.form['your_hand_rank2'], request.form['your_hand_suit2'].upper())
        ]
        # Opponent hand
        opponent_hand = [
            Card(request.form['opponent_hand_rank1'], request.form['opponent_hand_suit1'].upper()),
            Card(request.form['opponent_hand_rank2'], request.form['opponent_hand_suit2'].upper())
        ]
        # Board cards (optional, up to 5)
        board = []
        for i in range(1, 6):
            rank = request.form.get(f'board_rank{i}')
            suit = request.form.get(f'board_suit{i}')
            if rank and suit and rank != '' and suit != '':
                board.append(Card(rank, suit.upper()))
        odds = calculate_odds(your_hand, [opponent_hand], board)
        # Prepare input summary for display (with suit shapes)
        input_summary = {
            'your_hand': [card_str_shape(c) for c in your_hand],
            'opponent_hand': [card_str_shape(c) for c in opponent_hand],
            'board': [card_str_shape(c) for c in board]
        }
        # Keep selections for sticky form
        selected = {
            'your_hand_rank1': request.form['your_hand_rank1'],
            'your_hand_suit1': request.form['your_hand_suit1'],
            'your_hand_rank2': request.form['your_hand_rank2'],
            'your_hand_suit2': request.form['your_hand_suit2'],
            'opponent_hand_rank1': request.form['opponent_hand_rank1'],
            'opponent_hand_suit1': request.form['opponent_hand_suit1'],
            'opponent_hand_rank2': request.form['opponent_hand_rank2'],
            'opponent_hand_suit2': request.form['opponent_hand_suit2'],
        }
        for i in range(1, 6):
            selected[f'board_rank{i}'] = request.form.get(f'board_rank{i}', '')
            selected[f'board_suit{i}'] = request.form.get(f'board_suit{i}', '')
    return render_template('index.html', odds=odds, selected=selected, input_summary=input_summary)

if __name__ == '__main__':
    app.run(debug=True)