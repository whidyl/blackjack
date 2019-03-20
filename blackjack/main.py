from blackjack import Card, CardList, BlackjackPlayer
import time

def main():
        #initialize deck, user, and dealer
        deck = CardList([])
        user = BlackjackPlayer(CardList([]), "User", 1000)
        dealer = BlackjackPlayer(CardList([]), "Dealer", 99999999)
        running = True

        #game loop
        while running:
                # set deck to have 52 cards shuffled and clear player inventories
                user.cardsInHand = CardList([])
                dealer.cardsInHand = CardList([])
                deck = CardList([])
                deck.generateDeck()
                print("Shuffling deck.")
                printPause()
                deck.shuffle()
                # start game with user betting and 2 cards being dealt
                print("You have", user.chips, "chips.")
                if (user.chips <= 0):
                        print("Your out of chips! Get out of here.")
                        printPause()
                        break
                userBet = getBet(user)
                user.chips -= userBet
                userInsuranceBet = 0
                userWinnings = 0

                print("The dealer gives 2 cards to you and himself.")
                printPause()
                deck.transferCardTo(0, user.cardsInHand)
                deck.transferCardTo(0, user.cardsInHand)

                deck.transferCardTo(0, dealer.cardsInHand)
                deck.transferCardTo(0, dealer.cardsInHand)
                # One of dealer's cards is dealt face down (hidden)
                dealer.cardsInHand[0].isHidden = True
                dealer.printHand()
                user.printHand()
                print()
                
                # If the revealed card is an ace, offer insurance.
                if (dealer.cardsInHand[1].value == 1):
                        print("You may place an insurance bet. Enter 0 for no bet.")
                        #TODO may not exceed half the original wager
                        userInsuranceBet = getBet(user)
                        user.chips -= userInsuranceBet
                
                # Dealer turns hidden card over if he has a blackjack.
                dealer.cardsInHand[0].isHidden = False
                if (dealer.getHandValue() == 21):
                        print("Dealer reveals his cards because he has a blackjack.")
                        printPause()
                        dealer.printHand()
                        # if user doesn't have a blackjack, they lose but keep the insurance bet.
                        if (not (user.getHandValue() == 21)):
                                print("Dealer has a blackjack and you do not. You lose.")
                                userWinnings = userInsuranceBet*2
                                user.chips += userWinnings
                                print("You win", userWinnings, "chips.")
                                continue
                else:
                        dealer.cardsInHand[0].isHidden = True
                
                #player now has the choice between standing, hitting, doubling, and surrendering
                moveOn = False
                # this is here so that we can reset the loop if player busts.
                busted = False
                while not moveOn:
                        userChoice = getChoice()
                        # user stood
                        if(userChoice == 0):
                                moveOn = True
                        # user hit
                        elif(userChoice == 1):
                                printPause()
                                deck.transferCardTo(0, user.cardsInHand)
                                user.printHand()
                                # check if user busts.
                                if (user.getHandValue() > 21):
                                        print("You bust.")
                                        user.chips += userWinnings
                                        print("You win", userWinnings, "chips.")
                                        busted = True
                                        break
                        # user doubled. Double bet and gain one more card.
                        elif(userChoice == 2):
                                user.chips -= userBet
                                userBet*=2
                                deck.transferCardTo(0, user.cardsInHand)
                                moveOn = True
                                printPause()
                                user.printHand()
                                # check if user busts.

                                if (user.getHandValue() > 21):
                                        print("You bust.")
                                        user.chips += userWinnings
                                        print("You win", userWinnings, "chips.")
                                        busted = True
                                        break

                        # user surrendered
                        elif(userChoice == 3):
                                userWinnings = userBet/2
                                user.chips += userWinnings
                                print("You surrender and keep half your bet: ", userWinnings, "chips.")
                                busted = True
                                break
                if (busted):
                        continue

                print("Dealer turns over his hole card.")
                dealer.cardsInHand[0].isHidden = False
                printPause()
                dealer.printHand()
                # if dealer has 16 or less, he draws another card.
                while (dealer.getHandValue() <= 16):
                        print("Dealer draws another card.")
                        printPause()
                        deck.transferCardTo(0, dealer.cardsInHand)
                        dealer.printHand()
                # if dealer is over 21, player wins.
                if (dealer.getHandValue() > 21):
                        print("Dealer busts. You win!")
                        userWinnings = userBet*2
                        user.chips += userWinnings
                        print("You win", userWinnings, "chips.")
                        continue
                # if dealer is worth more
                elif (dealer.getHandValue() < user.getHandValue()):
                        print("Dealer's hand is worth less than yours. You win!")
                        userWinnings = userBet*2
                        user.chips += userWinnings
                        print("You win", userWinnings, "chips.")
                        continue
                # if player is worth more
                elif (dealer.getHandValue() > user.getHandValue()):
                        print("Dealer's hand is worth more than yours. You lose!")
                        print("You win", userWinnings, "chips.")
                        continue
                # if player and dealer have same hand value
                else:
                        print("Dealer's hand is worth the same as yours and you tie.")
                        userWinnings += userBet + userInsuranceBet
                        user.chips += userWinnings
                        print("You win", userWinnings, "chips.")
                        continue
                

def getBet(player):
        recievedInput = False
        while not recievedInput:
                try:
                        bet = int(input("Please enter a bet: "))
                        if bet > player.chips:
                                print("You don't have enought chips to make this bet.")
                                continue
                        elif bet < 0:
                                print("Bet must be greater than 0.")
                                continue
                        recievedInput = True
                except:
                        print("Incorrect input. Try entering a number.")
        return bet

def getChoice():
        recievedInput = False
        while not recievedInput:
                try:
                        choice = int(input("Would you like to stand(0), hit(1), double(2), or surrender(3)? "))
                        if choice in [0, 1, 2, 3]:
                                recievedInput = True
                                return choice
                        else:
                                raise Exception()
                        
                except:
                        print("Incorrect input. Please enter 0, 1, 2, or 3.")

def printPause():
        time.sleep(0.3)
        print('.', end = "")
        time.sleep(0.3)
        print('.', end = "")
        time.sleep(0.3)
        print('.', end = "")
        print()

if __name__ == "__main__":
    main()

