
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


def random_suit(Suit: Suit) -> Suit:
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

from deck import FirstDeck, Rank, Suit
player1 = []
player2 = []
player3 = []
players = [player1, player2, player3]
mydeck = FirstDeck()


def deal_cards(deck, players):
    """Takes a list of players (normally empty lists)
    and deals each of them five cards,
    returning the updated lists"""
    deck.shuffle()
    for i in range(0, 5):
        for player in players:
            card = mydeck.deal()
            player.append(card)
    return players


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

suits_uc = {"♠": 1, "♣": 2, "♥": 4, "♦": 8}

from typing import List
rankdict = dict.fromkeys(Rank)


def split_cards(hand):
    """Takes a list of card objects (a hand) and returns two lists,
    one of the
    suits, and the other of the ranks of the hand.
    Mostly useful for further functions """
    suits = []
    ranks = []
    for each in hand:
        suits.append(each.suit)
        ranks.append(each.rank)
    return suits, ranks


def count(ranks):
    """Take either a list of suits or ranks and returns
a dict with the counts of each. Used as input to checking functions"""
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
    res = {}
    counts = count(ranks)
    for k, v in counts.items():
        if v >= 2:
            res[k] = v
    return res


def is_straight(ranks, exact=True):
    ranks.sort()
    count = 0
    for i in range(0, len(ranks) - 1):
        if ranks[i + 1] - ranks[i] == 1:
            count += 1
    if not exact:
        return count

    if count == 4:
        return True
    else:
        return False


def is_flush(suits, exact=True):
    sc = count(suits)
    maxval = max(sc.values())
    if not exact:
        return maxval
    if maxval == 5:
        return True
    else:
        return False


def make_straight(suit: Suit, start: int) -> List[Card]:
    """This actually makes a straight flush, of suit Suit and starting at Rank start"""
    hand = []
    if not start:
        start = 7
    for rank in range(start, start + 5):
        hand.append(Card(suit, Rank(rank)))
    return hand

from deck import split_cards, is_flush, is_straight, count


def get_scores():
    scores = {'NOTHING': 2,
              'PAIR': 238,
              'TWO-PAIR': 2105,
              'THREE-OF-A-KIND': 4741,
              'STRAIGHT': 25641,
              'FLUSH': 52631,
              'FULL-HOUSE': 71428,
              '4-OF-A-KIND': 500000,
              'STRAIGHT-FLUSH': 100000000}
    return scores


def score_hand(hand):
    scores = get_scores()
    suits, ranks = split_cards(hand)
    flush = is_flush(suits)
    straight = is_straight(ranks)
    print("flush is {}, and straight is {}".format(flush, straight))
    pairs = find_repeated_cards(ranks)
    print("len(pairs) = {}".format(len(pairs)))
    if straight:
        handscore = scores['STRAIGHT']
        scorename = 'STRAIGHT'
    if flush:
        handscore = scores['FLUSH']
        scorename = 'FLUSH'
    if straight and flush:
        handscore = scores['STRAIGHT-FLUSH']
        scorename = 'STRAIGHT-FLUSH'
    if len(pairs) == 0:
        handscore = scores['NOTHING']
        scorename = 'NOTHING'
    if len(pairs) >= 1:
        vals = pairs.values()
        if max(vals) == 2 and len(pairs) == 1:
            handscore = scores['PAIR']
            scorename = 'PAIR'
        if max(vals) == 3 and len(pairs) == 1:
            handscore = scores['THREE-OF-A-KIND']
            scorename = 'THREE-OF-A-KIND'
        if max(vals) == 3 and len(pairs) == 2:
            handscore = scores['FULL-HOUSE']
            scorename = 'FULL-HOUSE'
        if max(vals) == 4:
            handscore = scores['FOUR-OF-A-KIND']
            scorename = 'FOUR-OF-A-KIND'
    return handscore, scorename
