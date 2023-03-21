import os
import random

class deck:
    # initalize deck class (add 52 cards to deck)
    def __init__(self):
        # Empty lists to store used and unused cards
        self.unused_cards = [ ]
        self.used_cards = [ ]
        
        # Four potential suits
        suits = ['S', 'H', 'D', 'C']
        
        # Look through 14 possible number/face cards with 4 different suits
        # Add each card to unused_cards
        for i in range(1,14):
            for suit in suits:
                if i == 1:
                    self.unused_cards.append('A' + suit)
                elif i == 11:
                    self.unused_cards.append('J' + suit)
                elif i == 12:
                    self.unused_cards.append('Q' + suit)
                elif i == 13:
                    self.unused_cards.append('K' + suit)
                else:
                    self.unused_cards.append(str(i) + suit) 
    
    # return a random card and place card in used pile
    def get_card(self):
        card = random.choice(self.unused_cards)
        self.unused_cards.remove(card)
        self.used_cards.append(card)
        return card
    
    # return all cards from used to unused (shuffling)
    def shuffle(self):
        print(">> Shuffling...")
        for x in self.used_cards:
            self.unused_cards.append(x)
        self.used_cards = [ ]

class blackjack_hand:
    # initalize the hand (two cards and evaluate value)
    def __init__(self, card_1, card_2):
        self.hand = [card_1, card_2]
        self.value = self.evaluate()
    
    # add a new card from the deck (re-evaluate value)
    def add_card(self, new_card):
        self.hand.append(new_card)
        self.value = self.evaluate()
    
    # evaluate the value(s) of a hand
    def evaluate(self):
        # two elements for potential double values of Aces
        value = [0, 0]
        numAces = 0
        
        # for each card in hand
        for card in self.hand:
            # if the card is an ace
            if card[0] == 'A':
                # add one to the first value
                value[0] += 1
                # add 11 to the second value (if there are no previous aces)
                if numAces == 0:
                    value[1] += 11
                # add 1 to the second value (if not first ace)
                else:
                    value[1] += 1
                numAces += 1
            # if face card, add 10 to both
            elif card[0] in ['K', 'Q', 'J']:
                value[0] += 10
                value[1] += 10
            # if number card, add number to both
            else:
                value[0] += int(card[0:len(card)-1])
                value[1] += int(card[0:len(card)-1])      
        return value
    
    # determines the best value for the hand
    def best_value(self):
        if self.value[1] <= 21:
            return self.value[1]
        else:
            return self.value[0]
    
    # prints out the hand for the user
    def display(self):
        outputStr = 'Hand: '
        
        # append the card names
        for card in self.hand:
            outputStr += card
            if card != self.hand[-1]:
                outputStr += ', '
        
        # determines whether to show two values or one
        if self.ace_in_hand() and self.value[1] <= 21:
            outputStr += ' (Total: ' + str(self.value[0]) + ' or ' + str(self.value[1]) + ')'
        else:
            outputStr += ' (Total: ' + str(self.value[0]) + ')'
        
        return outputStr
    
    # determines if there is an ace in the hand
    def ace_in_hand(self):
        if self.value[0] != self.value[1]:
            return True
        else:
            return False

class blackjack_game:
    # Rules for game are found here: http://en.wikipedia.org/wiki/Blackjack
    # initialize with a clean deck, money set to $1000, and other variables
    def __init__(self):
        self.deck = deck()
        self.user_hand = [ ]
        self.comp_hand = [ ]
        self.money = 1000.00
        self.bet = 0
        self.count = 0
        self.results = [ ]
        self.rounds_played = 0
        
    def play(self, count_cards=False):
        print(">> Welcome to Blackjack!")
        
        playAgain = ''
        while len(playAgain) == 0 or playAgain[0].lower() != 'n':
            self.rounds_played += 1
            self.results = [ ]
            if len(self.deck.unused_cards) < 15:
                self.deck.shuffle()
                self.count = 0
                
            self.make_bet(count_cards)
            self.deal()
            self.user_play(self.user_hand)
            self.comp_play()
            self.result()
            
            if self.money <= 0:
                print(">> You're out of money!")
                break
            
            playAgain = input("Play Again? ")
            os.system('clear')
        
        print(">> You played " + str(self.rounds_played) + " rounds and")
        print(">> You finished the game with $" + str(self.money))
        
        
    def make_bet(self, count_cards):
        if str(self.money)[len(str(self.money))-3:len(str(self.money))-2] == '.':
            print('>> Money: $' + str(self.money))
        else:
            print('>> Money: $' + str(self.money) + '0')
            
        if count_cards:
            print('>> Count: ' + str(self.count))
            
        bet_input = input("Place your bet: ")
        if bet_input[-1] == "%":
            self.bet = round(float(self.money * (float(bet_input[:-2])/10)),2)
        else:
            self.bet = round(float(eval(bet_input)),2)
        if self.bet > self.money:
            print(">> You bet more than you have. Bet set to $" + str(self.money))
            self.bet = self.money
        
    def deal(self):
        self.user_hand = blackjack_hand(self.deck.get_card(), self.deck.get_card())
        self.comp_hand = blackjack_hand(self.deck.get_card(), self.deck.get_card())    
        
    def user_play(self, hand):
        if hand == self.user_hand:
            hand = self.user_hand
            print('\n>> Dealer has: ' + self.comp_hand.hand[0])
        
        print('>> Your ' + hand.display())
        while hand.value[0] < 21:
            if hand.best_value() == 21:
                break
            
            move = input('Hit or Stay? ' )
            if move.lower() == 'stay':
                break
            elif move.lower() == 'hit':
                hand.add_card(self.deck.get_card())
            elif move.lower() == 'double':
                hand.add_card(self.deck.get_card())
                print('>> Your ' + hand.display())
                self.bet *= 2
                break
            elif self.can_split(hand.hand) and move.lower() == 'split':
                split_a = blackjack_hand(hand.hand[0], self.deck.get_card())
                split_b = blackjack_hand(hand.hand[1], self.deck.get_card())
                print("\n>> Split A:")
                self.user_play(split_a)
                
                print("\n>> Split B:")
                self.user_play(split_b)
                return
            else:
                print('>> Invalid Move. Hitting...')
                self.user_hand.add_card(self.deck.get_card())
            
            print('>> Your ' + hand.display())
            
        
        self.card_count(hand)        
        self.results.append(hand.best_value())
        
    def comp_play(self):
        while self.comp_hand.best_value() < 17:
            self.comp_hand.add_card(self.deck.get_card())
        
        self.card_count(self.comp_hand)
        if len(self.results) > 1:
            print('\n>> Dealer ' + self.comp_hand.display())
            
    def result(self):
        for result in self.results:
            if len(self.results) > 1:
                print(">> Hand Value: " + str(result))
            if result == 21:
                print(">> You got blackjack!")
                self.money += self.bet
            elif result > 21:
                print(">> You busted, sorry.")
                self.money -= self.bet
            elif self.comp_hand.value[0] > 21:
                if len(self.results) == 1:
                    print('\n>> Dealer ' + self.comp_hand.display())
                print(">> The dealer busted, you won!")
                self.money += self.bet
            elif result > self.comp_hand.best_value():
                if len(self.results) == 1:
                    print('\n>> Dealer ' + self.comp_hand.display())
                print(">> You beat the dealer!")
                self.money += self.bet
            elif result == self.comp_hand.best_value():
                if len(self.results) == 1:
                    print('\n>> Dealer ' + self.comp_hand.display())
                print(">> Push...")
            else:
                if len(self.results) == 1:
                    print('\n>> Dealer ' + self.comp_hand.display())
                print(">> The dealer beat you, sorry.")
                self.money -= self.bet
     
    def card_count(self, hand):
        for card in hand.hand:
            if card[0] in ['K', 'Q', 'J', 'A']:
                self.count -= 1
            elif int(card[0:len(card)-1]) <= 6:
                self.count += 1
            elif int(card[0:len(card)-1]) == 10:
                self.count -= 1
                
    def can_split(self, hand):
        if len(hand) != 2:
            return False
        
        if hand[0][0:len(hand[0])-1] in ['K', 'Q', 'J', '10'] and hand[1][0:len(hand[1])-1] in ['K', 'Q', 'J', '10']:
            return True
        elif hand[0][0:len(hand[0])-1] == hand[1][0:len(hand[1])-1]:
            return True
        else:
            return False

gameTest = blackjack_game()
gameTest.play(True)