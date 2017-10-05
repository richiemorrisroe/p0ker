
from enum import Enum, IntEnum
import random as random
import collections as collections



class Suit(Enum):
    SPADES = 1
    CLUBS = 2
    DIAMONDS = 3
    HEARTS = 4


class Rank(IntEnum):
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13
    ACE = 14


def random_choice(upper, lower):
    x = random.randint(upper, lower)
    return x


def random_suit(Suit : Suit) -> Suit:
    choice = Suit(random_choice(1, 4))
    return choice


def random_rank(Rank: Rank) -> Rank:
    choice = Rank(random_choice(2, 13))
    return choice


Card = collections.namedtuple("Card", ['rank', 'suit'])

from random import shuffle


class FirstDeck:
    def __init__(self):
        self._cards = [Card(rank, suit) for suit in Suit
                       for rank in Rank]
    def __len__(self):
        return len(self._cards)
    def __getitem__(self, position):
        return self._cards[position]

    def shuffle(self):
        cards = shuffle(self._cards)

    def deal(self):
        card = self._cards.pop(0)
        return card

player1 = []
player2 = []
player3 = []
players = [player1, player2, player3]
mydeck = FirstDeck()
mydeck.shuffle()
for i in range(0, 5):
    for player in players:
        card = mydeck.deal()
        player.append(card)

suits = []
ranks = []
for card in player3:
    suits.append(card.suit)
    ranks.append(card.rank)

for suit in Suit:
    print(suits.count(suit))

rcount = []
for rank in Rank:
    rcount.append(ranks.count(rank))

suits_uc = { "♠" :1, "♣" : 2, "♥" : 4, "♦" : 8 }

rankdict = dict.fromkeys(Rank)

for each in ranks:
    print(each.name)


def split_cards(hand):
    suits = []
    ranks = []
    for each in hand:
        suits.append(each.suit)
        ranks.append(each.rank)
    return suits, ranks


def count(ranks):
    rdict = dict.fromkeys(ranks)
    for each in ranks:
        if rdict[each]:
            rdict[each] += 1
        if not rdict[each]:
            rdict[each] = 1
    return rdict


def anyrep(ranks):
    origlen = len(ranks)
    uniquelen = len(set(ranks))
    if origlen == uniquelen:
        return False
    else:
        return True


def find_repeated_cards(ranks):
    res = []
    counts = count(ranks)
    for k, v in counts.items():
        if v >= 2:
            res.append((k, v))
    return res


for x in range(0, len(straight_ranks)):
    print(x)

def is_straight(ranks):
    ranks.sort()
    count = 0
    for i in range(0, len(ranks)-1):
        if ranks[i+1] - ranks[i] == 1:
            count +=1
    if count == 4:
        return True
    else:
        return False


def is_flush(suits):
    sc = count(suits)
    for k, v in sc.items():
        if v==5:
            return True
        else:
            return False


def make_straight(suit, start):
    hand = []
    if not start:
        start = 7
    for rank in range(8, 13):
        hand.append(Card(suit, Rank(rank)))
    return hand
