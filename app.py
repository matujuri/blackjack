from flask import Flask, request, render_template_string, session, redirect, url_for, send_from_directory
from flask_babel import Babel, _
from main import deal_card, calculate_score, compare
from base_template import base_template
from art import logo

app = Flask(__name__)
app.secret_key = 'your_secret_key'

babel = Babel(
    app, locale_selector=lambda: session.get('language', request.accept_languages.best_match(['en', 'ja', 'zh'])))

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


def get_selected_language():
    if 'language' in session:
        # 'language' key exists in the session dictionary
        return session['language']
    else:
        # 'language' key doesn't exist in the session dictionary
        return request.accept_languages.best_match(
            ['en', 'ja', 'zh'])


@app.route('/change_language')
def change_language():
    selected_language = request.args.get('lang')
    session['language'] = selected_language
    return redirect(url_for('index'))


@app.route('/static/images/background.jpeg')
def background():
    # Serve the background image with a cache-control header
    # Cache for 1 hour
    return send_from_directory('static', 'images/background.jpeg', max_age=3600)


@app.route('/')
def index():
    selected_language = get_selected_language()
    content = f'<a href="/play">{_("Start Game")}</a>'
    return render_template_string(base_template.replace('{{ logo }}', logo).replace('{{ content }}', content), selected_language=selected_language)


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

    dealer_first_card = _("Dealer's First Card")
    game_template = f'''
    <p><strong>{_('Your Cards')}: {game_state['player_cards']} ({_('Score')}: {game_state['player_score']})</strong></p>
    <p><strong>{dealer_first_card}: {game_state['dealer_cards'][0]}</strong></p>
    <form method="post">
        <button name="action" value="hit">{_('Hit')}</button>
        <button name="action" value="stand">{_('Stand')}</button>
    </form>
    '''
    dealer_final_hand = _("Dealer's final hand")
    end_game_template = f'''
    <p><strong>{_('Your final hand')}: {game_state['player_cards']} ({_('Score')}: {game_state['player_score']})</strong></p>
    <p><strong>{_(dealer_final_hand)}: {game_state['dealer_cards']} ({_('Score')}: {game_state['dealer_score']})</strong></p>
    <p><strong>{_('Result')}: {game_state['result']}</strong></p>
    <a href="/play">{_('Play Again')}</a>
    '''

    selected_language = get_selected_language()

    if game_state['game_over']:
        return render_template_string(base_template.replace('{{ logo }}', logo).replace('{{ content }}', end_game_template), selected_language=selected_language)
    else:
        return render_template_string(base_template.replace('{{ logo }}', logo).replace('{{ content }}', game_template), selected_language=selected_language)


if __name__ == '__main__':
    app.run(debug=True)
