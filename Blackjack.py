### Codecademy CS101 Portfolio Project: Blackjack

import random # For drawing cards randomly

# Player class: determines the player name & funds. Have method to add fund.
class Player:
    def __init__(self):
        self.name = input("\nWhat is your name? ")
        self.added_money = 0
        self.current_money = 0
        self.add_fund()
        self.still_playing = True # Used for looping the whole playing until specific user input

    def add_fund(self):
        amount = input("\nHow much money would you like to add? ")
        while True:
            try:
                self.added_money += int(amount)
                self.current_money += int(amount)
                break
            except ValueError:
                amount = input("Please re-Write numbers only, in integers: ")
        print(self)
    
    def __repr__(self):
        return "\n{name} has {total_money} fund total. They have added {added_money} fund so far. They have earned {earning} fund so far from playing.".format(name = self.name, total_money = self.current_money, added_money = self.added_money, earning = self.current_money-self.added_money)
      
# Deck class: Create the new deck each time it is called. This mimics deck shuffling for new rounds in real life. Creates the deck as a list for each management for each draw.
class Deck:
    def __init__(self):
        full_deck =[]
        # Trump faces shortened to 3-letter code for easier handling of each card name as a string.
        deck_faces = ["Dia", "Clb", "Hrt", "Spd"] 
        deck_numbers = ["A", 2, 3, 4, 5, 6, 7, 8, 9, 10, "J", "Q", "K"]
        for faces in deck_faces:
            for numbers in deck_numbers:
                full_deck.append(str(numbers)+"-"+faces)
        self.current_deck = full_deck # The instance deck is assigned to the instance variable self.current_deck

    def __repr__(self):
        return str(self.current_deck)

# Playing class: Main body for the actual play of the game. Defined as a class so that the each round of playing can be called as a unique instance.
class Playing:
    def __init__(self, player): # Calls player instance so that the fund changes are attached to the player
        self.player = player
        self.playing_deck = Deck() #Creates a new deck each time play starts
        print("\n** We are starting a new round! {player} has {fund} as their fund currently.\n".format(player = self.player.name, fund = self.player.current_money))
        # Initial fund adding for each round
        want_to_add_money = input("Would you like to add more fund before starting? (y/n) ")
        want_to_add_money.lower()
        if want_to_add_money == "y":
            self.player.add_fund()
        # Handling in case the player "owes" money to the casino or all run out - no bet limit is set by the program for the initial bet so that the player can lose more money than they have by 1) making too large bet or 2) making additional bets by Double Down or Insurance. It does not prevent player from ending a round, but it does prevent the player from starting the new round. Player is also given an option to quit if they lost too much money.
        while self.player.current_money <= 0 and self.player.still_playing:
            quitting = input("\nYou don't have sufficient funds! You currently owe {money} to the Casino. Please add more fund to play! If you would rather quit here, enter 'q'. Otherwise, just hit enter.".format(money = self.player.current_money * -1))
            quitting.lower()
            if quitting == 'q':
                self.player.still_playing = False
            else:
                self.player.add_fund()
        self.dealer_hand = [] # Variable for dealer's hand for this round
        self.player_hand = [] # Variable for player's hand for this round
        self.insurance = 0 # Variable for the Insurance amount for this round
        self.betting = 0 # Variable for the main bet for this round
    
    # Card dealing method for repeated draws, where the deck used is the instance variable of Deck class
    def deal_cards(self):
        dealing_index = random.randrange(0, len(self.playing_deck.current_deck)) #random used to draw
        dealt_card = self.playing_deck.current_deck.pop(dealing_index) # .pop used to id the drawn card and to remove it from the deck
        return dealt_card
    
    # Hand printing method for displaying the current playing table in the terminal. Used repeatedly everytime a card is drawn, so made to a separate method.
    def show_hands(self, show_hole=False):
        # Hole card is handled differently until it's dealer's turn
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
        print('\n')
    
    # Method to calculate the value of each hand. Done repeatedly everytime a card is drawn so made to a separate method.
    def hand_value(self, hand):
        hand_no_faces = []
        hand_in_numbers = [] # List for card values for calculating the sum
        number_of_ace = 0
        # Converting card values in string to numeric values
        for card in hand:
            hand_no_faces.append(card[:-4]) # Separates card value from card faces
        for values in hand_no_faces:
            if values in ["J", "Q", "K"]: # Handling letter values
                hand_in_numbers.append(10)
            elif values == "A": # Separate process to handle "A" which can be either 11 or 1
                hand_in_numbers.append(11)
                number_of_ace += 1
            else:
                hand_in_numbers.append(int(values))
        while(sum(hand_in_numbers) > 21 and number_of_ace >= 1): # Loop for handling multiple "A" in hand
            hand_in_numbers.append(-10)
            number_of_ace -= 1
        return sum(hand_in_numbers)
    
    # Method for dealer's play. By putting it as a method dealer play is bound to each of the player plays and their outcomes. 
    # This could also be done by better categorizing/looping player plays and adding the dealer play afterwards under an if statement. But it might have also made the Player play parts too complex for easier interpretation.
    def dealer_play(self):
        self.show_hands(True) # Since it's the dealer's turn Hole Card is being revealed
        # Following standard Casino rules of Stands at 17 or higher
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

    # Main method for playing each round, to be called by the play_game method. 
    # This is the most massive part of the program, which could be improved with a better scripting. 
    def playing_round(self):
        # Handling Natural Blackjacks either by the player or the dealer. The method is stopped in those cases by return, so that the play does not move further.
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
        # Handling Insurance bet if the dealer's revealed card is an Ace.
        if self.dealer_hand[1][:-4] == "A":
            insurance = input("Dealer has the Ace! Would you like to put an Insurance? Enter a value between 1 to {bet} if you would like to put an Insurance (whole numbers only): ".format(bet=int(self.betting/2)))
            while True:
                try:
                    self.insurance = int(insurance)
                    break
                except ValueError:
                    insurance = input("Wrong value added for the Insurance! It was not a proper value. Please enter a value between 1 to {bet} if you would like to put an Insurance (whole numbers only): ".format(bet=int(self.betting/2)))
            if self.insurance <= 0: # Handling negative Insurance bet
                print("Improper amount of Insurance added! The game will continue without the Insurance.")
                self.insurance = 0
        # Dealer Natural Blackjack
        if self.hand_value(self.dealer_hand) == 21:
            self.show_hands(True)
            print("Natural Blackjack for the dealer! Dealer has won this game!")
            self.player.current_money -= self.betting
            if self.insurance != 0:
                print("Player got paid back for the Insurance!")
                self.player.current_money += 2 * self.insurance
            return
        else: # Nothing happens here if ther was no Insurance bet
            self.player.current_money -= self.insurance

        # Main loop for the play, if no Natural Blackjack has been declared by either Dealer or the player. 
        # It is put in a loop as "Hit" gives the player choices back unless being busted. No ruling of winning is done in this loop, the loop is purely for playing until both dealer & player's hands are finalized.
        while(True):
            player_choice = input("What would you like to do? h=Hit, d=Double Down, s=Stand, u=Surrender: ") # As Split is not being played, there are 4 options for the player
            player_choice.lower()
            while(player_choice not in ['h', 'd', 's', 'u']): # Handling input error
                player_choice = input("Please choose from the options: h=Hit, d=Double Down, s=Stand, u=Surrender: ")
                player_choice.lower()
            # Player choices
            if player_choice == "u": 
                # Player Surrender
                # Handling Surrender by artificially making the player to be busted internally
                self.player_hand.append("K-Sur")
                self.player_hand.append("K-Sur")
                print("Player surrendered!")
                break
            elif player_choice == "d":
                # Player Double Down
                print("Player Doubled Down!")
                self.player_hand.append(self.deal_cards())
                self.betting = 2 * self.betting
                self.show_hands()
                if self.hand_value(self.player_hand) > 21: # When player is busted dealer does not play
                    print("Player got Busted!")
                    self.show_hands(True)
                    break
                elif self.hand_value(self.player_hand) == 21:
                    print("Player got Blackjack!")
                self.dealer_play() # Dealer plays after player is done with Double Down
                break
            elif player_choice == "s":
                # Player Stands
                print("Player Stands!")
                self.dealer_play()
                break
            elif player_choice == "h":
                # Player Hits
                print("Player Hits!")
                self.player_hand.append(self.deal_cards())
                self.show_hands()
                # The loop breaks if the result of Hit is Blackjack or Bust. Otherwise, the loop goes back for the player choice again.
                if self.hand_value(self.player_hand) > 21:
                    print("Player got Busted!")
                    self.show_hands(True)
                    break
                elif self.hand_value(self.player_hand) == 21:
                    print("Player got Blackjack!")
                    self.dealer_play()
                    break
        # Determines the winner after both hands are finalized
        if self.hand_value(self.player_hand) <= 21 and self.hand_value(self.dealer_hand) <= 21:
            if self.hand_value(self.player_hand) > self.hand_value(self.dealer_hand):
                print("Player has won!")
                if self.hand_value(self.player_hand) == 21: # Player Blackjack
                    self.player.current_money += int(1.5 * self.betting)
                else:
                    self.player.current_money += self.betting
            elif self.hand_value(self.player_hand) < self.hand_value(self.dealer_hand):
                print("Dealer has won!")
                self.player.current_money -= self.betting
            else:
                print("It's a tie! This game is Pushed!")
        # Handling Busts
        elif self.hand_value(self.player_hand) > 21:
            self.player.current_money -= self.betting
        elif self.hand_value(self.dealer_hand) > 21:
            self.player.current_money += self.betting
        return # This return is not required as the method ends here, but added for better readability
    
    # Main method to be called for actually playing the game.
    # Other than calling other methods, it sets up the game with the initial bet and the first hand dealing
    def play_game(self):
        if self.player.still_playing == False: # Safety exit in case the method is called despite the user wanted to quit
            return
        betting = input("\nHow much would you like to bet? Enter a value between 1 to {current_money}. ".format(current_money=self.player.current_money))
        while True:
            try:
                self.betting = int(betting)
                break
            except ValueError:
                betting = input("Please re-Write numbers only, in integers: ")
        print("\nNow we deal the first cards.")
        self.player_hand.append(self.deal_cards())
        self.dealer_hand.append(self.deal_cards())
        self.player_hand.append(self.deal_cards())
        self.dealer_hand.append(self.deal_cards())
        
        self.show_hands() # Showing initial hands

        self.playing_round() # Main play
        
        print(self.player) # Desplaying the result of the play in terms of cummulative player earnings

        self.end_game() # Asking if the game should end here

    # Method for ending the game. 
    # As this is a small method and called only once this can actually be combined to the play_game method
    # It was written as a separate method in case more "end game" element is to be added (so that it's easy to manipulate it separately)
    def end_game(self):
        continue_game = input("Would you like to continue playing? (y/n) ")
        continue_game.lower()
        if continue_game == "n":
            self.player.still_playing = False



# Main Script for playing
print("\n*** Welcome to Blackjack Casino! Here you can play a simple Blackjack game. For the simplicity, Splits are not included in this game. Hope you will enjoy! ***")

# Initiating the Player instance
player1 = Player()

# Main loop for playing the game
while(player1.still_playing):
    thisround = Playing(player1)
    thisround.play_game()

# Printing the final result of the playing
print(player1)

# Goodbye message
print("\n*** Thank you for playing, {player}! Hope you had fun! ***".format(player = player1.name))