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
      def __init__(self, suit, rank):
            self.rank = rank
            self.suit = suit

      def __str__(self):
            pstring = "{rank} of {suit}"
            return pstring.format(rank=self.rank.name, suit=self.suit.name)

      def __repr__(self):
            pstring = "Card({rank}, {suit})"
            return pstring.format(rank=self.rank, suit=self.suit)


class Hand:
      """A hand holds cards from a particular deck"""
      def __init__(self, cards):
            all_cards = [x for x in cards if isinstance(x, Card)]
            if len(all_cards) != len(cards):
                  raise ValueError('all cards must be of class Card')
            else:
                  self.cards = cards
                  self.pos = 0

      def __len__(self):
            
            return len(self.cards)

      def __iter__(self):
            self.pos = 0
            return iter(self.cards)

      def __next__(self):
            self.pos += 1
            if self.pos > len(self.cards):
                  raise StopIteration
            else:
                  return self.cards[self.pos - 1]


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
      card = Card(suit, rank)
      return card

def random_hand() -> Hand:
      """Choose five cards using random_card.
      Note that this function does not handle the possibility of
      two cards having the same rank & suit.
      Returns a list of Card objects"""
      cards = []
      for _ in range(0, 5):
            cards.append(random_card())
      return Hand(cards=cards)


class Deck:
    """An object representing a deck of playing cards"""
    def __init__(self):
          self._cards = [Card(rank, suit) for suit in Suit for rank in Rank]

    def __len__(self):
          return len(self._cards)

    def __getitem__(self, position):
          return self._cards[position]

    def __repr__(self):
          fstring = "Cards remaining: {left}"
          return fstring.format(left=len(self._cards))

    def shuffle(self):
          self._cards = shuffle(self._cards)

    def deal(self):
          card = self._cards.pop(0)
          return card


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



def deal_cards(deck, players):
      """Takes a list of players (normally empty lists)
      and deals each of them five cards,
      returning the updated lists"""
      for i in range(0, 5):
            for player in players:
                  card = deck.deal()
                  player.hand.append(card)
      return deck, players


def split_cards(Hand):
      """Takes a list of card objects (a hand) and returns two lists,
      one of the
      suits, and the other of the ranks of the hand.
      Mostly useful for further functions """
      suits = []
      ranks = []
      for each in Hand:
            suits.append(each.suit)
            ranks.append(each.rank)
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
      """
      Check if there are any repeated elements in either a selection of suits or ranks.
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


def is_straight(ranks, exact=True):
      """Check if the hand contains a straight.
      Returns True if so, False otherwise. 
      If exact=False, then returns the number of cards which 
      form part of a straight"""
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
      """Check if a set of suits contains a flush (all suits are the same). 
      Returns True if so, False otherwise. 
    If exact=False, returns the highest count of same suits present. """
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
            '4-OF-A-KIND': 500000,
            'STRAIGHT-FLUSH': 100000000
      }
      return scores


def score_hand(hand):
      """Return the score of a particular hand. Returns a tuple with the
      name of the hand and the score associated with this hand"""
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
      """Discard cards that do not add to the value of the hand. Ignores the
      possibility of straights or flushes. 
      Keeps any pairs etc, otherwise
      keeps the highest numeric cards and discards the rest. 
      In any case, will discard no more than three cards."""
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
            cards_remaining = [(rank, suit) for rank, suit in hand
                           if rank == keepvalues]

      return cards_remaining


def replenish_cards(deck, player):
      """Takes a deck and player as argument. Deals cards to the player,
      until they have five cards again."""
      while len(player.hand) < 5:
            card = deck.deal()
            player.hand.append(card)
            if len(player.hand) == 5:
                  pass
      return deck, player


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
            self.ante = ante
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
