### Codecademy CS101 Portfolio Project: Blackjack

import random # For drawing cards randomly

class Player:
    def __init__(self):
        self.name = input("\nWhat is your name? ")
        self.added_money = 0
        self.current_money = 0
        self.add_fund()
        self.still_playing = True

    def add_fund(self):
        amount = input("\nHow much money would you like to add? ")
        while True:
            try:
                self.added_money += int(amount)
                self.current_money += int(amount)
                break
            except ValueError:
                amount = input("\nPlease re-Write numbers only, in integers: ")
        print(self)
    
    def __repr__(self):
        return "\n{name} has {total_money} fund total. They have added {added_money} fund so far. They have earned {earning} fund so far from playing.".format(name = self.name, total_money = self.current_money, added_money = self.added_money, earning = self.current_money-self.added_money)
      
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
        print("\n\nWe are starting a new round! {player} has {fund} as their fund currently.\n".format(player = self.player.name, fund = self.player.current_money))
        want_to_add_money = input("\nWould you like to add more fund before starting? (y/n) ")
        want_to_add_money.lower()
        if want_to_add_money == "y":
            self.player.add_fund()
        while self.player.current_money <= 0 and self.player.still_playing:
            quitting = input("\nYou don't have sufficient funds! You currently owe {money} to the Casino. Please add more fund to play! If you would rather quit here, enter 'q'. ".format(money = self.player.current_money * -1))
            quitting.lower()
            if quitting == 'q':
                self.player.still_playing = False
            else:
                self.player.add_fund()
        self.dealer_hand = []
        self.player_hand = []
        self.insurance = 0
    
    def deal_cards(self):
        dealing_index = random.randrange(0, len(self.playing_deck.current_deck))
        dealt_card = self.playing_deck.current_deck.pop(dealing_index)
        return dealt_card
    
    def show_hands(self, show_hole=False):
        if show_hole:
            hole_card = self.dealer_hand[0]
        else:
            hole_card = "HIDDEN"
        print("\nHere is the dealer's hand:", end=" ")
        print(hole_card, end=" ")
        for i in range(1, len(self.dealer_hand)):
            print(self.dealer_hand[i], end=" ")
        print("\nHere is your hand:", end=" ")
        for i in range(len(self.player_hand)):
            print(self.player_hand[i], end=" ")
        print('\n\n')
    
    def hand_value(self, hand):
        hand_no_faces = []
        hand_in_numbers = []
        number_of_ace = 0
        for card in hand:
            hand_no_faces.append(card[:-4])
        for values in hand_no_faces:
            if values in ["J", "Q", "K"]:
                hand_in_numbers.append(10)
            elif values == "A":
                hand_in_numbers.append(11)
                number_of_ace += 1
            else:
                hand_in_numbers.append(int(values))
        while(sum(hand_in_numbers) > 21 and number_of_ace >= 1):
            hand_in_numbers.append(-10)
            number_of_ace -= 1
        return sum(hand_in_numbers)
    
    def dealer_play(self):
        self.show_hands(True)
        while(self.hand_value(self.dealer_hand)<= 16):
            print("Dealer Hits!")
            self.dealer_hand.append(self.deal_cards())
            self.show_hands(True)

        if self.hand_value(self.dealer_hand) == 21:
            print("Dealer got Blackjack!")
            return
        elif self.hand_value(self.dealer_hand) > 21:
            print("Dealer got Busted!")
        else:
            print("Dealer Stands!")

    def playing_round(self):
        if self.hand_value(self.player_hand) == 21:
            if self.hand_value(self.dealer_hand) == 21:
                self.show_hands(True)
                print("Both player and the Dealer have natural Blackjack! This game is Pushed!")
                return
            else:
                self.show_hands(True)
                print("Natural Blackjack for the player! Player has won this game!")
                self.player.current_money += 2 * self.betting
                return
        if self.dealer_hand[1][:-4] == "A":
            insurance = input("Dealer has the Ace! Would you like to put an Insurance? Enter a value between 1 to {bet} if you would like to put an Insurance (whole numbers only): ".format(bet=int(self.betting/2)))
            while True:
                try:
                    self.insurance = int(insurance)
                    break
                except ValueError:
                    insurance = input("Wrong value added for the Insurance! It was not a proper value. Please enter a value between 1 to {bet} if you would like to put an Insurance (whole numbers only): ".format(bet=int(self.betting/2)))
            if self.insurance <= 0:
                print("Improper amount of Insurance added! The game will continue without the Insurance.")
                self.insurance = 0
        if self.hand_value(self.dealer_hand) == 21:
            self.show_hands(True)
            print("Natural Blackjack for the dealer! Dealer has won this game!")
            self.player.current_money -= self.betting
            if self.insurance != 0:
                print("Player got paid back for the Insurance!")
                self.player.current_money += 2 * self.insurance
            return
        else:
            self.player.current_money -= self.insurance

        while(True):
            player_choice = input("What would you like to do? h=Hit, d=Double Down, s=Stand, u=Surrender: ")
            player_choice.lower()
            while(player_choice not in ['h', 'd', 's', 'u']):
                player_choice = input("Please choose from the options: h=Hit, d=Double Down, s=Stand, u=Surrender: ")
                player_choice.lower()

            if player_choice == "u":
                self.player.current_money -= self.betting
                print("Player surrendered!")
                break
            elif player_choice == "d":
                print("Player Doubled Down!")
                self.player_hand.append(self.deal_cards())
                self.betting = 2 * self.betting
                self.show_hands()
                if self.hand_value(self.player_hand) > 21:
                    print("Player got Busted!")
                    self.show_hands(True)
                    break
                elif self.hand_value(self.player_hand) == 21:
                    print("Player got Blackjack!")
                self.dealer_play()
                break
            elif player_choice == "s":
                print("Player Stands!")
                self.dealer_play()
                break
            elif player_choice == "h":
                print("Player Hits!")
                self.player_hand.append(self.deal_cards())
                self.show_hands()
                if self.hand_value(self.player_hand) > 21:
                    print("Player got Busted!")
                    self.show_hands(True)
                    break
                elif self.hand_value(self.player_hand) == 21:
                    print("Player got Blackjack!")
                    self.dealer_play()
                    break
        
        if self.hand_value(self.player_hand) <= 21 and self.hand_value(self.dealer_hand) <= 21:
            if self.hand_value(self.player_hand) > self.hand_value(self.dealer_hand):
                print("Player has won!")
                if self.hand_value(self.player_hand) == 21:
                    self.player.current_money += int(1.5 * self.betting)
                else:
                    self.player.current_money += self.betting
            elif self.hand_value(self.player_hand) < self.hand_value(self.dealer_hand):
                print("Dealer has won!")
                self.player.current_money -= self.betting
            else:
                print("It's a tie! This game is Pushed!")
        elif self.hand_value(self.player_hand) > 21:
            self.player.current_money -= self.betting
        elif self.hand_value(self.dealer_hand) > 21:
            self.player.current_money += self.betting
    
        return
        
    def play_game(self):
        if self.player.still_playing == False:
            return
        betting = input("How much would you like to bet? Enter a value between 1 to {current_money}. ".format(current_money=self.player.current_money))
        while True:
            try:
                self.betting = int(betting)
                break
            except ValueError:
                betting = input("Please re-Write numbers only, in integers: ")
        print("Now we deal the cards.")
        self.player_hand.append(self.deal_cards())
        self.dealer_hand.append(self.deal_cards())
        self.player_hand.append(self.deal_cards())
        self.dealer_hand.append(self.deal_cards())
        
        self.show_hands()

        self.playing_round()
        
        print(self.player)

        self.end_game()

    def end_game(self):
        continue_game = input("Would you like to continue playing? (y/n) ")
        continue_game.lower()
        if continue_game == "n":
            self.player.still_playing = False



#script for playing
print("Welcome to Blackjack Casino! Here you can play a simple Blackjack game. For the simplicity, Splits are not included in this game. Hope you will enjoy!")

player1 = Player()

while(player1.still_playing):
    thisround = Playing(player1)
    thisround.play_game()

print(player1)
print("Thank you for playing, {player}! Hope you had fun!".format(player = player1.name))