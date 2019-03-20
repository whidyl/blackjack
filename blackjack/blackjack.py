from random import shuffle

class CardList():
    """Represents a list of playing cards
    Attributes:
        cards (list of :obj:`card`): Represents list of playing cards.
    """
    def __init__ (self, cards = []):
        self.cards = cards
    
    def __getitem__(self, key):
        """ Adds functionality for getting item with syntax: card = myCardList[0]"""
        return self.cards[key]
    
    def __setitem__(self, key, value):
        """ Adds functionality for setting item with syntax: myCardList[0] = Card(...)"""
        if (type(value) == Card):
            self.cards[key] = value
        else:
            raise Exception("Cannot set card to value other than type card.")
        return self
    
    def append(self, card):
        """ adds card object to card list """
        self.cards.append(card)
    
    def generateDeck(self):
        """ Generates and adds an organized typical 52-card deck to card list """
        # for every suit, generate 13 cards
        for suit in range(0, 4):
            for value in range(1, 14):
                self.append(Card(suit, value))
    
    def transferCardTo(self, cardIndex, cardList):
        """ Removes card from @param cardIndex from self and adds the card to another cardlist (@param cardList)"""
        transferedCard = self.cards.pop(cardIndex)
        cardList.append(transferedCard)
    
    def shuffle(self):
        """ randomizes position of cards """
        shuffle(self.cards)   

class Card():
    """Represents a classic french playing card
    Attributes:
        suit (int): The suit of the card. 0, 1, 2, 3 represent clubs, diamonds, hearts, spades respectively.
        value (int): The value of the card. 1-13. 2-10 being their digit, 1 representing and ace, 11,12,13 represents
                    jack, queen, and king respectively
        isHidden (bool): Describes the card as hidden to all players. This changes how the card is displayed.
    """ 
    def __init__(self, suit, value , isHidden = False):
        if (suit < 0 or 3 < suit):
            raise Exception("Argument suit for card object must be between 0 and 3")
        if (value < 1 or 13 < value):
            raise Exception("Argument suit for card object must be between 1 and 13")
        
        self.suit = suit
        self.value = value
        self.isHidden = isHidden
    
    def getBlackjackValue(self):
        """ returns value of card for a blackjack game. Ace is returned as 1. Face cards are returned as 10 """
        if (self.value == 1): return 1
        elif (self.value <= 10): return self.value
        else: return 10
    
    def getSuitString(self):
        """ returns suit converted to string """
        if (self.suit == 0): return "♣"
        elif (self.suit == 1): return "♦"
        elif (self.suit == 2): return "♥"
        elif (self.suit == 3): return "♠"
    
    def getValueString(self):
        """ returns value converted to string """
        if (self.value == 1): return "Ace"
        elif (self.value <= 10): return str(self.value)
        elif (self.value == 11): return "Jack"
        elif (self.value == 12): return "Queen"
        elif (self.value == 13): return "King"
    
    def __str__(self):
        output = ""
        if self.isHidden:
            return ("[   HIDDEN   ]")
        else:
            output += "["
            output += self.getValueString().ljust(5)
            output += " of "
            output += self.getSuitString() + "'s" + "]"
            return(output)

class BlackjackPlayer():
    """ represents player in a game of blackjack and manages their inventory 
    Attributes:
        cardsInHand (:obj:`cardList`): Represents cards in player's hand
        name (str) : Player's name.
        chips (int): Number of chips owned by player.   
    """
    def __init__(self, cardsInHand, name, chips):
        self.cardsInHand = cardsInHand
        self.name = name
        self.chips = chips
    
    def getHandValue(self):
        """ Calculates the value of the hand for a game of blackjack"""
        handValue = 0
        for card in self.cardsInHand.cards:
            #if card is an ace, don't count it because aces should be counted last  
            if not(card.value == 1):
                handValue += card.getBlackjackValue()
        #now, add the aces with values depending on context
        for card in self.cardsInHand.cards:
            if card.value == 1:
                if (handValue <= 10):
                    handValue += 11
                else:
                    handValue += 1
        return handValue
    
    def printHand(self):
        """ prints hand as it should be shown for a blackjack game. """
        unknown = False
        print((self.name + "'s" + " hand:").ljust(20), end = " ")
        for card in self.cardsInHand.cards:
            # don't tell user the hand value if card is unknown.
            if (card.isHidden):
                unknown = True
            print(card, end = " ")
        if unknown:
            print("HAND VALUE = UNKNOWN")
        else:
            print("HAND VALUE = ", self.getHandValue())
        


