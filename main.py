from art import logo
import random
import os


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
        return "You went over. You lose 😤"

    if player_score == dealer_score:
        return "Draw 🙃"
    elif dealer_score == 0:
        return "Lose, opponent has Blackjack 😱"
    elif player_score == 0:
        return "Win with a Blackjack 😎"
    elif player_score > 21:
        return "You went over. You lose 😭"
    elif dealer_score > 21:
        return "Opponent went over. You win 😁"
    elif player_score > dealer_score:
        return "You win 😃"
    else:
        return "You lose 😤"


cards = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]


def play_game():

    player_cards = []
    dealer_cards = []
    game_over = False

    print(logo)

    # Dealing initial cards
    player_cards.append(deal_card())
    player_cards.append(deal_card())
    dealer_cards.append(deal_card())
    dealer_cards.append(deal_card())

    while not game_over:

        # calculate the score
        player_score = calculate_score(player_cards)
        dealer_score = calculate_score(dealer_cards)

        # print out current state
        print(f"  Your cards: {player_cards}, current score: {player_score}")
        print(f"  Dealer's first card: {dealer_cards[0]}")

        # check if blackjack or burst. if so, game over, if not, ask player if need another card.
        if player_score == 0 or dealer_score == 0 or player_score > 21:
            game_over = True
        else:
            want_another_card = input(
                "Press 'y' to get another card, or press 'n' to pass. ") == "y"
            if want_another_card:
                player_cards.append(deal_card())
            else:
                game_over = True

        # Dealer's turn to play. If dealer score < 17, keep playing.
        while dealer_score < 17:
            dealer_cards.append(deal_card())
            dealer_score = calculate_score(dealer_cards)

    # print out the final results
    print(f"Your final hand: {player_cards}, final score: {player_score}")
    print(f"Dealer's final hand: {dealer_cards}, final score: {dealer_score}")
    print(compare(player_score, dealer_score))


# while input("do you want to play black jack? 'yes' or 'no' ").lower() == "yes":
#     os.system('clear')
#     play_game()
