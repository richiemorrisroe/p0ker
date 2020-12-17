from enum import Enum, IntEnum
import random as random


from random import shuffle
import math as math
import random as random
from typing import Union, List, Dict, Tuple, Optional, Set, Any


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

    def __init__(self, rank: Rank, suit: Suit) -> None:
        assert isinstance(rank, Rank)
        assert isinstance(suit, Suit)
        self.rank = rank
        self.suit = suit

    def __str__(self) -> str:
        pstring = "{rank} of {suit}"
        return pstring.format(rank=self.rank.name, suit=self.suit.name)

    def __repr__(self) -> str:
        pstring = "Card({rank}, {suit})"
        return pstring.format(rank=self.rank, suit=self.suit)

    def __eq__(self, other) -> bool:
        if self.suit == other.suit and self.rank == other.rank:
            return True
        else:
            return False

    def __hash__(self) -> int:
        return hash((self.rank, self.suit))

    def __len__(self) -> int:
        return 1

    def __gt__(self, other) -> Optional[bool]:
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

    def __init__(self, cards: Set[Card]) -> None:
        all_cards = [x for x in cards if isinstance(x, Card)]
        cards_set = set(cards)
        if len(all_cards) != len(cards):
            raise ValueError("all cards must be of class Card")

        if len(all_cards) != len(cards_set):
            raise ValueError("all cards must be unique")
        else:
            self.cards = cards
            self.pos = 0

    def __len__(self) -> int:
        return len(self.cards)

    def __iter__(self):
        self.pos = 0
        return iter(self.cards)

    def __eq__(self, other) -> bool:
        eq_cnt = 0
        for s, o in zip(self.cards, other.cards):
            if s == o:
                eq_cnt += 1
            else:
                pass
        if eq_cnt == len(self.cards):
            return True
        else:
            return False

    def __str__(self) -> str:
        result = ",".join(str(card) for card in self.cards)
        return result

    def __repr__(self) -> str:
        result = ",".join(repr(card) for card in self.cards)
        return result

    def __next__(self):
        self.pos += 1
        if self.pos > len(self.cards):
            raise StopIteration
        else:
            return self.cards[self.pos - 1]

    def add_card(self, card: Card) -> None:
        if len(self) >= 5:
            pass
        else:
            self.cards.append(card)

    def count(self, suit_or_rank=None):
        """Take either a list of suits of ranks and returns
        a dict with the counts of each.
        Used as input to checking functions"""
        suits, ranks = self.split_cards()
        if suit_or_rank == "suits":
            vals = suits
        if suit_or_rank == "ranks":
            vals = ranks
        rdict = dict.fromkeys(vals)
        for each in vals:
            if rdict[each]:
                rdict[each] += 1
            if not rdict[each]:
                rdict[each] = 1
        return rdict

    def split_cards(self) -> Tuple[List[Suit], List[Rank]]:
        """Takes a list of card objects (a hand) and returns two lists,
        one of the
        suits, and the other of the ranks of the hand.
        Mostly useful for further functions"""
        suits = []
        ranks = []
        for card in self.cards:
            suits.append(card.suit)
            ranks.append(card.rank)
        return suits, ranks

    def get_scores(self) -> Dict[str, int]:
        """Returns a dictionary with potential hands and the scores associated
        with them. Normally only called from within other functions"""
        scores = {
            "NOTHING": 2,
            "PAIR": 238,
            "TWO-PAIR": 2105,
            "THREE-OF-A-KIND": 4741,
            "STRAIGHT": 25641,
            "FLUSH": 52631,
            "FULL-HOUSE": 71428,
            "FOUR-OF-A-KIND": 500000,
            "STRAIGHT-FLUSH": 100000000,
        }
        return scores

    def is_flush(self) -> bool:
        """Check if a set of suits contains a flush (all suits are the same).
        Returns True if so, False otherwise.
        If exact=False, returns the highest count of same suits present."""
        suits, ranks = self.split_cards()
        all_suits = [x for x in suits if isinstance(x, Suit)]
        if len(all_suits) != len(suits):
            raise ValueError("all suits must be of class Suit")
        sc = self.count("suits")
        maxval = max(sc.values())
        if maxval == 5:
            return True
        else:
            return False

    def is_straight(self) -> bool:
        suits, ranks = self.split_cards()
        all_ranks = [x for x in ranks if isinstance(x, Rank)]
        if len(all_ranks) != len(ranks):
            raise ValueError("all cards must be of class Rank")
        ranks_int = [int(rank) for rank in ranks]
        min_rank = min(ranks_int)
        straight_seq = list(range(min_rank, min_rank + 5))
        ranks_int.sort()
        if ranks_int == straight_seq:
            return True
        else:
            return False

    def find_repeated_cards(self):
        """Check if there are any repeated cards in a list of suits or ranks.
        Return the elements which are repeated if so, an empty dictionary otherwise"""
        suits, ranks = self.split_cards()
        res = {}
        counts = self.count("ranks")
        for k, v in counts.items():
            if v >= 2:
                res[k] = v
        return res

    def score(self) -> Tuple[int, str]:
        """Return the score of a particular hand. Returns a tuple with the
        name of the hand and the score associated with this hand"""
        hand = Hand(self.cards)
        scores = hand.get_scores()
        print(len(hand))
        if len(hand) == 0:
            handscore = 0
            scorename = "EMPTY"
            return handscore, scorename

        suits, ranks = hand.split_cards()
        flush = hand.is_flush()
        straight = hand.is_straight()
        pairs = hand.find_repeated_cards()
        if straight and not flush:
            handscore = scores["STRAIGHT"]
            scorename = "STRAIGHT"
        if flush and not straight:
            handscore = scores["FLUSH"]
            scorename = "FLUSH"
        if straight and flush:
            handscore = scores["STRAIGHT-FLUSH"]
            scorename = "STRAIGHT-FLUSH"
        if len(pairs) == 0 and not flush and not straight:
            handscore = scores["NOTHING"]
            scorename = "NOTHING"
        if len(pairs) >= 1:
            vals = pairs.values()
            if max(vals) == 2 and len(pairs) == 1:
                handscore = scores["PAIR"]
                scorename = "PAIR"
            if max(vals) == 2 and len(pairs) == 2:
                handscore = scores["TWO-PAIR"]
                scorename = "TWO-PAIR"
            if max(vals) == 3 and len(pairs) == 1:
                handscore = scores["THREE-OF-A-KIND"]
                scorename = "THREE-OF-A-KIND"
            if max(vals) == 3 and len(pairs) == 2:
                handscore = scores["FULL-HOUSE"]
                scorename = "FULL-HOUSE"
            if max(vals) == 4:
                handscore = scores["FOUR-OF-A-KIND"]
                scorename = "FOUR-OF-A-KIND"
        return handscore, scorename

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
    hand = deck.deal(num_cards=5)
    return Hand(hand)


class Deck:
    """An object representing a deck of playing cards"""

    def __init__(self) -> None:
        deck = [Card(rank, suit) for suit in Suit for rank in Rank]
        random.shuffle(deck)
        self._cards = deck

    def __len__(self) -> int:
        return len(self._cards)

    def __getitem__(self, position):
        return self._cards[position]

    def __repr__(self) -> str:
        fstring = "Cards remaining: {left}"
        return fstring.format(left=len(self._cards))

    def shuffle(self) -> None:
        shuffle(self._cards)

    def deal(self, num_cards):
        if num_cards < 1:
            raise ValueError("cannot be dealt less than 1 card")
        if num_cards == 1:
            cards = self._cards[0]
            self._cards = self._cards[1:]
        else:

            cards = self._cards[0:num_cards]
            self._cards = self._cards[num_cards:]
        return cards


# class PlayerNamer():
#     def __init__(names):
#         if not names:
#             names = set(["Liam","Emma","Noah","Olivia","William","Ava",
#                 "James","Isabella","Oliver","Sophia"])
#     def get_name(self):
#         return(self.names.pop())


class PlayerNamer:
    def __init__(self, names=None):
        if not names:
            self.names = [
                "Liam",
                "Emma",
                "Noah",
                "Olivia",
                "William",
                "Ava",
                "James",
                "Isabella",
                "Oliver",
                "Sophia",
            ]
        else:
            self.names = names

    def get_name(self) -> str:
        length_names = len(self.names)
        rand_choice = random_choice(0, length_names - 1)
        name = self.names.pop(rand_choice)
        return name


class Player:
    def __init__(self, hand=None, stash=None):

        if hand is None:
            self.hand = Hand([])
        else:
            self.hand = Hand(hand)
        if stash is None:
            self.stash = 5000
        else:
            self.stash = stash
        self.score = 0
        self.minbet = 10
        self.randnum = random.randint(0, 100)

        ##this guarentees unique names as the names list is shared
        ##between player objects. Normally this would be a bug,
        ##it's a little tricksy

    def __repr__(self) -> str:
        fstring = "Player(stash = {stash}, score={score}, hand = {hand})"
        return fstring.format(stash=self.stash, score=self.score, hand=self.hand)

    def __len__(self) -> int:
        return 1

    def scores(self) -> float:
        if len(self.hand) > 0:
            score, sname = Hand(self.hand).score()
            self.score = score
            return self.score
        else:
            return self.score

    def discard(self) -> List[Card]:
        self.hand, discard = discard_cards(self.hand)
        return discard

    def bet(self, bet=None) -> float:
        def check_bet(bet, stash):
            if bet > stash:
                print("got here")
                raise ValueError(
                    "can only bet {max_stash}, you bet {bet}".format(
                        max_stash=stash, bet=bet
                    )
                )
            else:
                return bet

        if bet:
            bet = check_bet(bet, self.stash)
            return bet
        else:
            bet = 0
            score, name = Hand(self.hand).score()
            if score > 200:
                bet = (self.stash * 0.01) * math.log(score)
                bet = check_bet(bet, self.stash)
                self.stash -= bet
                return bet
            else:
                bet = self.minbet
                bet = check_bet(bet, self.stash)
                self.stash -= self.minbet
                return self.minbet

    def call(self, bet_required=None) -> bool:
        if not self.score:
            self.score, _ = Hand(self.hand).score()

        if self.score < 200:
            return False
        else:
            return True

        if bet_required:
            if self.score < bet_required:
                return False
            else:
                return True

    def fold(self, state: Optional[Dict[str, int]] = None) -> bool:
        if not state:
            state = {"min_bet": 100}
        if not self.score:
            self.score, _ = Hand(self.hand).score()
        if self.score < state["min_bet"]:
            return True
        else:
            return False

    def decide_action(self, state=None) -> Dict[str, Union[int, str]]:
        is_call = self.call()
        is_fold = self.fold(state)
        if is_fold:
            return {"action": "FOLD", "amount": 0}
        if not is_fold and is_call:
            return {"action": "CALL", "amount": 0}
        if self.score < 200 or self.score > 400:
            return {"action": "CHECK", "amount": 0}
        else:
            return {"action": "BET", "amount": 0}

    def send_action(self, state=None):
        action = self.decide_action(state)
        return action

    def pay(self, amount):
        self.stash -= amount
        return amount

    def add_card(self, card: Card) -> None:
        self.hand.add_card(card)
        return None


class Round:
    def __init__(self, ante, players: List[Player]) -> None:
        self.pot = 0
        self.position = 0
        self.ante = ante
        self.num_players = len(players)
        self.min_bet = ante
        self.actions = []

    def add_to_pot(self, bet) -> None:
        self.pot += bet

    def get_pot_value(self):
        return self.pot

    def get_position(self):
        return self.position

    def set_position(self, position) -> None:
        self.position = position

    def get_actions(self):
        return self.actions

    def set_action(self, action) -> None:
        self.actions.append(action)
        self.update_state()

    def get_blind(self, blind_type):
        if blind_type == "small":
            return self.ante
        if blind_type == "big":
            return self.ante * 2
        else:
            raise NotImplementedError

    def get_blinds(self, players: List[Player]) -> List[Player]:
        small_blind_pos = 0
        big_blind_pos = 1
        small_blind = self.get_blind("small")
        big_blind = self.get_blind("big")
        sb = players[small_blind_pos].pay(small_blind)
        bb = players[big_blind_pos].pay(big_blind)
        self.add_to_pot(bb + sb)
        return players

    def get_minimum_bet(self):
        if not self.min_bet:
            self.min_bet = self.ante
        return self.min_bet

    def update_state(self) -> Dict[str, Any]:
        sblind = self.get_blind("small")
        lblind = self.get_blind("big")
        potval = self.get_pot_value()
        position = self.get_position()
        min_bet = self.get_minimum_bet()
        actions = self.get_actions()
        return {
            "small_blind": sblind,
            "big_blind": lblind,
            "pot_value": potval,
            "position": position,
            "min_bet": min_bet,
            "actions": actions,
        }


class Dealer:
    def __init__(self, name: str = "poker", ante: int = 100) -> None:
        self.name = name
        self.ante = ante
        self.maxdrop = 3
        deck = Deck()
        self.deck = deck
        self.round = None
        self.discard_pile = []
        self.round_count = None
        self.player_namer = PlayerNamer()

    def start_game(self, players: List[Player]) -> List[Player]:
        player_list = []
        self.round_count = 0
        for player in players:
            player = self.give_name(player)
            player_list.append(player)
        return player_list

    def give_name(self, player):
        name = self.player_namer.get_name()
        player.name = name
        return player

    def __repr__(self) -> str:
        pot = self.get_pot_value()
        fstring = "Game{name}, ante={ante}, maxdrop={maxdrop},pot={pot}"
        return fstring.format(name=self.name, ante=self.ante, maxdrop=self.maxdrop)

    def deals(self, players: List[Player]) -> List[Player]:
        """Takes a list of players (normally empty lists)
        and deals each of them five cards,
        returning the updated lists"""
        deck = self.deck
        for i in range(0, 5):
            for player in players:
                card = deck.deal(num_cards=1)
                player.add_card(card)
        return players

    def update_cards(self, player):
        if len(player) > 1:
            raise ValueError(
                "update cards only takes one player, not {x}".format(x=len(player))
            )
        deck, player = replenish_cards(self.deck, player)
        self.deck = deck
        return player

    def take_action(self, player) -> None:
        state = self.round.update_state()
        print(f"state is:{state}")
        action = player.send_action(state)
        self.round.set_action(action)

    def compare(self, players):
        scores = {}
        for player in players:
            score, sname = player.hand.score()
            scores[player.name] = score
        print(scores)
        # maxscore = max(scores.items())
        return scores

    def start_round(self, players: List[Player] = None) -> Round:
        r = Round(self.ante, players)
        self.round = r
        players = self.round.get_blinds(players)
        players = self.deals(players)
        return r

    def end_round(self, players: List[Player]) -> None:
        self.round_count += 1

    def take_discards(self, cards: List[Card]) -> None:
        for card in cards:
            self.discard_pile.append(card)

    def get_pot_value(self):
        val = self.round.get_pot_value()
        return val

    def get_blind(self, blind_type):
        return self.round.get_blind(blind_type)

    def get_blinds(self, players: List[Player]) -> List[Player]:
        return self.round.get_blinds(players)

    def get_position(self):
        return self.round.position

    def set_position(self, position) -> None:
        self.round.position = position

    def update_state(self, round):
        return round.update_state()

    def get_state(self, Round: Round):
        return self.update_state(Round)


def deal_cards(dealer: Dealer, players: List[Player]) -> Tuple[Dealer, List[Player]]:
    """Takes a list of players (normally empty lists)
    and deals each of them five cards,
    returning the updated lists"""
    for i in range(0, 5):
        for player in players:
            card = dealer.deck.deal(num_cards=1)
            player.add_card(card)
    return dealer, players


def anyrep(ranks) -> bool:
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


def make_straight(start: int) -> Hand:
    """This can produce a straight flush, of suit random_suit and starting at Rank start"""
    hand = []
    if not start:
        start = 7
    for rank in range(start, start + 5):
        hand.append(Card(Rank(rank), random_suit()))
    return Hand(hand)


def make_flush(suit: Optional[Suit] = None) -> Hand:
    """This can produce a flush, of suit random_suit and with a random_ranks"""
    hand = []
    if not suit:
        suit = random_suit()
    random_ranks = random.sample(list(Rank), 5)
    for rank in random_ranks:
        hand.append(Card(rank, suit))
    return Hand(hand)


def print_source(function) -> None:
    import inspect
    import pprint

    pprint.pprint(inspect.getsource(function))


def discard_cards(hand: Hand) -> Tuple[List[Card], List[Card]]:
    """Discard cards that do not add to the value of the hand. Ignores the
    possibility of straights or flushes.
    Keeps any pairs etc, otherwise
    keeps the highest numeric cards and discards the rest.
    In any case, will discard no more than three cards."""
    # if not isinstance(hand, Hand):
    #     hand = Hand(hand)
    if len(hand) <= 3:
        keep, discard = hand, []
        return keep, discard
    suits, ranks = hand.split_cards()
    this_score, handname = hand.score()
    if handname == "STRAIGHT" or handname == "FLUSH" or handname == "STRAIGHT-FLUSH":
        keep = hand.cards
        discard = []
    if handname == "NOTHING":
        three_cards = random.sample(list(hand), 3)
        keep = [card for card in hand if card not in three_cards]
        discard = [card for card in hand if card in three_cards]
    else:
        keep = []
        discard = []
        for card in hand:
            old_score = this_score
            new_hand = Hand([c for c in hand if c != card])
            score_new, _ = new_hand.score()
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
        card = deck.deal(num_cards=1)
        player.add_card(card)
        if len(player.hand) == 5:
            pass
    return deck, player
