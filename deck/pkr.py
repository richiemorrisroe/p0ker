from copy import deepcopy
from enum import Enum, IntEnum
import datetime as dt
import logging
import math
from pprint import pprint
from random import shuffle, sample
import random

from typing import Union, List, Dict, Tuple, Optional, Any, Collection, Sequence
now = dt.datetime.now().isoformat()
logging.basicConfig(filename=f"pkr_{now}.log",
                    # level=logging.INFO,
                    
                    format='%(asctime)s,%(msecs)03d %(name)s - %(levelname)s - %(funcName)s() %(message)s')



logger = logging.getLogger()
logger.setLevel(logging.DEBUG)




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
        if self.rank <= other.rank:
            return False
        return False

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank


class Hand:
    """A hand holds cards from a particular deck"""

    def __init__(self, cards: list[Card]) -> None:
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

    def count(self, suit_or_rank="suit"):
        """Take either a list of suits of ranks and returns
        a dict with the counts of each.
        Used as input to checking functions"""
        vals = suit_or_rank
        if not suit_or_rank:
            suit_or_rank = "suits"
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

    def find_repeated_cards(self) -> Dict[Any, Any]:
        """Check if there are any repeated cards in a list of suits or ranks.
        Return the elements which are repeated if so, an empty dictionary
        otherwise"""
        suits, ranks = self.split_cards()
        res = {}
        counts = self.count("ranks")
        for k, v in counts.items():
            if v >= 2:
                # has at least two of this rank=pair
                res[k] = v
        return res

    def score(self) -> Tuple[int, str]:
        """Return the score of a particular hand. Returns a tuple with the
        name of the hand and the score associated with this hand"""
        hand = Hand(self.cards)
        scores = hand.get_scores()
        if len(hand) == 0:
            handscore = 0
            scorename = "EMPTY"
            return handscore, scorename

        # suits, ranks = hand.split_cards()

        flush = hand.is_flush()
        straight = hand.is_straight()
        pairs = hand.find_repeated_cards()
        handscore, scorename = scores["NOTHING"], "NOTHING"
        suits, ranks = self.split_cards()
        max_rank = max(list(convert_rank_enum_to_integer(ranks)))
        ranks = get_ranks_from_repeated_cards(pairs)
        ranks_int = list(convert_rank_enum_to_integer(ranks).values())
        if straight and not flush:
            handscore = scores["STRAIGHT"] + max_rank
            scorename = "STRAIGHT"
        if flush and not straight:
            handscore = scores["FLUSH"] + max_rank
            scorename = "FLUSH"
        if straight and flush:
            handscore = scores["STRAIGHT-FLUSH"] + max_rank
            scorename = "STRAIGHT-FLUSH"
        if len(pairs) == 0 and not flush and not straight:
            handscore = scores["NOTHING"] + max_rank
            scorename = "NOTHING"
        if len(pairs) > 0:
            handscore, scorename = self.check_for_kind_of_pair(
                pairs, scores, ranks_int)
        return handscore, scorename

    def check_for_kind_of_pair(self, pairs, scores, ranks_int):
        handscore, scorename = scores["NOTHING"], "NOTHING"
        vals = pairs.values()
        if max(vals) == 2 and len(pairs) == 1:
            handscore = scores["PAIR"] + ranks_int[0]
            scorename = "PAIR"
        if max(vals) == 2 and len(pairs) == 2:
            handscore = scores["TWO-PAIR"] + ranks_int[0] + ranks_int[1]
            scorename = "TWO-PAIR"
        if max(vals) == 3 and len(pairs) == 1:
            handscore = scores["THREE-OF-A-KIND"] + ranks_int[0]
            scorename = "THREE-OF-A-KIND"
        if max(vals) == 3 and len(pairs) == 2:
            handscore = scores["FULL-HOUSE"] + ranks_int[0] + ranks_int[1]
            scorename = "FULL-HOUSE"
        if max(vals) == 4:
            handscore = scores["FOUR-OF-A-KIND"] + ranks_int[0]
            scorename = "FOUR-OF-A-KIND"
        return handscore, scorename

    def get_suits(self) -> List[Suit]:
        suits = []
        for card in self.cards:
            suits.append(card.get_suit())
        return suits

    def discard(self) -> Tuple[List[Card], List[Card]]:
        """Discard cards that do not add to the value of the hand. Ignores the
        possibility of straights or flushes.
        Keeps any pairs etc, otherwise
        keeps the highest numeric cards and discards the rest.
        In any case, will discard no more than three cards."""
        # if not isinstance(hand, Hand):
        #     hand = Hand(hand)
        hand = self.cards
        if len(hand) <= 3:
            keep, discard = hand, []
            return keep, discard
        suits, ranks = self.split_cards()
        this_score, handname = self.score()
        if (handname == "STRAIGHT" or handname == "FLUSH" or handname == "STRAIGHT-FLUSH"):
            keep = self.cards
            discard = []
        if handname == "NOTHING":
            three_cards = random.sample(list(hand), 3)
            keep = [card for card in hand if card not in three_cards]
            discard = [card for card in hand if card in three_cards]
        else:
            keep: list[Card] = []
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


def get_ranks_from_repeated_cards(reps: dict) -> Tuple[Rank]:
    result = tuple(reps.keys())
    return result


def convert_rank_enum_to_integer(ranks) -> Dict[Rank, int]:
    rank_ints = {rank: int(rank) for rank in ranks}
    return rank_ints


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
    hand: list[Card] = deck.deal(num_cards=5)
    logger.warning(f"{hand=}")
    return Hand(hand)


class Deck:
    """An object representing a deck of playing cards"""

    def __init__(self) -> None:
        deck = [Card(rank, suit) for suit in Suit for rank in Rank]
        shuffle(deck)
        self._cards: List[Card] = deck

    def __len__(self) -> int:
        return len(self._cards)

    def __getitem__(self, position):
        return self._cards[position]

    def __repr__(self) -> str:
        fstring = "Cards remaining: {left}"
        return fstring.format(left=len(self._cards))

    def shuffle(self) -> None:
        shuffle(self._cards)

    def deal(self, num_cards) -> Card | list[Card]:
        if num_cards < 1:
            raise ValueError("cannot be dealt less than 1 card")
        if num_cards == 1:
            logger.debug(f"{len(self._cards)=}")
            cards = self._cards[0]
            self._cards = self._cards[num_cards:]
        else:
            cards = self._cards[0:num_cards]
            self._cards = self._cards[num_cards:]
        return cards


class Action:
    def __init__(self, kind: str, amount: int, name: str | None = None):
        if kind not in ["BET", "CALL", "RAISE",
                        "FOLD", "CHECK", "MATCH", "END"]:
            raise ValueError(f"{kind} is not a valid action")
        self.kind = kind
        self.amount = amount
        self.name = name

    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, Action):
            return False

        elif (self.kind == __o.kind and self.amount == __o.amount
              and self.name == __o.name):
            return True

        else:
            return False

    def __repr__(self):
        return f"""Action(kind={self.kind!r}, amount={self.amount!r},
        name={self.name!r})"""

    def get_name(self):
        return self.name

    def set_name(self, name):
        if not self.name:
            self.name = name
        elif self.name == name:
            pass
        else:
            raise ValueError("cannot overwrite name")

    def is_valid(self) -> bool:
        if self.kind not in ["BET", "CALL", "RAISE", "FOLD",
                             "CHECK", "END", "MATCH"]:
            raise ValueError(f"{self.kind} is not valid")
        if self.kind == "BET" and self.amount == 0:
            return False
        if self.kind == "FOLD" and self.amount > 0:
            return False
        if self.kind == "CALL" and self.amount == 0:
            return False
        else:
            return True

    def get_action(self) -> str:
        return self.kind

    def get_amount(self) -> int:
        return self.amount


class Actions:
    def __init__(self, actions=None):
        if not actions:
            actions = []
        self.action_list = list()
        for action in actions:
            self.action_list.append(action)
        if not actions:
            self.kind_count = {"CHECK": 0, "BET": 0, "FOLD": 0, "RAISE": 0,
                               "MATCH": 0,  "END": 0}
        self.update_actions()


    def __len__(self):
        return len(self.action_list)

    def __getitem__(self, idx):
        return self.action_list[idx]

    def __repr__(self):
        s = ",".join([repr(a) for a in self.action_list])
        return s

    def update(self, action):
        self.action_list.append(action)
        self.update_actions()

    def get_bets(self):
        bets = []
        for action in self.action_list:
            if action.kind == "BET" or action.kind == "RAISE":
                bets.append(action)
        return bets

    def max_bet(self):
        bets = self.get_bets()
        if len(bets) >= 1:
            max_bet = max([a.amount for a in bets])
        else:
            max_bet = 0
        return max_bet

    def sum_bets(self):
        sum_bets = 0
        if self.kind_count["BET"] == 0:
            return sum_bets
        if self.kind_count["BET"] > 0:
            bets = self.get_bets()
            logger.debug(f"bets are {bets}")
            for bet in bets:
                sum_bets += bet.amount
        return sum_bets

    def update_actions(self):
        kind_count = {"CHECK": 0, "BET": 0, "FOLD": 0, "RAISE": 0,
                           "MATCH": 0,  "END": 0}
        kinds = [a.kind for a in self.action_list]
        for kind in kinds:
            try:
                kind_count[kind] += 1
            except KeyError:
                kind_count[kind] = 1
        self.kind_count = kind_count
        return kind_count


class Player:
    def __init__(self, hand=None, stash=None, name=None):

        if hand is None:
            self.hand = Hand([])
        else:
            self.hand = Hand(hand)
        if stash is None:
            self.stash = 5000
        else:
            self.stash = stash
        if name:
            self.name = name
        self.score = 0
        self.minbet = 10
        self.randnum = random.randint(0, 100)

        # this guarentees unique names as the names list is shared
        # between player objects. Normally this would be a bug,
        # it's a little tricksy

    def __repr__(self) -> str:
        fstring = f"""Player(name = {self.name}, stash = {self.stash},
        score={self.score}, hand = {self.hand})"""
        return fstring

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
        # self.hand.discard() returns (cards_to_keep, cards_to_discard)
        new_hand_cards, discard = self.hand.discard()
        self.hand = Hand(new_hand_cards) # Reassign with a new Hand object
        return discard

    def bet(self, bet=None) -> float:
        def check_bet(bet, stash):
            if bet > stash:
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

    def decide_action(self, state: Dict[str, Any]) -> Action:
        logger.debug(f"state is {state} for {self.name}")
        valid_actions = state["valid_actions"]
        logger.debug(
            f"{valid_actions=}")
        if not valid_actions:
            raise ValueError("there should always be valid actions")
        if len(valid_actions) >= 2:
            action = deepcopy(sample(valid_actions, 1))
            logger.debug(f"{action=}")
            action_pop = action.pop()
            logger.debug(f"selected action for {self.name} is {action_pop}")
            actual_action = action_pop.get_action()
            amount = action_pop.amount
        else:
            action_obj = deepcopy(valid_actions[0])
            actual_action = action_obj.get_action()
            amount = action_obj.amount
            logger.debug(f"action_object is {action_obj}")
        logger.debug(f"{self.name} stash is {self.stash}")
        action = actual_action
        logger.debug(f"{self.name} action is {action}")
        if action == "BET":
            amount = random.randint(state["min_bet"], state["min_bet"] + 100)
            logger.debug(f"amount is {amount}")
        if action == "RAISE":
            pass
        if action == "FOLD" or action == "CHECK":
            amount = 0
        return Action(kind=action, amount=amount, name=None)

    def send_action(self, state: Dict | None = None, action: Action | None = None):
        if not action:
            action = self.decide_action(state)
            logger.info(f"Action:{action}")
        player_name = self.name
        action.set_name(player_name)
        self.stash -= action.amount
        # action = {"name": player_name, "action" : action}
        return action

    def pay(self, amount):
        self.stash -= amount
        return amount

    def add_card(self, card: Card | list[Card]) -> None:
        self.hand.add_card(card)



class Round:
    def __init__(self, ante, players: List[Player]) -> None:
        self.pot = 0
        self.position = 0
        self.ante = ante
        self.num_players = len(players)
        self.min_bet = 0
        self.actions: Actions = Actions(actions=[])
        self.turn = 0
        self.player_names: List[str] = [p.name for p in players]
        self.active_players = players[:] # Create a copy to modify
        self.bets = {p.name: 0 for p in players}
        self.last_raiser: Optional[str] = None

    def __repr__(self):
        repr_string = f"""Round(
        pot={self.pot},
        position={self.position},
        ante={self.ante},
        num_players={self.num_players},
        min_bet = {self.min_bet}
        actions = {self.actions}"""
        return repr_string

    def add_to_pot(self, bet) -> None:
        self.pot += bet

    def get_pot_value(self):
        return self.pot

    def zero_pot(self):
        self.pot = 0

    def reset_bets(self):
        self.bets = {p.name: 0 for p in self.active_players}
        self.last_raiser = None

    def get_position(self):
        return self.position

    def set_position(self, position) -> None:

        self.position = position

    def get_actions(self):
        return self.actions

    def set_action(self, action) -> None:
        self.set_position(self.get_position() + 1)
        self.actions.update(action)
        logger.debug(f"{self.actions=}")
        if action.kind in ["BET", "RAISE"]:
            self.last_raiser = action.name
        self.update_state()

    def get_blinds(self, players: list[Player]) -> List[Player]:
        for player in players:
            self.add_to_pot(player.pay(self.ante))
        return players

    def get_sum_bets(self):
        return self.actions.sum_bets()

    def get_minimum_bet(self):
        if self.turn == 0:
            min_bet = self.ante
        else:
            min_bet = self.min_bet

        self.min_bet = min_bet
        return min_bet

    def get_maximum_bet(self):
        return self.actions.max_bet()

    def is_betting_over(self) -> bool:
        # If only one player is active, the round is effectively over (by folds)
        if len(self.active_players) <= 1:
            return True

        # If no actions have been taken yet, the betting round is not over.
        if len(self.actions.action_list) == 0:
            return False

        current_max_bet = self.get_maximum_bet()
        # Check if all active players have matched the max bet
        # If any active player has bet less than the max bet, betting is not over
        for player in self.active_players:
            player_bet_in_this_round = self.bets.get(player.name, 0)
            if player_bet_in_this_round < current_max_bet:
                return False

        # If all active players have matched the max bet,
        # we need to check if the action has come full circle.
        # This means the current player whose turn it is would be the last raiser
        # or the first player if no one has raised yet.
        # This check needs context from the play_round loop, so for now, we'll
        # assume that if all bets match, and the play_round loop correctly cycles,
        # the betting is effectively over.
        # The play_round loop will manage whose turn it is.
        # The key is that once `current_max_bet` is established, and everyone matches it,
        # the round can end.

        # If last_raiser is None, it means no one has bet/raised yet, only checks or folds.
        # In this case, if all active players have matched current_max_bet (which would be 0),
        # the betting round is over.
        if self.last_raiser is None:
            return True # All checks or folds

        # If a raiser exists, and everyone has matched their bet, the round is over.
        # This assumes the play_round loop correctly ensures everyone has had a chance to act.
        # A more robust solution might track turns more explicitly within Round.
        return True

    def calculate_valid_actions(self) -> List[Action]:
        position = self.get_position()
        actions = self.get_actions()
        no_bet_state = [Action("CHECK", 0), Action("BET", self.ante),
                        Action("FOLD", 0)]
        some_bet_state = [
            Action("MATCH", self.get_maximum_bet()),
            Action("FOLD", 0),
            Action("RAISE", (self.get_maximum_bet()) * 2),
        ]

        match_fold_state = [
            Action("MATCH", 100),
            Action("FOLD", 0),
            Action("RAISE", 200)]

        end_state = [Action("END", 0)]
        if position == 0:
            return no_bet_state
        # logger.debug("actions are {a}".format(a=self.get_actions()))

        kind_count = actions.kind_count
        logger.debug(f"{kind_count=}")
        ## somehow we're calling this too late
        if kind_count['FOLD'] == (self.num_players - 1):
            losers = [a.name for a in
                      self.get_actions() if a.get_action == 'FOLD']
            winner = [name for name in self.player_names
                      if name not in losers].pop()
            logger.debug(f"winner is {winner}")

            end_state = [Action(kind="END", amount=0, name=winner)]
            logger.debug(f"end state is {end_state}")
            return end_state

        if kind_count['BET'] > 0 and kind_count['RAISE'] > 0:
            return match_fold_state

        if kind_count['BET'] > 0:
            logger.debug(f"some bet state is {some_bet_state}")
            return some_bet_state

        if kind_count['CHECK'] + kind_count['FOLD'] == position:
            logger.debug(f"no bet state is {no_bet_state}")
            return no_bet_state
        logger.debug(f"player num is {self.num_players}")

    def update_state(self) -> Dict[str, Any]:
        potval = self.get_pot_value()
        position = self.get_position()
        min_bet = self.get_minimum_bet()
        sum_bets = self.get_sum_bets()
        max_bet = self.get_maximum_bet()
        actions = self.get_actions()
        # logger.debug(f"update state actions:{actions}")
        valid_actions: List[Action] = self.calculate_valid_actions()
        kind_count = self.actions.kind_count

        state = deepcopy(
            {
                "pot_value": potval,
                "position": position,
                "min_bet": min_bet,
                "sum_bets": sum_bets,
                "max_bet": max_bet,
                "actions": actions,
                "valid_actions": valid_actions,
                "kind_count" : kind_count
            }
        )
        # logger.debug(f"update_state state={state}")
        return state


class Dealer:
    def __init__(self, name: str = "poker", ante: int = 100) -> None:
        self.name = name
        self.ante = ante
        self.maxdrop = 3
        deck = Deck()
        self.deck = deck
        self.round: Round | None = None
        self.discard_pile: List[Card] = []
        self.round_count = 0
        self.old_rounds: List[Round] = []
        self.player_names = ["Liam", "Emma", "Noah", "Olivia", "William",
                             "Ava", "James", "Isabella", "Oliver", "Sophia",
                             ]


    def get_player_name(self) -> str:
        names = self.player_names
        rand_choice = random.randint(0, len(names) - 1)
        name = names.pop(rand_choice)
        return name

    def start_game(self, n_players: int) -> list[Player]:
        players = []
        player_dict = {}
        self.round_count = 0
        for x in range(0, n_players):
            name = self.get_player_name()
            player = Player(name=name)
            player_dict[player.name] = player
            players.append(player)
            # logger.debug(f"player_dict is {player_dict}")
            # logger.debug(f"player_list is {players}")
        return players

    def __repr__(self) -> str:
        return f"""Game({self.name}, ante={self.ante},
        maxdrop={self.maxdrop})"""

    def deals(self, players: List[Player]) -> Dict[str, Player]:
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
                "update cards only takes one player, not {x}".format(
                    x=len(player))
            )
        deck, player = replenish_cards(self.deck, player)
        self.deck = deck
        return player

    def update_round(self, players: List[Player], round: Round) -> List[Player]:
        logger.debug(f"players is {players}, round is {round!r}")
        state = self.round.update_state()
        logger.debug(f'{state=}')
        valid_actions = state['valid_actions']
        print(f"va in update_round is {valid_actions}")
        if len(valid_actions) == 1 and valid_actions[0].kind == 'END':
            logger.warning(f"{valid_actions=}")
            winner_name = valid_actions[0].name
            # Find the actual Player object
            winning_player = next((p for p in players if p.name == winner_name), None)
            if winning_player:
                players = self.end_round(round=self.round, players=players, winner=winning_player)
            else:
                # This case should ideally not happen if valid_actions[0].name is always valid
                raise ValueError(f"Winner player '{winner_name}' not found in current players.")
        position = round.get_position()
        if position == round.num_players:
            pass
        self.round = round
        return players

    def take_action(self, player: Player, action=None) -> None:
        state = self.update_state(self.round)
        if not action:
            state = self.update_state(self.round)
            logger.debug(f"take_action state is {state}")
            action = player.send_action(state)
            amount = action.amount
            self.round.add_to_pot(amount)
        else:
            action = player.send_action(state, action)
            amount = action.amount
            self.round.add_to_pot(amount)
        if self.is_valid_action(action):
            self.accept_action(action)
        else:
            raise ValueError("action is not valid")

    def accept_action(self, action) -> None:
        logger.debug(f"action is {action!r}")
        self.round.set_action(action)
        state = self.round.update_state()
        # logger.debug(f"accept action state:{state}")

    def compare(self, players):
        scores = {}
        for player in players:
            score, sname = player.hand.score()
            scores[player.name] = score
        logger.debug(scores)
        # maxscore = max(scores.items())
        return scores

    def _showdown(self, active_players: List[Player]) -> Player:
        if not active_players:
            raise ValueError("Showdown called with no active players.")

        highest_score = -1
        winner: Optional[Player] = None

        for player in active_players:
            player_score = player.scores() # This also updates player.score
            if player_score > highest_score:
                highest_score = player_score
                winner = player
            # For tie-breaking, we can add more complex logic here later.
            # For now, the first player encountered with the max score wins.

        if winner is None:
            # This should ideally not happen if active_players is not empty
            raise ValueError("Could not determine a winner in showdown.")

        return winner

    def start_round(self, players: List[Player]) -> Round:
        logger.debug(f"players passed to start_round={players}")
        r = Round(self.ante, players)
        self.round = r
        players = self.round.get_blinds(players)
        players = self.deals(players)
        for p in players:
            p.hand.score()
        names = [p.name for p in players]
        self.player_names = names
        self.active_players = names
        logger.debug(f"{players=}, {self.active_players}")
        return r

    def end_round(self, round: Round, players: List[Player], winner: Player) -> List[Player]:
        pot_value = round.get_pot_value()
        amount_to_pay = -1 * pot_value # pot value is positive, player pays negative

        logger.debug(f"amout to pay is {amount_to_pay}")
        logger.debug("winning player is {p}".format(p=winner.name))

        # Find the actual winner object from the original list of players
        # The winner passed here should already be the correct Player object
        # winning_player = [p for p in players if p.name == winner.name][0]

        winner.pay(amount_to_pay)

        # For now, all players are returned. Later, we might filter out
        # players who have run out of money.
        self.round_count += 1
        self.round.zero_pot()
        self.old_rounds.append(round) # Append the round object, not self.round
        return players # Return the full list of players for now

    def play_round(self, players: List[Player]) -> Player:
        round = self.start_round(players)

        # Betting Phase 1
        player_turn_index = 0
        logger.warning(f"{round.active_players=}")
        logger.info(f"{players=}, {self.round.pot=}")
        while not round.is_betting_over():
            current_active_players = list(round.active_players) # Get current active884 players
            if not current_active_players: # All folded
                break

            # Ensure player_turn_index is valid for the current list of active players
            player_turn_index %= len(current_active_players)
            current_player = current_active_players[player_turn_index]

            state = self.update_state(round)
            logger.debug(f"play_round {state=}")
            action = current_player.send_action(state)
            self.take_action(current_player, action)

            # Update round's active players and bets
            if action.kind == "FOLD":
                # Remove player from active_players list in the round object
                round.active_players = [p for p in round.active_players if p.name != current_player.name]
            else:
                round.bets[current_player.name] += action.amount

            # If only one player left, they win
            if len(round.active_players) == 1:
                winner = round.active_players[0]
                self.end_round(round, players, winner)
                return winner

            # Move to next player, cycling through remaining active players
            # Only increment if there are still active players to avoid IndexError
            if len(round.active_players) > 0:
                player_turn_index = (player_turn_index + 1) % len(current_active_players)

        # After Betting Phase 1, reset bets for next phase
        round.reset_bets()
        round.last_raiser = None # Reset last raiser for the new betting phase

        # Discard and Draw Phase (only for remaining active players)
        for player in list(round.active_players): # Iterate over a copy as list might change
            if player.name in [p.name for p in round.active_players]: # Ensure player is still active
                discarded_cards = player.discard()
                self.take_discards(discarded_cards)
                self.update_cards(player)

        # Betting Phase 2
        player_turn_index = 0
        # Reset last_raiser for the new betting phase
        round.last_raiser = None
        while not round.is_betting_over():
            current_active_players = list(round.active_players)
            if not current_active_players:
                break

            player_turn_index %= len(current_active_players)
            current_player = current_active_players[player_turn_index]

            state = self.update_state(round)
            action = current_player.send_action(state)
            self.take_action(current_player, action)

            if action.kind == "FOLD":
                round.active_players = [p for p in round.active_players if p.name != current_player.name]
            else:
                round.bets[current_player.name] += action.amount

            if len(round.active_players) == 1:
                winner = round.active_players[0]
                self.end_round(round, players, winner)
                return winner

            if len(round.active_players) > 0:
                player_turn_index = (player_turn_index + 1) % len(round.active_players)

        # Determine winner after all betting phases (if not already determined by folds)
        if len(round.active_players) == 1:
            winner = round.active_players[0]
        elif len(round.active_players) > 1:
            winner = self._showdown(list(round.active_players)) # Call showdown for multiple remaining players
        else: # No active players (everyone folded) - should not happen if previous check is correct
            raise ValueError("No active players left but round not ended by fold")

        self.end_round(round, players, winner)
        return winner

    def take_discards(self, cards: List[Card]) -> None:
        for card in cards:
            self.discard_pile.append(card)

    def update_state(self, round: Round):
        state = round.update_state()
        # logger.debug(f"state in update_state is {state}")
        return state

    def get_state(self, Round: Round):
        return self.update_state(Round)

    def is_valid_action(self, action: Action, state=None) -> bool:
        is_valid = action.is_valid()
        if not is_valid:
            return False
        if not state:
            state = self.update_state(self.round)
        if action == "CALL" and state["amount"] == 0:
            return False
        else:
            return True


def deal_cards(dealer: Dealer,
               players: List[Player]) -> Tuple[Dealer, List[Player]]:
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
    """This can produce a straight flush, of suit random_suit and starting at
    Rank start"""
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
    pprint.pprint(inspect.getsource(function))


def replenish_cards(deck, player):
    """Takes a deck and player as argument. Deals cards to the player,
    until they have five cards again."""
    while len(player.hand) < 5:
        card = deck.deal(num_cards=1)
        player.add_card(card)
        if len(player.hand) == 5:
            pass
    return deck, player
