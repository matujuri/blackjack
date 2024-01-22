from flask_babel import _
from art import logo
import random

cards = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]


def deal_card():
    """add a card to a player's hand"""
    return random.choice(cards)


def calculate_score(cards):
    """calculate the score of a player's hand"""
    # initial check for blackjack
    if sum(cards) == 21 and len(cards) == 2:
        return 0

    # Adjusting for Ace value
    if sum(cards) > 21 and 11 in cards:
        cards.remove(11)
        cards.append(1)

    return sum(cards)


def compare(player_score, dealer_score):
    """check final scores and declare winner"""
    if player_score > 21 and dealer_score > 21:
        return _("You went over. You lose") + " 😤"

    if player_score == dealer_score:
        return _("Draw") + " 🙃"
    elif dealer_score == 0:
        return _("Lose, opponent has Blackjack") + " 😱"
    elif player_score == 0:
        return _("Win with a Blackjack") + " 😎"
    elif player_score > 21:
        return _("You went over. You lose") + " 😭"
    elif dealer_score > 21:
        return _("Opponent went over. You win") + " 😁"
    elif player_score > dealer_score:
        return _("You win") + " 😃"
    else:
        return _("You lose") + " 😤"
