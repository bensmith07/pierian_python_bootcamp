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
        
        # if self.rank == 'A':
        #     self.value = None
        #     while True:
        #         choice = input('Ace high or low? (H or L): ').upper()
        #         if choice == 'H':
        #             self.value = 14
        #             break
        #         elif choice == 'L':
        #             self.value = 1
        #             break
        # else:
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
    
    def deal(self, n):
        dealt_cards = []
        for i in range(n):
            dealt_cards.append(self.cards.pop())
        return dealt_cards
    
class Player:

    def __init__(self, name, bankroll):
        self.name = name
        self.bankroll = float(bankroll)

    def bet(self, amount):
        if amount < self.bankroll:
            print(f'You do not have enough to bet ${amount}')
        else:
            self.bankroll -= amount

    def win(self, amount):
        self.bankroll += amount

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




# GAME SETUP

player_name = input("Enter the player's name: ")
player_bankroll = input("Enter a starting bankroll amount: ")
player = Player(name=player_name, bankroll=player_bankroll)

deck = Deck(n_decks=6)
deck.shuffle()

game_on = True
while game_on:

    print(f'{player.name}\'s turn\n---------------------')
    player_cards = []
    cards = deck.deal(2)
    display_cards(cards)
    for card in cards:
        if card.rank == 'A':
            card.set_value(input('ACE HIGH OR LOW? (H/L)'))
    player_cards += cards
    player_total = sum([card.value for card in player_cards])
    display_total(player_cards)

    if player_total < 21:
        choice = input('Hit (H) or Stay (S)? ')[0].upper()
        while choice == 'H' and player_total < 21:
            card = deck.deal(1)
            if card.rank == 'A':
                card.set_value(input('ACE HIGH OR LOW? (H/L)'))
            player_cards += card
            player_total = sum([card.value for card in player_cards])
            display_cards(player_cards)
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
    elif player.state == 'bust':
        print(f'BUST! {player.name} LOSES!')
    elif player.state == 'stand':

        # dealer's turn
        print(f'Dealer\'s turn\n---------------------')
        dealer_cards = []
        cards = deck.deal(2)            
        # TODO: logic for ACES
        dealer_cards += cards
        dealer_total = sum([card.value for card in dealer_cards])
        display_cards(dealer_cards)
        display_total(dealer_cards)

        while dealer_total < 17:
            dealer_cards += deck.deal(1)
            dealer_total = sum([card.value for card in player_cards])
            display_cards(player_cards)
            display_total(dealer_cards)
        if dealer_total > 21:
            print(f'DEALER BUSTS! {player.name} WINS!')
        else:
            # compare 
            if player_total > dealer_total:
                print(f'{player.name} WINS!')
            elif player_total < dealer_total:
                print(f'{player.name} LOSES!')
            else:
                print('PUSH!')
            
    break