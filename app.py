from flask import Flask, request, render_template_string, session
import random
from art import logo
from main import deal_card, calculate_score, compare

app = Flask(__name__)
app.secret_key = 'your_secret_key'

cards = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]


def initialize_game():
    player_cards = [deal_card(), deal_card()]
    dealer_cards = [deal_card(), deal_card()]
    return {
        'player_cards': player_cards,
        'dealer_cards': dealer_cards,
        'player_score': calculate_score(player_cards),
        'game_over': False
    }


def update_game_state(game_state):
    player_score = calculate_score(game_state['player_cards'])
    dealer_score = calculate_score(game_state['dealer_cards'])

    if player_score == 0 or dealer_score == 0 or player_score > 21:
        game_state['game_over'] = True
    else:
        while dealer_score < 17:
            game_state['dealer_cards'].append(deal_card())
            dealer_score = calculate_score(game_state['dealer_cards'])

    game_state['player_score'] = player_score
    game_state['dealer_score'] = dealer_score

    if game_state['game_over']:
        game_state['result'] = compare(player_score, dealer_score)


@app.route('/')
def index():
    return f'<pre>{logo}</pre><br><a href="/play">Start Game</a>'


@app.route('/play', methods=['GET', 'POST'])
def play():
    if request.method == 'POST':
        action = request.form.get('action')

        game_state = session.get('game_state', None)
        if not game_state:
            game_state = initialize_game()

        if action == 'hit':
            game_state['player_cards'].append(deal_card())
            update_game_state(game_state)
        elif action == 'stand':
            game_state['game_over'] = True
            update_game_state(game_state)

        session['game_state'] = game_state

        if game_state['game_over']:
            return render_template_string(end_game_template, game_state=game_state, logo=logo)
        else:
            return render_template_string(game_template, game_state=game_state, logo=logo)
    else:
        session['game_state'] = initialize_game()
        return render_template_string(game_template, game_state=session['game_state'], logo=logo)


game_template = '''
<html>
<body>
    <!-- Game interface -->
    <pre>{{ logo }}</pre>
    <p>Your Cards: {{ game_state.player_cards }} (Score: {{ game_state.player_score }})</p>
    <p>Dealer's First Card: {{ game_state.dealer_cards[0] }}</p>
    <form method="post">
        <button name="action" value="hit">Hit</button>
        <button name="action" value="stand">Stand</button>
    </form>
</body>
</html>
'''

end_game_template = '''
<html>
<body>
    <!-- Game over interface -->
    <pre>{{ logo }}</pre>
    <p>Your final hand: {{ game_state.player_cards }} (Score: {{ game_state.player_score }})</p>
    <p>Dealer's final hand: {{ game_state.dealer_cards }} (Score: {{ game_state.dealer_score }})</p>
    <p>Result: {{ game_state.result }}</p>
    <a href="/play">Play Again</a>
</body>
</html>
'''

if __name__ == '__main__':
    app.run(debug=True)
