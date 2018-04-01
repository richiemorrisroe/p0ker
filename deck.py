
from enum import Enum, IntEnum
import random as random
import collections as collections
from random import shuffle


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


def random_suit() -> Suit:
    choice = Suit(random_choice(1, 4))
    return choice


def random_rank() -> Rank:
    choice = Rank(random_choice(2, 13))
    return choice


def random_card() -> Card:
    suit = random_suit()
    rank = random_rank()
    card = Card(rank, suit)
    return card

def random_hand():
    cards = []
    for _ in range(0, 5):
        cards.append(random_card())
    return cards

# Card = collections.namedtuple("Card", ['rank', 'suit'])

class Card:
    """A playing card in the space (2,13) rank and one of four suits"""
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
    def __repr__(self):
        pstring = "{rank} of {suit}"
        return pstring.format(rank=self.rank, suit=self.suit)


class Hand:
    """A hand holds 5 cards from a particular deck"""
    def __init__(self, cards):
        if len(cards)!= 5:
            print("there should be five cards in a hand")
        else:
            self.cards = cards

class FirstDeck:
    def __init__(self):
        self._cards = [Card(rank, suit) for suit in Suit
                       for rank in Rank]

    def __len__(self):
        return len(self._cards)

    def __getitem__(self, position):
        return self._cards[position]

    def shuffle(self):
        self._cards = shuffle(self._cards)

    def deal(self):
        card = self._cards.pop(0)
        return card

def deal_cards(deck, players):
    """Takes a list of players (normally empty lists)
    and deals each of them five cards,
    returning the updated lists"""
    for i in range(0, 5):
        for player in players:
            card = deck.deal()
            player.hand.append(card)
    return deck, players

from typing import List


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
        if max(vals) == 2 and len(pairs) == 2:
            handscore = scores['TWO-PAIR']
            scorename = 'TWO-PAIR'
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

def discard_cards(hand):
    suits, ranks = split_cards(hand)
    score, handname = score_hand(hand)
    scount = count(suits)
    rcount = count(ranks)
    if handname == 'NOTHING':
        ranks.sort(reverse=True)
        topranks = ranks[0:2]
        minretained = topranks[1].value
        cards_remaining = [(r, s) for r, s in hand if r >= minretained]
    else:
        keep = {k: v for k, v in rcount.items() if v >= 2}
        keepvalues = list(keep)[0].value
        cards_remaining = [(rank, suit) for rank, suit
                           in hand if rank == keepvalues]

    return cards_remaining


def replenish_cards(deck, player):
    while len(player.hand) < 5:
        card = deck.deal()
        player.hand.append(card)
        if len(player.hand) == 5:
            pass
    return deck, player

# maybe straight and flush logic, leave for now
# if is_flush(suits, exact=False)>=3:
#             suitcount = count(suits)
#             cards_remaining = [(k, v) for k, v in hand.items if v>=3]
#             return cards_remaining, 'MAYBE-FLUSH'
#         if is_straight(ranks, exact=False) >= 3:
#             cards_remaining = hand
#             return cards_remaining, 'MAYBE-STRAIGHT'

import math as math
import random as random


class Player:
    def __init__(self, hand=None, stash=5000):
        self.hand = []
        self.stash = stash
        self.score = 0
        self.minbet = 10
        self.randnum = random.randint(0, 100)

    def __repr__(self):
        fstring = "Player(stash = {stash}, score={score}, hand = {hand})"
        return fstring.format(stash=self.stash,
                              score=self.score,
                              hand=self.hand)

    def scores(self):
        if len(self.hand) > 0:
            score, sname = score_hand(self.hand)
            self.score = score
            return self.score
        else:
            return self.score

    def discard(self):
        self.hand = discard_cards(self.hand)

    def bet(self, bet=None):
        if bet:
            return bet
        else:
            score, name = score_hand(self.hand)
            if score > 200:
                bet = (self.stash * 0.01) * math.log(score)
                randnumber = random.random()
                if randnumber < 0.25:
                    bet += self.randnum
                if randnumber > 0.75:
                    bet -= self.randnum
                self.stash = self.stash - bet
                return bet
            else:
                self.stash -= self.minbet
                return self.minbet

    def call(self, bet_required=None):
        if not self.score:
            self.score, _ = score_hand(self.hand)

        else:
            if self.score < 200:
                return False
            else:
                return True
        if bet_required:
            if self.score < bet_required:
                return False
            else:
                return True

    def fold(self):
        if not self.score:
            self.score = score_hand(self.hand)
        if self.score < 100:
            return True
        else:
            return False

    def decide_action(self, game):
        is_call = self.call()
        is_fold = self.fold()
        if is_fold:
            return 'FOLD'
        if not is_fold and is_call:
            return 'CALL'
        if self.score < 200 or self.score > 400:
            return 'CHECK'
        else:
            return 'BET'

class Game:
    def __init__(self, name="poker", ante=100):
        self.name = name
        self.ante = 100
        self.maxdrop = 3
        self.deck = FirstDeck()
        self.pot = 0
    def __repr__(self):
        fstring = "Game{name}, ante={ante}, maxdrop={maxdrop},pot={pot}"
        return fstring.format(name=self.name,
                              ante=self.ante,
                              maxdrop=self.maxdrop,
                              pot=self.pot)

    def start_round(self, players):
        self.deck.shuffle()
        deck, players = deal_cards(self.deck, players=players)
        self.deck = deck
        return players

    def deal(self, player):
        deck, player = replenish_cards(self.deck, player)
        self.deck = deck
        return player

    def compare(self, players):
        scores = {}
        for player in players:
            score, sname = score_hand(players.hand)
            scores[player] = score
        maxscore = max(scores.items)
        return maxscore



    def add_to_pot(self, bet):
        print("pot is {} and bet is {}".format(self.pot, bet))
        self.pot += bet

    def get_pot_value(self):
        return self.pot
