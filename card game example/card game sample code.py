# Magic the Lambda-ing!
import random


class Card:
    cardtype = 'Staff'

    def __init__(self, name, attack, defense):
        """
        Create a Card object with a name, attack,
        and defense.
        >>> staff_member = Card('staff', 400, 300)
        >>> staff_member.name
        'staff'
        >>> staff_member.attack
        400
        >>> staff_member.defense
        300
        >>> other_staff = Card('other', 300, 500)
        >>> other_staff.attack
        300
        >>> other_staff.defense
        500
        """
        self.name = name
        self.attack = attack
        self.defense = defense

    def power(self, opponent_card):
        """
        Calculate power as:
        (player card's attack) - (opponent card's defense)
        >>> staff_member = Card('staff', 400, 300)
        >>> other_staff = Card('other', 300, 500)
        >>> staff_member.power(other_staff)
        -100
        >>> other_staff.power(staff_member)
        0
        >>> third_card = Card('third', 200, 400)
        >>> staff_member.power(third_card)
        0
        >>> third_card.power(staff_member)
        -100
        """
        return self.attack - opponent_card.defense

    def effect(self, opponent_card, player, opponent):
        ...

    def __repr__(self):
        ...

    def copy(self):
        ...


class Player:
    def __init__(self, deck, name):
        """Initialize a Player object.
        A Player starts the game by drawing 5 cards from their deck. Each turn,
        a Player draws another card from the deck and chooses one to play.
        >>> test_card = Card('test', 100, 100)
        >>> test_deck = Deck([test_card.copy() for _ in range(6)])
        >>> test_player = Player(test_deck, 'tester')
        >>> len(test_deck.cards)
        1
        >>> len(test_player.hand)
        5
        """
        self.deck = deck
        self.name = name
        self.hand = [self.deck.draw() for i in range(5)]

    def draw(self):
        """Draw a card from the player's deck and add it to their hand.
        >>> test_card = Card('test', 100, 100)
        >>> test_deck = Deck([test_card.copy() for _ in range(6)])
        >>> test_player = Player(test_deck, 'tester')
        >>> test_player.draw()
        >>> len(test_deck.cards)
        0
        >>> len(test_player.hand)
        6
        """
        assert not self.deck.is_empty(), 'Deck is empty!'
        self.hand.append(self.deck.draw())

    def play(self, index):
        """Remove and return a card from the player's hand at the given INDEX.
        >>> from cards import *
        >>> test_player = Player(standard_deck, 'tester')
        >>> ta1, ta2 = TACard("ta_1", 300, 400), TACard("ta_2", 500, 600)
        >>> tutor1, tutor2 = TutorCard("t1", 200, 500), TutorCard("t2", 600, 400)
        >>> test_player.hand = [ta1, ta2, tutor1, tutor2]
        >>> test_player.play(0) is ta1
        True
        >>> test_player.play(2) is tutor2
        True
        >>> len(test_player.hand)
        2
        """
        return self.hand.pop(index)

    def display_hand(self):
        ...

    def play_random(self):
        ...


class AICard(Card):
    cardtype = 'AI'

    def effect(self, opponent_card, player, opponent):
        """
        Add the top two cards of your deck to your hand via drawing.
        Once you have finished writing your code for this problem,
        set implemented to True so that the text is printed when
        playing an AICard.

        >>> from cards import *
        >>> player1, player2 = Player(standard_deck.copy(), 'p1'), Player(standard_deck.copy(), 'p2')
        >>> opponent_card = Card("other", 500, 500)
        >>> test_card = AICard("AI Card", 500, 500)
        >>> initial_deck_length = len(player1.deck.cards)
        >>> initial_hand_size = len(player1.hand)
        >>> test_card.effect(opponent_card, player1, player2)
        AI Card allows me to draw two cards!
        >>> initial_hand_size == len(player1.hand) - 2
        True
        >>> initial_deck_length == len(player1.deck.cards) + 2
        True
        """
        implemented = True
        for i in range(2):
            player.hand.append(player.deck.draw())
        if implemented:
            print(f"{self.name} allows me to draw two cards!")

    def copy(self):
        ...


class TutorCard(Card):
    cardtype = 'Tutor'

    def effect(self, opponent_card, player, opponent):
        """
        Add a copy of the first card in your hand
        to your hand, at the cost of losing the current
        round. If there are no cards in hand, this card does
        not add any cards, but still loses the round.  To
        implement the second part of this effect, a Tutor
        card's power should be less than all non-Tutor cards.

        >>> from cards import *
        >>> player1, player2 = Player(standard_deck.copy(), 'p1'), Player(standard_deck.copy(), 'p2')
        >>> opponent_card = Card("other", 500, 500)
        >>> test_card = TutorCard("Tutor Card", 10000, 10000)
        >>> player1.hand = [Card("card1", 0, 100), Card("card2", 100, 0)]
        >>> test_card.effect(opponent_card, player1, player2)
        Tutor Card allows me to add a copy of a card to my hand!
        >>> print(player1.hand)
        [card1: Staff, [0, 100], card2: Staff, [100, 0], card1: Staff, [0, 100]]
        >>> player1.hand[0] is player1.hand[2] # must add a copy!
        False
        >>> player1.hand = []
        >>> test_card.effect(opponent_card, player1, player2)
        >>> print(player1.hand) # must not add a card if not available
        []
        >>> test_card.power(opponent_card) < opponent_card.power(test_card)
        True
        """
        if player.hand:
            added = True
            player.hand.append(player.hand[0].copy())
        else:
            added = False

        if added:
            print(f"{self.name} allows me to add a copy of a card to my hand!")

    def power(self, opponent_card):
        super().power(opponent_card)
        return -float('inf')

    def copy(self):
        ...


class TACard(Card):
    cardtype = 'TA'

    def effect(self, opponent_card, player, opponent, arg=None):
        """
        Discard the card with the highest `power` in your hand,
        and add the discarded card's attack and defense
        to this card's own respective stats.

        >>> from cards import *
        >>> player1, player2 = Player(standard_deck.copy(), 'p1'), Player(standard_deck.copy(), 'p2')
        >>> opponent_card = Card("other", 500, 500)
        >>> test_card = TACard("TA Card", 500, 500)
        >>> player1.hand = []
        >>> test_card.effect(opponent_card, player1, player2) # if no cards in hand, no effect.
        >>> print(test_card.attack, test_card.defense)
        500 500
        >>> player1.hand = [Card("card1", 0, 100), TutorCard("tutor", 10000, 10000), Card("card3", 100, 0)]
        >>> test_card.effect(opponent_card, player1, player2) # must use card's power method.
        TA Card discards card3 from my hand to increase its own power!
        >>> print(player1.hand)
        [card1: Staff, [0, 100], tutor: Tutor, [10000, 10000]]
        >>> print(test_card.attack, test_card.defense)
        600 500
        """
        if player.hand:
            i = 0
            index_best_card = 0
            best_card = player.hand[0]
            while i < len(player.hand):
                if player.hand[i].cardtype == 'Staff' and player.hand[i].power(opponent_card) > best_card.power(opponent_card):
                    best_card = player.hand[i]
                    index_best_card = i
                i += 1
            self.attack += best_card.attack
            self.defense += best_card.defense
            player.hand.pop(index_best_card)
            if best_card:
                print(
                    f"{self.name} discards {best_card.name} from my hand to increase its own power!")

    def copy(self):
        ...


class InstructorCard(Card):
    cardtype = 'Instructor'

    def effect(self, opponent_card, player, opponent, arg=None):
        """
        Survives multiple rounds, as long as it has a non-negative
        attack or defense at the end of a round. At the beginning of the round,
        its attack and defense are permanently reduced by 1000 each.
        If this card would survive, it is added back to the hand.

        >>> from cards import *
        >>> player1, player2 = Player(standard_deck.copy(), 'p1'), Player(standard_deck.copy(), 'p2')
        >>> opponent_card = Card("other", 500, 500)
        >>> test_card = InstructorCard("Instructor Card", 1000, 1000)
        >>> player1.hand = [Card("card1", 0, 100)]
        >>> test_card.effect(opponent_card, player1, player2)
        Instructor Card returns to my hand!
        >>> print(player1.hand) # survives with non-negative attack
        [card1: Staff, [0, 100], Instructor Card: Instructor, [0, 0]]
        >>> player1.hand = [Card("card1", 0, 100)]
        >>> test_card.effect(opponent_card, player1, player2)
        >>> print(player1.hand)
        [card1: Staff, [0, 100]]
        >>> print(test_card.attack, test_card.defense)
        -1000 -1000
        """
        self.attack -= 1000
        self.defense -= 1000
        if self.attack >= 0 or self.defense >= 0:
            re_add = True
        else:
            re_add = False
        if re_add:
            player.hand.append(self.copy())
        if re_add:
            print(f"{self.name} returns to my hand!")

    def copy(self):
        return InstructorCard(self.name, self.attack, self.defense)


class Deck:
    ...
