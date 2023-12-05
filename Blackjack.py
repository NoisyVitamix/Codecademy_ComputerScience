### Codecademy CS101 Portfolio Project: Blackjack

import random # For drawing cards randomly

class Player:
    def __init__(self):
        self.name = input("What is your name? ")
        self.added_money = 0
        self.current_money = 0
        self.add_fund()
        self.earning = self.current_money - self.added_money
        self.still_playing = True

    def add_fund(self):
        amount = input("How much money would you like to add?")
        while(type(amount) != "int"):
            amount = input("Please re-Write numbers only, in integers.")
        self.added_money += amount
        self.current_money += amount
    
    def __repr__(self):
        return "{name} has {total_money} money total. They have added {added_money} so far. They have earned {earning} so far from playing.".format(name = self.name, total_money = self.current_money, added_money = self.added_money, earning = self.earning)
      
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
