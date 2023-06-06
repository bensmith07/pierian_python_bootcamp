import random

suits = ('hearts', 'diamonds', 'spades', 'clubs')
ranks = ('2', '3', '4', '5', '6', '7', '8', 
         '9', '10', 'J', 'Q', 'K', 'A')

values_dct = {
    '2': 2,
    '3': 3, 
    '4': 4,
    '5': 5,
    '6': 6,
    '7': 7,
    '8': 8,
    '9': 9,
    '10': 10,
    'J': 10,
    'Q': 10,
    'K': 10,
    'A': 0, # to be set when dealt
}

class Card:
    def __init__(self, rank, suit):

        self.rank = str(rank).upper()
        self.suit = suit.upper()
        self.value = int(values_dct[self.rank])
        
    def set_value(self, choice):
        if choice.upper() == 'H': # high
            self.value = 11
        elif choice.upper() == 'L': # low
            self.value = 1
        else:
            raise ValueError
        
class Deck:
    
    def __init__(self, n_decks):
        self.cards = []
        for i in range(n_decks):
            for suit in suits:
                for rank in ranks:
                    self.cards.append(
                        Card(rank=rank, suit=suit)
                    )

    def shuffle(self):
        random.shuffle(self.cards)

    def deal_one(self):
        return self.cards.pop()
    
class Player:

    def __init__(self, name, bankroll):
        self.name = name
        self.bankroll = float(bankroll)

    def lose(self, amount):
        self.bankroll -= amount
        print(f'BANKROLL: {self.bankroll}')

    def win(self, amount):
        self.bankroll += amount
        print(f'BANKROLL: {self.bankroll}')

    def set_state(self, state):
        '''
        state: stand, blackjack, bust
        '''
        self.state = state

def display_cards(card_lst):

    str = 'CARDS: '
    for i, card in enumerate(card_lst):
        str += card.rank
        if i != len(card_lst):
            str += '|'
    print(str)

def display_total(card_lst):
    print(f'TOTAL: {sum(card.value for card in card_lst)}')
    print('\n')

deck = Deck(n_decks=6)

# GAME SETUP

player_name = input("Enter the player's name: ")
player_bankroll = input("Enter a starting bankroll amount: ")
player = Player(name=player_name, bankroll=player_bankroll)

deck.shuffle()

game_on = 'Y'
while game_on == 'Y':

    print(f'{player.name}\'s turn\n---------------------')
    print(f'BANKROLL: {player.bankroll}')
    bet_amount = float(input('Enter your bet amount: '))
    while bet_amount > player.bankroll:
        bet_amount = float(input(f'You do not have enough to bet {bet_amount}. Enter a lower amount: '))
    player_cards = []
    player_cards.append(deck.deal_one())
    player_cards.append(deck.deal_one())
    display_cards(player_cards)
    for card in player_cards:
        if card.rank == 'A':
            card.set_value(input('ACE HIGH OR LOW? (H/L)'))
    player_total = sum([card.value for card in player_cards])
    display_total(player_cards)

    if player_total < 21:
        choice = input('Hit (H) or Stay (S)? ')[0].upper()
        while choice == 'H' and player_total < 21:
            player_cards.append(deck.deal_one())
            display_cards(player_cards)
            if player_cards[-1].rank == 'A':
                card.set_value(input('ACE HIGH OR LOW? (H/L)'))
            player_total = sum([card.value for card in player_cards])
            display_total(player_cards)
            if player_total < 21:
                choice = input('Hit (H) or Stay (S)? ')[0].upper()
                if choice == 'S':
                    player.set_state('stand')
                    break
            elif player_total == 21:
                player.set_state('blackjack')
                break
            elif player_total > 21:
                player.set_state('bust')
                break
        if choice == 'S':
            player.set_state('stand')
    elif player_total == 21:
        player.set_state('blackjack')
        break
    elif player_total > 21:
        player.set_state('bust')
        break
    
    # check game state
    if player.state == 'blackjack':
        print(f'BLACKJACK! {player.name} WINS!')
        player.win(bet_amount)
    elif player.state == 'bust':
        print(f'BUST! {player.name} LOSES!')
        player.lose(bet_amount)
    elif player.state == 'stand':

        # dealer's turn
        print(f'Dealer\'s turn\n---------------------')
        dealer_cards = []
        dealer_cards.append(deck.deal_one())
        dealer_cards.append(deck.deal_one())
        display_cards(dealer_cards)
        for card in dealer_cards:
            if card.rank == 'A':
                card.set_value(input('ACE HIGH OR LOW? (H/L)'))
        dealer_total = sum([card.value for card in dealer_cards])
        display_total(dealer_cards)

        while dealer_total < 17:
            dealer_cards.append(deck.deal_one())
            display_cards(dealer_cards)
            if dealer_cards[-1].rank == 'A':
                card.set_value(input('ACE HIGH OR LOW? (H/L)'))
            dealer_total = sum([card.value for card in dealer_cards])
            display_total(dealer_cards)
        if dealer_total > 21:
            print(f'DEALER BUSTS! {player.name} WINS!')
            player.win(bet_amount)
        else:
            # compare 
            if player_total > dealer_total:
                print(f'{player.name} WINS!')
                player.win(bet_amount)
            elif player_total < dealer_total:
                print(f'{player.name} LOSES!')
                print(player.lose(bet_amount))
            else:
                print('PUSH!')
    if player.bankroll > 0:
        game_on = input('Play again (Y/N)?').upper()
    else:
        break
