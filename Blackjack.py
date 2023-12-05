### Codecademy CS101 Portfolio Project: Blackjack

import random # For drawing cards randomly

class Player:
    def __init__(self):
        self.name = input("What is your name? ")
        self.added_money = 0
        self.current_money = 0
        self.earning = self.current_money - self.added_money
        self.add_fund()
        self.still_playing = True

    def add_fund(self):
        amount = input("How much money would you like to add? ")
        while True:
            try:
                self.added_money += int(amount)
                self.current_money += int(amount)
                break
            except ValueError:
                amount = input("Please re-Write numbers only, in integers: ")
        print(self)
    
    def __repr__(self):
        return "{name} has {total_money} fund total. They have added {added_money} fund so far. They have earned {earning} fund so far from playing.".format(name = self.name, total_money = self.current_money, added_money = self.added_money, earning = self.earning)
      
class Deck:
    def __init__(self):
        full_deck =[]
        deck_faces = ["Dia", "Clb", "Hrt", "Spd"]
        deck_numbers = ["A", 2, 3, 4, 5, 6, 7, 8, 9, 10, "J", "Q", "K"]
        for faces in deck_faces:
            for numbers in deck_numbers:
                full_deck.append(str(numbers)+"-"+faces)
        self.current_deck = full_deck

    def __repr__(self):
        return str(self.current_deck)

class Playing:
    def __init__(self, player):
        self.player = player
        self.playing_deck = Deck()
        print("We are starting a new round! {player} has {fund} as their fund currently.\n".format(player = self.player.name, fund = self.player.current_money))
        if self.player.current_money <= 0:
            print("You don't have sufficient funds! You currently owe {money} to the Casino. Please add more fund to play!\n".format(money = self.player.current_money * -1))
        want_to_add_money = input("Would you like to add more fund? (y/n) ")
        want_to_add_money.lower()
        if want_to_add_money == "y":
            self.player.add_fund()
        self.casino_hand = []
        self.player_hand = []
        self.not_done_betting = True
    
    def deal_cards(self):
        dealing_index = random.randrange(0, len(self.playing_deck.current_deck))
        dealt_card = self.playing_deck.current_deck.pop(dealing_index)
        return dealt_card

    def betting_round(self):
        
        pass
        
    def play_game(self):
        print("Now we deal the cards.")
        self.player_hand.append(self.deal_cards())
        self.casino_hand.append(self.deal_cards())
        self.player_hand.append(self.deal_cards())
        self.casino_hand.append(self.deal_cards())
        
        print('''
        Here is the dealer's hand: {casino_first_card}, HIDDEN
        Here is your hand: {player_first_card}, {player_second_card}
        '''.format(casino_first_card = self.casino_hand[0], player_first_card = self.player_hand[0], player_second_card = self.player_hand[1]))

        # while(self.not_done_betting):
            # pass
        
        self.end_round()

    def end_round(self):
        continue_game = input("Would you like to continue playing? (y/n) ")
        continue_game.lower()
        if continue_game == "n":
            self.player.still_playing = False



#script for playing
print("Welcome to Blackjack Casino! Here you can play a simple Blackjack game. Hope you will enjoy!")

player1 = Player()

while(player1.still_playing):
    thisround = Playing(player1)
    thisround.play_game()

print("Thank you for playing, {player}! Hope you had fun!".format(player = player1.name))