import random

class Card:
    def __init__(self, rank, suit):
        self._rank = rank
        self._suit = suit
    
    def get_rank(self):
        return self._rank

    def get_suit(self):
        return self._suit

    def to_string(self):
        return f"{self._rank} of {self._suit}s"

class Deck:
    def __init__(self):
        self._ranks = ["Ace", "Deuce", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten", "Jack", "Queen", "King"]
        self._suits = ["Heart", "Spade", "Club", "Diamond"]
        self._deck = None
        self.refill_deck()
        self._card_map = {"Ace": 11, "Deuce": 2, "Three": 3, "Four": 4, "Five": 5, "Six": 6, "Seven": 7, "Eight": 8, "Nine": 9, "Ten": 10,
                          "Jack": 10, "Queen": 10, "King": 10}

    def refill_deck(self):
        self._deck = set()
        for rank in self._ranks:
            for suit in self._suits:
                self._deck.add(Card(rank, suit))

    def pick_card(self):
        res = random.choice(list(self._deck))
        self._deck.remove(res)
        return res

    def get_card_map(self):
        return self._card_map

    def print_deck(self):
        print(self._deck)

class Person:
    def __init__(self, name):
        self._name = name
        self._cards = []
        self._points = 0
    
    def get_name(self):
        return self._name
    
    def get_cards(self):
        return self._cards

    def get_points(self):
        return self._points

    def calibrate_points(self, deck):
        self._points = 0
        card_map = deck.get_card_map()
        for card in self._cards:
            rank = card.get_rank()
            self._points += card_map[rank]
        return self._points

    def add_card(self, card):
        self._cards.append(card)

    def add_points(self, points):
        self._points += points
    
    def reset(self):
        self._cards = []
        self._points = 0
        

class Dealer(Person):
    def __init__(self, name):
        super().__init__(name)
    

class Player(Person):
    def __init__(self, name, balance):
        super().__init__(name)
        self._balance = balance

    def get_balance(self):
        return self._balance

    def set_balance(self, balance):
        self._balance = balance

class Game:
    def __init__(self, player, dealer, deck):
        self._player = player
        self._dealer = dealer
        self._deck = deck
    
    def play(self):
        
        while True:
            print(f"You have {self._player.get_balance()} dollars.")
            print(f"How much would you like to bet {self._player.get_name()}?")
            bet_amt = int(input())

            self._player.reset()
            self._dealer.reset()
            print(f"Dealing cards now...\n")
            self._dealer.add_card(self._deck.pick_card())
            self._dealer.add_card(self._deck.pick_card())
            print(f"The dealer has been dealt two cards. Once of them is {self._dealer.get_cards()[0].to_string()}")
            self._player.add_card(self._deck.pick_card())
            self._player.add_card(self._deck.pick_card())
            print(f"\nYou have been dealt two cards:")
            for card in self._player.get_cards():
                print(f"{card.to_string()}")
            print(f"You now have {self._player.calibrate_points(self._deck)} points")
            while True:
                print(f"Would you like to hit or stay?")
                if input() == "hit":
                    new_card = self._deck.pick_card()
                    self._player.add_card(new_card)
                    print(f"You've picked {new_card.to_string()}.")
                    new_points = self._player.calibrate_points(self._deck)
                    print(f"You now have {new_points} points.")
                    if new_points > 21:
                        print(f"You've busted!")
                        self._player.set_balance(self._player.get_balance() - bet_amt)
                        break
                else:
                    print(f"You now have {self._player.calibrate_points(self._deck)} points")
                    break
            
            if self._player.get_points() > 21:
                continue
            
            while self._dealer.get_points() < 21 and self._dealer.get_points() < self._player.get_points():
                new_card = self._deck.pick_card()
                self._dealer.add_card(new_card)
                new_points = self._dealer.calibrate_points(self._deck)
                print(f"Dealer picked {new_card.to_string()}.")
                if new_points > 21:
                    print(f"Dealer busted with {new_points} points! You win!")
                    self._player.set_balance(self._player.get_balance() + bet_amt)
                    break
                if new_points > self._player.get_points():
                    print(f"Dealer finished with {new_points}. You lose...")
                    self._player.set_balance(self._player.get_balance() - bet_amt)


deck = Deck()
player = Player("Cade", 100)
dealer = Dealer("House")
game = Game(player, dealer, deck)
game.play()
