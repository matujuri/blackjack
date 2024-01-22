from flask import Flask, request, render_template_string, session
from flask_babel import Babel, _
from main import deal_card, calculate_score, compare
from base_template import base_template
from art import logo

app = Flask(__name__)
app.secret_key = 'your_secret_key'

babel = Babel(
    app, locale_selector=lambda: request.accept_languages.best_match(['en', 'ja', 'zh']))

cards = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]


def initialize_game():
    player_cards = [deal_card(), deal_card()]
    dealer_cards = [deal_card(), deal_card()]
    return {
        'player_cards': player_cards,
        'dealer_cards': dealer_cards,
        'player_score': calculate_score(player_cards),
        'dealer_score': calculate_score(dealer_cards),  # ここで初期化
        'game_over': False,
        'result': None
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
    content = f'<a href="/play">{_("Start Game")}</a>'
    return base_template.replace('{{ logo }}', logo).replace('{{ content }}', content)


@app.route('/play', methods=['GET', 'POST'])
def play():
    if 'game_state' not in session:
        session['game_state'] = initialize_game()
    game_state = session['game_state']

    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'hit':
            game_state['player_cards'].append(deal_card())
            update_game_state(game_state)
        elif action == 'stand':
            game_state['game_over'] = True
            update_game_state(game_state)

        session['game_state'] = game_state
    else:
        session['game_state'] = initialize_game()
        game_state = session['game_state']

    game_template = f'''
    <p>{_('Your Cards')}: {game_state['player_cards']} ({_('Score')}: {game_state['player_score']})</p>
    <p>{_('Dealer\'s First Card')}: {game_state['dealer_cards'][0]}</p>
    <form method="post">
        <button name="action" value="hit">{_('Hit')}</button>
        <button name="action" value="stand">{_('Stand')}</button>
    </form>
    '''

    end_game_template = f'''
    <p>{_('Your final hand')}: {game_state['player_cards']} ({_('Score')}: {game_state['player_score']})</p>
    <p>{_('Dealer\'s final hand')}: {game_state['dealer_cards']} ({_('Score')}: {game_state['dealer_score']})</p>
    <p>{_('Result')}: {game_state['result']}</p>
    <a href="/play">{_('Play Again')}</a>
    '''

    if game_state['game_over']:
        return render_template_string(base_template.replace('{{ logo }}', logo).replace('{{ content }}', end_game_template))
    else:
        return render_template_string(base_template.replace('{{ logo }}', logo).replace('{{ content }}', game_template))


if __name__ == '__main__':
    app.run(debug=True)
