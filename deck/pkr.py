from enum import Enum, IntEnum
import random as random
import collections as collections

from random import shuffle
import math as math
import random as random
from typing import List, Set, Dict, Tuple, Optional


class Suit(Enum):
    """An enum defining the suits in a deck of playing cards"""
    SPADES = 1
    CLUBS = 2
    DIAMONDS = 3
    HEARTS = 4


class Rank(IntEnum):
    """An IntEnum defining the rank of playing cards"""
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


class Card:
    """A playing card in the space (2,14) rank and one of four suits"""
    def __init__(self, rank:Rank=None, suit:Suit = None):
        assert isinstance(rank, Rank)
        assert isinstance(suit, Suit)
        self.rank = rank
        self.suit = suit

    def __str__(self):
        pstring = "{rank} of {suit}"
        return pstring.format(rank=self.rank.name, suit=self.suit.name)

    def __repr__(self):
        pstring = "Card({rank}, {suit})"
        return pstring.format(rank=self.rank, suit=self.suit)

    def __eq__(self, other):
        if self.suit == other.suit and self.rank == other.rank:
            return True
        else:
            return False

    def __hash__(self):
        return hash((self.rank, self.suit))

    def __gt__(self, other):
        if self.rank > other.rank:
            return True
        if self.rank < other.rank:
            return False
        
    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank


class Hand:
    """A hand holds cards from a particular deck"""
    def __init__(self, cards:List[Card]):
        all_cards = [x for x in cards if isinstance(x, Card)]
        cards_set = set(cards)
        print(f'all_cards:{all_cards}; cards_set:{cards_set}')
        if len(all_cards) != len(cards):
            raise ValueError('all cards must be of class Card')
        
        if len(all_cards) != len(cards_set):
            raise ValueError('all cards must be unique')
        else:
            self.cards = cards
            self.pos = 0

    def __len__(self):
        return len(self.cards)

    def __iter__(self):
        self.pos = 0
        return iter(self.cards)
    
    def __str__(self):
        result = ",".join(str(card) for card in self.cards)
        return result

    def __repr__(self):
        result = ",".join(repr(card) for card in self.cards)
        
    def __next__(self):
        self.pos += 1
        if self.pos > len(self.cards):
            raise StopIteration
        else:
            return self.cards[self.pos - 1]

    def get_suits(self) -> List[Suit]:
        suits = []
        for card in self.cards:
            suits.append(card.get_suit())
        return suits


def random_choice(upper: int, lower: int) -> int:
    """Choose an int between upper and lower, uniformly at random"""
    x = random.randint(upper, lower)
    return x


def random_suit() -> Suit:
    """Choose a Suit uniformly at random. Return a Suit Enum"""
    choice = Suit(random_choice(1, 4))
    return choice


def random_rank() -> Rank:
    """Choose a rank uniformly at random. Return a Rank Enum"""
    choice = Rank(random_choice(2, 13))
    return choice


def random_card() -> Card:
    """Choose a Suit and Rank uniformly at random,
      return the combination as a Card object"""
    suit = random_suit()
    rank = random_rank()
    card = Card(rank, suit)
    return card


def random_hand() -> Hand:
    """Choose five cards using random_card.
    Note that this function does not handle the possibility of
    two cards having the same rank & suit.
    Returns a list of Card objects"""
    deck = Deck()
    hand = deck.deal(num_cards = 5)
    return Hand(hand)




class Deck:
    """An object representing a deck of playing cards"""
    def __init__(self):
        deck = [Card(rank, suit) for suit in Suit for rank in Rank]
        random.shuffle(deck)
        self._cards = deck

    def __len__(self):
        return len(self._cards)

    def __getitem__(self, position):
        return self._cards[position]

    def __repr__(self):
        fstring = "Cards remaining: {left}"
        return fstring.format(left=len(self._cards))

    def shuffle(self):
        self._cards = shuffle(self._cards)

    def deal(self, num_cards):
        if num_cards < 1:
            raise ValueError("cannot be dealt less than 1 card")
        if num_cards == 1:
            cards = self._cards[0]
        else:
            
            cards = self._cards[0:num_cards]
            self._cards = self._cards[num_cards:]
        return cards


class Player:
    def __init__(self, hand=None, stash=None):
        if hand is None:
            self.hand = []
        else:
            self.hand = hand
        if stash is None:
            self.stash = 5000
        else:
            self.stash = stash
        self.score = 0
        self.minbet = 10
        self.randnum = random.randint(0, 100)

    def __repr__(self):
        fstring = "Player(stash = {stash}, score={score}, hand = {hand})"
        return fstring.format(stash=self.stash,
                              score=self.score,
                              hand=self.hand)

    def scores(self) -> float:
        if len(self.hand) > 0:
            score, sname = score_hand(self.hand)
            self.score = score
            return self.score
        else:
            return self.score

    def discard(self):
        self.hand = discard_cards(self.hand)

    def bet(self, bet=None) -> float:
        if bet:
            return bet
        else:
            bet = 0
            score, name = score_hand(self.hand)
            print(f'score is {score}')
            if score > 200:
                bet = (self.stash * 0.01) * math.log(score)
                self.stash -= bet
                return bet
            else:
                self.stash -= self.minbet
                return self.minbet

    def call(self, bet_required=None) -> bool:
        if not self.score:
            self.score, _ = score_hand(self.hand)

        if self.score < 200:
            return False
        else:
            return True

        if bet_required:
            if self.score < bet_required:
                return False
            else:
                return True

    def fold(self) -> bool:
        if not self.score:
            self.score, _ = score_hand(self.hand)
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
        self.ante = ante
        self.maxdrop = 3
        deck = Deck()
        self.deck = deck
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

def deal_cards(game:Game, players:List[Player]) -> Tuple[Game, List[Player]]:
    """Takes a list of players (normally empty lists)
      and deals each of them five cards,
      returning the updated lists"""
    for i in range(0, 5):
        for player in players:
            card = game.deck.deal(num_cards=1)
            player.hand.append(card)
    return game, players



def split_cards(Hand:Hand) -> Tuple[List[Suit], List[Rank]]:
    """Takes a list of card objects (a hand) and returns two lists,
      one of the
      suits, and the other of the ranks of the hand.
      Mostly useful for further functions """
    suits = []
    ranks = []
    for card in Hand:
        suits.append(card.suit)
        ranks.append(card.rank)
    return suits, ranks


def count(ranks):
    """Take either a list of suits of ranks and returns
      a dict with the counts of each. 
      Used as input to checking functions"""
    rdict = dict.fromkeys(ranks)
    for each in ranks:
        if rdict[each]:
            rdict[each] += 1
        if not rdict[each]:
            rdict[each] = 1
    return rdict


def anyrep(ranks):
    """Check if there are any repeated elements in either 
      a selection of suits or ranks.
      Return True if there are, False otherwise.
      """
    origlen = len(ranks)
    uniquelen = len(set(ranks))
    if origlen == uniquelen:
        return False
    else:
        return True


def find_repeated_cards(ranks):
    """Check if there are any repeated cards in a list of suits or ranks. 
    Return the elements which are repeated if so, an empty dictionary otherwise"""
    res = {}
    counts = count(ranks)
    for k, v in counts.items():
        if v >= 2:
            res[k] = v
    return res


def is_straight(ranks : List[Rank]) -> bool:
    all_ranks = [x for x in ranks if isinstance(x, Rank)]
    if len(all_ranks) != len(ranks):
        raise ValueError('all cards must be of class Rank')
    ranks_int = [int(rank) for rank in ranks]
    min_rank = min(ranks_int)
    straight_seq = list(range(min_rank, min_rank+5))
    ranks_int.sort()
    if ranks_int == straight_seq:
        return True
    else:
        return False

def is_flush(suits : List[Suit]) -> bool :
    """Check if a set of suits contains a flush (all suits are the same). 
      Returns True if so, False otherwise. 
    If exact=False, returns the highest count of same suits present. """
    all_suits = [x for x in suits if isinstance(x, Suit)]
    if len(all_suits) != len(suits):
        raise ValueError('all suits must be of class Suit')
    sc = count(suits)
    maxval = max(sc.values())
    if maxval == 5:
        return True
    else:
        return False


def make_straight(start: int) -> Hand:
    """This can produce a straight flush, of suit random_suit and starting at Rank start"""
    hand = []
    if not start:
        start = 7
    for rank in range(start, start + 5):
        hand.append(Card(Rank(rank), random_suit()))
    return Hand(hand)

def make_flush(suit: Suit = None) -> Hand:
    """This can produce a flush, of suit random_suit and with a random_ranks"""
    hand = []
    if not suit:
        suit = random_suit()
    random_ranks = random.sample(set(Rank), 5)
    for rank in random_ranks:
        hand.append(Card(rank, suit))
    return Hand(hand)


def get_scores() -> Dict[str, int]:
    """Returns a dictionary with potential hands and the scores associated
      with them. Normally only called from within other functions"""
    scores = {
        'NOTHING': 2,
        'PAIR': 238,
        'TWO-PAIR': 2105,
        'THREE-OF-A-KIND': 4741,
        'STRAIGHT': 25641,
        'FLUSH': 52631,
        'FULL-HOUSE': 71428,
        'FOUR-OF-A-KIND': 500000,
        'STRAIGHT-FLUSH': 100000000
    }
    return scores


def print_source(function):
    import inspect
    import pprint
    pprint.pprint(inspect.getsource(function))


def score_hand(hand :Hand):
    """Return the score of a particular hand. Returns a tuple with the
      name of the hand and the score associated with this hand"""
    scores = get_scores()
    suits, ranks = split_cards(hand)
    flush = is_flush(suits)
    straight = is_straight(ranks)
    pairs = find_repeated_cards(ranks)
    if straight and not flush:
        handscore = scores['STRAIGHT']
        scorename = 'STRAIGHT'
    if flush and not straight:
        handscore = scores['FLUSH']
        scorename = 'FLUSH'
    if straight and flush:
        handscore = scores['STRAIGHT-FLUSH']
        scorename = 'STRAIGHT-FLUSH'
    if len(pairs) == 0 and not flush and not straight:
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
    """Discard cards that do not add to the value of the hand. Ignores the
      possibility of straights or flushes. 
      Keeps any pairs etc, otherwise
      keeps the highest numeric cards and discards the rest. 
      In any case, will discard no more than three cards."""
    suits, ranks = split_cards(hand)
    score, handname = score_hand(hand)
    if handname == 'STRAIGHT' or handname == 'FLUSH' or handname == 'STRAIGHT-FLUSH':
        keep = hand
        discard = []
    if handname == 'NOTHING':
        three_cards = random.sample(set(hand), 3)
        keep = [card for card in hand if card not in three_cards]
        discard = [card for card in hand if card in three_cards]
    else:
        keep = []
        discard = []
        for card in hand:

            old_score = score
            print(f'card is {card}')
            new_hand = [c for c in hand if c != card]
            score_new, _ = score_hand(new_hand)
            print(f'new_hand is {new_hand}; new_score is {score_new}; old_score is {old_score}')
            if old_score > score_new:
                keep.append(card)
            if old_score == score_new:
                discard.append(card)
            if old_score < score_new:
                raise ValueError("something has gone very wrong")
        discard = [c for c in hand if c not in keep]
        
    return keep, discard


def replenish_cards(deck, player):
    """Takes a deck and player as argument. Deals cards to the player,
      until they have five cards again."""
    while len(player.hand) < 5:
        card = deck.deal()
        player.hand.append(card)
        if len(player.hand) == 5:
            pass
    return deck, player
