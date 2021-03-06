
# Table of Contents

1.  [Testing](#org0478493)
    1.  [Next Steps](#orge1b02a2)
        1.  [Add round to dealer object](#orgdd0888d)
    2.  [Design Thoughts](#org87522a4)
        1.  [i need to make some kind of stash object to hold the discarded cards](#org5b48922)
        2.  [should probably exist as something off a Dealer/Game object](#orgefce010)
        3.  [Visualising Code graph](#orgb930b1c)



<a id="org0478493"></a>

# Testing

I need some tests, as I now have no idea what I was getting at before
:(

We'll use pytest, as it has less boilerplate

First, I need to put all my code into a module

I'm going to recreate the entirety of deck.py within a folder called
deck

This will make it easier to set up all the testing and whatnot. 

    from enum import Enum, IntEnum
    import random as random
    
    
    from random import shuffle
    import math as math
    import random as random
    from typing import List,  Dict, Tuple, Optional
    
    
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
        def __init__(self, rank:Rank, suit:Suit):
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
    
        def __len__(self):
            return 1
        
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
            return(result)
    
        
        def __next__(self):
            self.pos += 1
            if self.pos > len(self.cards):
                raise StopIteration
            else:
                return self.cards[self.pos - 1]
    
        def add_card(self, card:Card) -> None:
            self.cards.append(card)
    
        def count(self, suit_or_rank=None):
            """Take either a list of suits of ranks and returns
            a dict with the counts of each. 
            Used as input to checking functions"""
            suits, ranks = self.split_cards()
            if suit_or_rank == 'suits':
                vals = suits
            if suit_or_rank == 'ranks':
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
            Mostly useful for further functions """
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
    
        def is_flush(self) -> bool :
            """Check if a set of suits contains a flush (all suits are the same). 
            Returns True if so, False otherwise. 
            If exact=False, returns the highest count of same suits present. """
            suits, ranks = self.split_cards()
            all_suits = [x for x in suits if isinstance(x, Suit)]
            if len(all_suits) != len(suits):
                raise ValueError('all suits must be of class Suit')
            sc = self.count('suits')
            maxval = max(sc.values())
            if maxval == 5:
                return True
            else:
                return False
    
        def is_straight(self) -> bool:
            suits, ranks = self.split_cards()
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
    
        def find_repeated_cards(self):
            """Check if there are any repeated cards in a list of suits or ranks. 
            Return the elements which are repeated if so, an empty dictionary otherwise"""
            suits, ranks = self.split_cards()
            res = {}
            counts = self.count('ranks')
            for k, v in counts.items():
                if v >= 2:
                    res[k] = v
            return res
    
        def score(self):
            """Return the score of a particular hand. Returns a tuple with the
            name of the hand and the score associated with this hand"""
            hand = Hand(self.cards)
            scores = hand.get_scores()
            suits, ranks = hand.split_cards()
            flush = hand.is_flush()
            straight = hand.is_straight()
            pairs = hand.find_repeated_cards()
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
            
        
    
        
    class Player:
        def __init__(self, hand=None, stash=None, names=["Liam","Emma","Noah",
                                                         "Olivia","William","Ava",
                                                         "James","Isabella",
                                                         "Oliver","Sophia"]):
            if hand is None:
                self.hand = []
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
            length_names = len(names)
            rand_choice = random_choice(0, length_names-1)
            self.name = names[rand_choice]
            
        def __repr__(self):
            fstring = "Player(stash = {stash}, score={score}, hand = {hand})"
            return fstring.format(stash=self.stash,
                                  score=self.score,
                                  hand=self.hand)
    
        def __len__(self):
            return(1)
        
        def scores(self) -> float:
            if len(self.hand) > 0:
                score, sname = Hand(self.hand).score()
                self.score = score
                return self.score
            else:
                return self.score
    
        def discard(self):
            self.hand, discard = discard_cards(self.hand)
            return discard
        
        def bet(self, bet=None) -> float:
            def check_bet(bet, stash):
                if bet > stash:
                    print('got here')
                    raise ValueError('can only bet {max_stash}, you bet {bet}'.format(
                        max_stash=stash,
                        bet=bet))
                else:
                    return bet
                
            if bet:
                bet = check_bet(bet, self.stash)
                return bet
            else:
                bet = 0
                score, name = Hand(self.hand).score()
                print(f'score is {score}')
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
    
        def fold(self) -> bool:
            if not self.score:
                self.score, _ = Hand(self.hand).score()
            if self.score < 100:
                return True
            else:
                return False
    
        def decide_action(self, state=None):
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
    
    
        def pay(self, amount):
            self.stash -= amount
            return amount
    
        def add_card(self, card:Card) -> None:
            if not isinstance(self.hand, Hand):
                self.hand = Hand(self.hand)
            self.hand.add_card(card)
            return None
    
    
    class Dealer:
        def __init__(self, name="poker", ante=100):
            self.name = name
            self.ante = ante
            self.maxdrop = 3
            deck = Deck()
            self.deck = deck
            self.round = None
            self.discard_pile = []
            self.round_count = 0
            
            
    
        def __repr__(self):
            fstring = "Game{name}, ante={ante}, maxdrop={maxdrop},pot={pot}"
            return fstring.format(name=self.name,
                                  ante=self.ante,
                                  maxdrop=self.maxdrop
                                  )
    
    
        def deals(self, players:List[Player]) -> List[Player]:
            """Takes a list of players (normally empty lists)
            and deals each of them five cards,
            returning the updated lists"""
            deck = self.deck
            for i in range(0, 5):
                for player in players:
                    card = deck.deal(num_cards=1)
                    player.add_card(card)
                    print('deck_length:{deck_len}'.format(deck_len=len(deck)))
            return players
            
    
        def update_cards(self, player):
            if len(player)>1:
                raise ValueError('update cards only takes one player, not {x}'.format(x=len(player)))
            deck, player = replenish_cards(self.deck, player)
            self.deck = deck
            return player
    
        
        def compare(self, players):
            scores = {}
            for player in players:
                score, sname = players.hand.score()
                scores[player] = score
                maxscore = max(scores.items)
            return maxscore
    
        def start_round(self, players:List[Player]=None):
            r = Round(self.ante, players)
            self.round = r
            players = self.round.get_blinds(players)
            players = self.deals(players)
            return(r)
    
        def end_round(self, players:List[Player]):
            self.round_count += 1
            
    
        def take_discards(self, cards:List[Card]) -> None:
            for card in cards:
                self.discard_pile.append(card)
    
        def get_pot_value(self):
            val = self.round.get_pot_value()
            return(val)
        
    
        
        def get_blind(self, blind_type):
            return(self.round.get_blind(blind_type))
    
            
        def get_blinds(self, players:List[Player]) -> List[Player]:
            return(self.round.get_blinds(players))
            
        def get_position(self):
            return(self.round.position)
    
        def set_position(self, position):
            self.round.position = position
    
        def update_state(self, round):
            return(round.update_state())
    
        def get_state(self, round):
            return self.update_state(round)
    
    
    
    
    class Round():
        def __init__(self, ante, players:List[Player]):
            self.pot = 0
            self.position = 0
            self.ante = ante
            self.num_players = len(players)
            self.min_bet = ante
    
        def add_to_pot(self, bet):
            self.pot += bet
    
            
        def get_pot_value(self):
            return self.pot
    
        def get_position(self):
            return(self.position)
    
        def set_position(self, position):
            self.position = position
    
        def get_blind(self, blind_type):
            if blind_type == 'small':
                return self.ante
            if blind_type == 'big':
                return self.ante * 2
            else:
                raise NotImplementedError
    
            
        def get_blinds(self, players:List[Player]) -> List[Player]:
            small_blind_pos = 0
            big_blind_pos = 1
            small_blind = self.get_blind('small')
            big_blind = self.get_blind('big')
            sb = players[small_blind_pos].pay(small_blind)
            bb = players[big_blind_pos].pay(big_blind)
            self.add_to_pot(bb+sb)
            return players
    
        def get_minimum_bet(self):
            if not self.min_bet:
                self.min_bet = self.ante
            return(self.min_bet)
        
        def update_state(self):
            sblind = self.get_blind('small')
            lblind = self.get_blind('big')
            potval = self.get_pot_value()
            position = self.get_position()
            min_bet = self.get_minimum_bet()
            return {'small_blind' : sblind,
                    'big_blind': lblind,
                    'pot_value' : potval,
                    'position': position,
                    'min_bet' : min_bet}
    
    
    
    
    def deal_cards(dealer:Dealer, players:List[Player]) -> Tuple[Dealer, List[Player]]:
        """Takes a list of players (normally empty lists)
          and deals each of them five cards,
          returning the updated lists"""
        for i in range(0, 5):
            for player in players:
                card = dealer.deck.deal(num_cards=1)
                player.hand.append(card)
        return dealer, players
    
    
    
    
    
    
    
    
    
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
        random_ranks = random.sample(set(Rank), 5)
        for rank in random_ranks:
            hand.append(Card(rank, suit))
        return Hand(hand)
    
    
    
    
    def print_source(function):
        import inspect
        import pprint
        pprint.pprint(inspect.getsource(function))
    
    
    
    
    def discard_cards(hand:Hand):
        """Discard cards that do not add to the value of the hand. Ignores the
          possibility of straights or flushes. 
          Keeps any pairs etc, otherwise
          keeps the highest numeric cards and discards the rest. 
          In any case, will discard no more than three cards."""
        # if not isinstance(hand, Hand):
        #     hand = Hand(hand)
        suits, ranks = hand.split_cards()
        this_score, handname = hand.score()
        if handname == 'STRAIGHT' or handname == 'FLUSH' or handname == 'STRAIGHT-FLUSH':
            keep = hand.cards
            discard = []
        if handname == 'NOTHING':
            three_cards = random.sample(set(hand), 3)
            keep = [card for card in hand if card not in three_cards]
            discard = [card for card in hand if card in three_cards]
        else:
            keep = []
            discard = []
            for card in hand:
    
                old_score = this_score
                print(f'card is {card}')
                new_hand = Hand([c for c in hand if c != card])
                score_new, _ = new_hand.score()
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
            card = deck.deal(num_cards=1)
            player.hand.append(card)
            if len(player.hand) == 5:
                pass
        return deck, player

    from typing import List
    from collections import defaultdict
    
    
    from .pkr import Hand, random_hand
    
    def generate_hands(n:int) -> List[Hand]:
        manyhands = [random_hand() for _ in range(n)]
        return(manyhands)
    
    def score_hand_distribution(hands:List[Hand]):
        dist = {}
        scores = [hand.score() for hand in hands]
        assert len(scores) == len(hands)
        for score, name in scores:
            try:
                dist[name] += 1
            except KeyError:
                dist[name] = 1
                
        return(dist)

    from deck.pkr import random_hand
    from deck.stats import score_hand_distribution, generate_hands
    
    def test_generate_hands_returns_n_hands() -> None:
        manyhands = generate_hands(n=100)
        assert len(manyhands) == 100
    
    def test_score_hand_dist_returns_all_hands() -> None:
        n = 100
        manyhands = generate_hands(n)
        score_dist = score_hand_distribution(manyhands)
        total_sum = sum(score_dist.values())
        assert total_sum == n
        
        
    def test_count_list_of_hands() -> None:
        manyhands = [random_hand() for x in range(100)]
        hand_dist = score_hand_distribution(manyhands)
        assert hand_dist is not None
    
    def test_score_hand_dist_returns_scores() -> None:
        manyhands = [random_hand() for x in range(100)]
        hand_dist = score_hand_distribution(manyhands)
        assert hand_dist['NOTHING'] > 0

-   We need to create an empty `__init_file.py`  for *reasons*.

    # type: ignore 
    import pytest
    from deck.pkr import Rank, Suit, Card
    
    
    def generate_rank(num) -> Rank:
        rank = Rank(num)
        return rank
    
    
    def generate_suit(num) -> Suit:
        s = Suit(num)
        return s
    
    def test_suit_min():
        with pytest.raises(ValueError):
            suit = generate_suit(0)
    
    def test_suit_max():
        with pytest.raises(ValueError):
            suit = generate_suit(5)
    
    
    def test_rank_min():
        with pytest.raises(ValueError):
            rank = generate_rank(1)
    
    def test_rank_max():
        with pytest.raises(ValueError):
            rank = generate_rank(15)
    
    
    # ace_of_spades = Card(Suit(1), Rank(14))
    # def test_suit_and_rank():
    #     assert (ace_of_spades == Card(Suit(1), Rank(14)))
        
    Ace = Rank(14)
    Deuce = Rank(2)
    
    def test_rank_ordering() -> None:
        assert Ace > Deuce
    
    def test_wrong_rank_ordering() -> None:
        with pytest.raises(AssertionError):
            assert Deuce > Ace
    
    def test_court_cards() -> None:
        assert Rank(13) > Rank(12) > Rank(11)
    
    def test_card_equality() -> None:
        c1 = Card(Rank(14), Suit(1))
        c2 = Card(Rank(14), Suit(1))
        assert c1 == c2
    
    def test_card_notequal() -> None:
        c1 = Card(Rank(14), Suit(1))
        c2 = Card(Rank(14), Suit(2))
        assert c1 != c2
    
    def test_card_wrong_order_fails() -> None:
        with pytest.raises(AssertionError):
            Card(Suit(1), Rank(2))
    
    def test_card_greater_than() -> None:
        c1 = Card(Rank(14), Suit(1))
        c2 = Card(Rank(13), Suit(2))
        assert c1 > c2
    
    def test_card_less_than() -> None:
        c1 = Card(Rank(14), Suit(1))
        c2 = Card(Rank(13), Suit(2))
        assert c2  <   c1

After setting the empty file as above, tests can be ran with the
following incantation:

    pytest --verbosity=1 deck
    pytest --help #for far too much information

    # type: ignore 
    import pytest
    from deck.pkr import (Card, Suit, Rank, Hand, random_suit, random_rank, random_card,
                     random_hand)
    ace_spades = Card(Rank(14), Suit(1))
    king_clubs = Card(Rank(13), Suit(2))
    hand = Hand([ace_spades, king_clubs])
    fake_hand = [1, 2, 3]
    
    def test_repr_hand() -> None:
        hand = random_hand()
        assert isinstance(repr(hand), str)
    
    
    
    def test_fake_hand():
        with pytest.raises(ValueError):
            hand_wrong = Hand(fake_hand)
    
    
    def test_iter_hand() -> None:
        res = []
        for card in hand:
            res.append(card)
        assert len(res) == len(hand)
    
    
    def test_random_suit() -> None:
        assert isinstance(random_suit(), Suit)
    
    
    def test_random_rank() -> None:
        assert isinstance(random_rank(), Rank)
    
    
    def test_random_card() -> None:
        assert isinstance(random_card(), Card)
    
    def test_random_card_suit() -> None:
        c = random_card()
        assert isinstance(c.get_suit(), Suit)
        
    
    def test_random_hand() -> None:
        rhand = random_hand()
        assert isinstance(rhand, Hand)
    
    def test_get_suit() -> None:
        c = Card(Rank(2), Suit(1))
        assert c.get_suit() == Suit(1)
    
    def test_get_rank() -> None:
        c = Card(Rank(2), Suit(1))
        assert c.get_rank() == Rank(2)
    
    def test_get_suit_type() -> None:
        c = random_card()
        assert isinstance(c.get_suit(), Suit)
    
    def test_get_rank_type() -> None:
        c = random_card()
        assert isinstance(c.get_rank(), Rank)    
    
    # def test_hand_get_suits() -> None:
    #     rhand = random_hand()
    #     suits = rhand.get_suits()
    #     assert suits is None

    # type: ignore 
    import pytest
    
    from deck.pkr import Card, Deck, Player, Suit, Rank, random_hand, Hand, deal_cards
    
    
    def test_deck_length() -> None:
        deck = Deck()
        assert len(deck) == 52
    
    def test_deck_deal() -> None:
        deck = Deck()
        card = deck.deal(num_cards = 1)
        assert isinstance(card, Card)
    
    
    def test_deck_getitem() -> None:
        first_card = Deck()[0]
        assert isinstance(first_card, Card)
    
    def test_deck_deal_hand() -> None:
        d = Deck()
        hand = d.deal(num_cards=5)
        assert len(hand)==5
    
    
    def test_hand_uniqueness() -> None:
        rhand = random_hand()
        assert len(set(rhand.cards)) == len(rhand.cards)
    
    def test_deck_length_after_dealing() -> None:
        d = Deck()
        cards = d.deal(num_cards=2)
        assert len(d) + len(cards) == 52
    
    def test_negative_number_deal() -> None:
        d = Deck()
        with pytest.raises(ValueError):
            d.deal(-1)
    
    def test_hand_rejects_invalid_card_combinations() -> None:
        invalid_hand = [Card(Rank(2), Suit(1)), Card(Rank(2), Suit(1))]
        with pytest.raises(ValueError):
            Hand(invalid_hand)
    
    def test_deck_deal_one_card() -> None:
        d = Deck()
        cards = d.deal(num_cards=1)
        assert len(d) + len(cards) == 52
    
    def test_deck_shuffle() -> None:
        d = Deck()
        len1 = len(d)
        d.shuffle()
        assert len(d) == len1 

    from deck.pkr import (Card, Player, Suit, Rank,  Deck, Hand, deal_cards,
                     random_hand, anyrep,
                      make_straight,
                      make_flush, discard_cards, Dealer)
    def test_deal_cards() -> None:
        p1 = Player()
        p2 = Player()
        list_players = [p1, p2]
        d = Dealer()
        cards_in_hand = 5
        d, p = deal_cards(d, list_players)
        p1, p2 = p
        assert len(p1.hand)==5 and len(p2.hand) == 5
    
    # def test_game_deal_cards() -> None:
    #     game = Game()
    #     p1 = Player()
    #     p2 = Player()
    #     list_players = [p1, p2]
    #     game, players = deal_cards(game, list_players)
    #     p1, p2 = players
    #     assert len(game.deck) + len(p1.hand) + len(p2.hand) == 52
    
    def test_split_cards() -> None:
        rhand = random_hand() 
        suits, ranks = rhand.split_cards()
        assert len(ranks) and len(suits) == 5
    
    def test_split_cards_suits() -> None:
        rhand = random_hand() 
        suits, ranks = rhand.split_cards()
        assert isinstance(suits[0], Suit)
    
    def test_split_cards_ranks() -> None:
        rhand = random_hand() 
        suits, ranks = rhand.split_cards()
        assert isinstance(ranks[0], Rank)
    
        
    def test_count() -> None:
        hand = Hand([Card(Rank(14), Suit(1)), Card(Rank(14),Suit(2)),
                Card(Rank(14), Suit(3)), Card(Rank(8),Suit(1)),
                Card(Rank(8),Suit(2))])
        count_ranks = hand.count('ranks')
        assert max(count_ranks.values()) == 3
    
    
    def test_repeated_cards() -> None:
        hand = Hand([Card(Rank(14), Suit(1)), Card(Rank(14),Suit(2)),
                Card(Rank(14), Suit(3)), Card(Rank(8),Suit(1)),
                Card(Rank(8),Suit(2))])
        reps = hand.find_repeated_cards()
        assert len(reps)==2
    
    def test_make_straight_is_straight() -> None:
        straight = make_straight(start=5)
        assert straight.is_straight()
    
    
    def test_straight_has_consecutive_numbers() -> None:
        straight = make_straight(start=5)
        suits, ranks = straight.split_cards()
        ranks_int = [int(rank) for rank in ranks]
        assert ranks_int == [5, 6, 7, 8, 9]
    
    def test_is_flush_correct() -> None:
        flush = make_flush()
        assert flush.is_flush()
    
    def test_get_scores_scores_every_hand() -> None:
        rhand = random_hand()
        rscore, scorename = rhand.score()
        assert rscore is not None
    
    
    
    
    def test_discard_cards() -> None:
        testhand = Hand([Card(Rank(2), Suit(1)), Card(Rank(2), Suit(2)), Card(Rank(2), Suit(3)),
                    Card(Rank(8), Suit(1)), Card(Rank(7), Suit(4))])
        keep, discarded = discard_cards(testhand)
        assert len(keep) == 3 and len(discarded) == 2
    
    def test_discard_cards_nothing() -> None:
        testhand = Hand([Card(Rank(2), Suit(1)), Card(Rank(5), Suit(2)),
                    Card(Rank(14), Suit(3)), Card(Rank(7), Suit(1)),
                    Card(Rank(11), Suit(2))])
        keep, discarded = discard_cards(testhand)
        assert len(keep) == 2 and len(discarded) == 3
    
    def test_discard_cards_straight() -> None:
        straight = make_straight(5)
        keep, discarded = discard_cards(straight)
        assert len(keep) == 5
    
    def test_discard_cards_flush() -> None:
        flush = make_flush()
        keep, discarded = discard_cards(flush)
        assert len(discarded) == 0

    from deck.pkr import Card, Suit, Rank, Hand,  make_straight
    from deck.stats import generate_hands
    def test_score_full_house() -> None:
        full_house = Hand([Card(Rank(14), Suit(1)), Card(Rank(14),Suit(2)),
                           Card(Rank(14), Suit(3)), Card(Rank(8),Suit(1)),
                           Card(Rank(8),Suit(2))])
        score, name = full_house.score()
        assert name == 'FULL-HOUSE'
    
    def test_score_pair() -> None:
        pair = Hand([Card(Rank(8),Suit(1)), Card(Rank(8), Suit(2)),
                     Card(Rank(2), Suit(1)), Card( Rank(3), Suit(2)),
                     Card(Rank(5), Suit(3))])
        score, name = pair.score()
        assert name == 'PAIR'
        
    def test_score_straight() -> None:
        straight = make_straight(start=5)
        score, name = straight.score()
        ## make straight sometimes returns a straight flush
        assert name.startswith('STRAIGHT')
    
    def test_score_straight_flush() -> None:
        straight_flush = Hand([Card( Rank(7),Suit(1)),  Card(Rank(8),Suit(1)),
                               Card(Rank(9), Suit(1)), Card( Rank(10), Suit(1)),
                               Card(Rank(11), Suit(1))])
        score, name = straight_flush.score()
        assert name == 'STRAIGHT-FLUSH'
    
    def test_score_three_of_a_kind() -> None:
        three_of_a_kind = Hand([Card(Rank(14), Suit(1)), Card( Rank(14), Suit(2)),
                                Card(Rank(14), Suit(3)), Card( Rank(3), Suit(1)),
                                Card(Rank(5), Suit(1))])
        score, name = three_of_a_kind.score()
        assert name == 'THREE-OF-A-KIND'
    
    def test_score_twopair() -> None:
        twopair = Hand([Card(Rank(8), Suit(1)), Card(Rank(8), Suit(2)),
                        Card(Rank(2), Suit(1)), Card( Rank(2), Suit(2)),
                        Card(Rank(5), Suit(3))])
        score, name = twopair.score()
        assert name == 'TWO-PAIR'
    
    def test_all_hands_can_be_scored() -> None:
        n = 1000
        manyhands = generate_hands(n)
        scores = [hand.score() for hand in manyhands]
        assert len(scores) == n

    from deck.pkr import Player, random_hand, Card, Suit, Rank, Dealer
    import pytest
    def test_player_exists() -> None:
        player = Player()
        assert isinstance(player, Player)
    
    
    def test_player_hand_score() -> None:
        rhand = random_hand()
        player = Player(hand=rhand)
        assert player.scores() is not None
    
    def test_player_discard_cards() -> None:
        twopair = [Card(Rank(8),Suit(1)), Card(Rank(8), Suit(2)),
                Card(Rank(2), Suit(1) ), Card(Rank(2), Suit(2)),
                Card( Rank(5), Suit(3))]
        player = Player(hand=twopair)
        discard = player.discard()
        keep = player.hand
        assert len(keep)==4 and len(discard)==1
    
    def test_player_bet_amount() -> None:
        p = Player()
        bet = 200
        new_bet = p.bet(bet=bet)
        assert bet == new_bet
    
    def test_player_always_calculate_bet() -> None:
        hand = random_hand()
        p = Player(hand=hand)
        assert p.bet() is not  None
    
    def test_player_bet_always_positive() -> None:
        hand = random_hand()
        p = Player(hand=hand)
        assert p.bet() > 0
    
    def test_player_call() -> None:
        p = Player(hand=random_hand())
        assert p.call() is not None
    
    def test_player_call_true() -> None:
        twopair = [Card(Rank(8),Suit(1)), Card(Rank(8), Suit(2)),
                Card(Rank(2), Suit(1) ), Card(Rank(2), Suit(2)),
                Card( Rank(5), Suit(3))]
        p = Player(hand=twopair)
        assert p.call() is True
    
    
    def test_player_call_false() -> None:
        testhand = [Card(Rank(2), Suit(1)), Card(Rank(5), Suit(2)),
                    Card(Rank(14), Suit(3)), Card(Rank(7), Suit(1)),
                    Card(Rank(11), Suit(2))]
        p = Player(hand=testhand)
        assert p.call() is False
    
    def test_player_negative_bet_impossible() -> None:
        hand = [Card(Rank(7), Suit.DIAMONDS),
                Card(Rank(3), Suit.DIAMONDS),
                Card(Rank(13), Suit.SPADES),
                Card(Rank(9), Suit.DIAMONDS),
                Card(Rank(5), Suit.SPADES)]
        player = Player(stash=5077, hand=hand)
        assert player.bet() > 0
        
    def test_player_stash_identical() -> None:
        player = Player(stash=100)
        assert player.stash == 100
    
    def test_player_fold() -> None:
        testhand = [Card(Rank(2), Suit(1)), Card(Rank(5), Suit(2)),
                    Card(Rank(14), Suit(3)), Card(Rank(7), Suit(1)),
                    Card(Rank(11), Suit(2))]
        player = Player(stash=100, hand=testhand)
        assert player.fold() is True
    
    def test_player_fold_false() -> None:
        full_house = [Card(Rank(14), Suit(1)), Card(Rank(14),Suit(2)),
                           Card(Rank(14), Suit(3)), Card(Rank(8),Suit(1)),
                           Card(Rank(8),Suit(2))]
        player = Player(stash=100, hand=full_house)
        assert player.fold() is False
    
    def test_player_stash_default_correct() -> None:
        hand = random_hand()
        player = Player(hand=hand)
        assert player.stash == 5000
    
    def test_player_decide_action():
        hand = random_hand()
        player = Player(hand=hand)
        dealer = Dealer()
        assert player.decide_action(dealer) is not None
    
    def test_player_cannot_go_into_debt() -> None:
        p = Player(stash=100)
        with pytest.raises(ValueError):
            p.bet(101)
    
    def test_player_can_pay() -> None:
        p1 = Player()
        p2 = Player()
        dealer = Dealer()
        round = dealer.start_round([p1, p2])
        small_blind = round.get_blind('small')
        pay_blind = p1.pay(small_blind)
        assert pay_blind == small_blind
    
    
    def test_player_add_card_to_hand() -> None:
        p = Player()
        c = Card(Rank(2), Suit(1))
        p.add_card(c)
        assert len(p.hand) == 1
    
    def test_player_send_action() -> None:
        p1 = Player()
        p2 = Player()
        dealer = Dealer()
        p1, p2 = dealer.deals([p1, p2])
        action = p1.decide_action()
        assert action in ['CALL', 'BET', 'FOLD', 'RAISE']
    
    def test_player_has_name() -> None:
        p1 = Player()
        assert p1.name is not None
    
    def test_different_players_have_different_names() -> None:
        p1 = Player()
        p2 = Player()
        assert p1.name != p2.name

    from deck.pkr import Dealer, Deck, Player, deal_cards, random_choice, Round
    import pytest
    def test_dealer_is_dealer() -> None:
        dealer = Dealer()
        assert isinstance(dealer, Dealer)
    
    def test_dealer_has_deck() -> None:
        dealer = Dealer()
        assert isinstance(dealer.deck, Deck)
    
    def test_dealer_pot_is_zero() -> None:
        dealer = Dealer()
        p1 = Player()
        p2 = Player()
        round = dealer.start_round([p1, p2])
        pot = round.get_pot_value()
        assert pot == 300
    
    def test_dealer_deal_cards() -> None:
        p1 = Player()
        p2 = Player()
        lp = [p1, p2]
        dealer = Dealer()
        original_len = len(dealer.deck)
        list_players = dealer.deals(lp)
        p1, p2 = list_players
        assert len(dealer.deck) == 42
    
    def test_dealer_discard_pile_exists() -> None:
        d = Dealer()
        assert d.discard_pile is not None
    
    
    def test_dealer_discard_pile_update() -> None:
        d = Dealer()
        p1 = Player()
        p2 = Player()
        p1, p2 = d.deals([p1, p2])
        discard = p1.discard()
        len_discard = len(discard)
        d.take_discards(discard)
        assert len(d.discard_pile) == len_discard
    
    
    
    
    
    
    
    
    
    def test_dealer_ask_for_action() -> None:
        dealer = Dealer()
        p1 = Player()
        p2 = Player()
        p3 = Player()
        list_players = [p1, p2, p3]
        round = dealer.start_round(list_players)
        p1_action = p1.decide_action(dealer)
        p2_action = p2.decide_action(dealer)
        p3_action = p3.decide_action(dealer)
        assert all([p1_action, p2_action, p3_action]) is not  None
    
    
    
    
    
    
    
    
    
        
    def test_dealer_update_cards() -> None:
        p1 = Player()
        dealer = Dealer()
        p1 = dealer.update_cards(p1)
        assert len(p1.hand) == 5
    
    def test_dealer_update_cards_two_player() -> None:
        p1 = Player()
        p2 = Player()
        dealer = Dealer()
        with pytest.raises(ValueError):
            dealer.update_cards([p1, p2])
    
        
        
    def test_dealer_keeps_track_of_completed_rounds() -> None:
        dealer = Dealer()
        p1 = Player()
        p2 = Player()
        dealer.start_round([p1, p2])
        assert dealer.round_count is not None

    from deck.pkr import Round, Dealer, Player, random_choice
    
    
    def test_dealer_round_is_round() -> None:
        dealer = Dealer()
        p1 = Player()
        p2 = Player()
        round =  dealer.start_round([p1, p2])
        assert isinstance(round, Round)
    
    def test_round_exists() -> None:
        p1 = Player()
        p2 = Player()
        r = Round(100, [p1, p2])
        assert r is not None
    
    
    
    def test_dealer_set_blind() -> None:
        dealer = Dealer()
        p1 = Player()
        p2 = Player()
        round = dealer.start_round([p1, p2])
        small_blind = round.get_blind('small')
        big_blind = round.get_blind('big')
        assert big_blind > small_blind
    
    def test_round_get_blind() -> None:
        dealer = Dealer()
        p1 = Player()
        p2 = Player()
        p3 = Player()
        list_players = [p1, p2, p3]
        round = dealer.start_round(list_players)
        assert round.get_pot_value() == 300
    
    def test_dealer_has_state() -> None:
        p1 = Player()
        p2 = Player()
        
        dealer = Dealer()
        round = dealer.start_round([p1, p2])
        state = dealer.get_state(round)
        assert state is not None
    
    
    def test_round_state_is_dict() -> None:
        p1 = Player()
        p2 = Player()
        p3 = Player()
        dealer = Dealer()
        round = dealer.start_round([p1, p2, p3])
        state = dealer.get_state(round)
        assert isinstance(state, dict)
    
    
    def test_round_state_has_pot_value() -> None:
        dealer = Dealer()
        p1 = Player()
        p2 = Player()
        round = dealer.start_round([p1, p2])
        state = dealer.get_state(round)
        assert state['pot_value'] is not None
    
    def test_round_pot_value_state() -> None:
        dealer = Dealer()
        p1 = Player()
        p2 = Player()
        p3 = Player()
        list_players = [p1, p2, p3]
        round = dealer.start_round(list_players)
        state = dealer.get_state(round)
        assert state['pot_value'] == 300
    
    
    def test_round_state_has_player_pos() -> None:
        dealer = Dealer()
        p1 = Player()
        p2 = Player()
        p3 = Player()
        round = dealer.start_round([p1, p2, p3])
        state = dealer.get_state(round)
        assert state['position'] is not None
    
    
    def test_round_set_position() -> None:
        
        dealer = Dealer()
        p1 = Player()
        p2 = Player()
        list_players = [p1, p2]
        pos = random_choice(0, len(list_players))
        round = dealer.start_round(list_players)
        round.set_position(pos)
        assert dealer.get_state(round)['position'] == pos
    
    
    def test_round_takes_a_list_of_players() -> None:
        dealer = Dealer()
        p1 = Player()
        p2 = Player()
        p3 = Player()
        round = dealer.start_round([p1, p2, p3])
        assert round is not None
    
    def test_round_returns_players_with_hands() -> None:
        dealer = Dealer()
        p1 = Player()
        p2 = Player()
        p3 = Player()
        round = dealer.start_round([p1, p2, p3])
        assert (len(p1.hand) == 5 and len(p2.hand) == 5
                and len(p3.hand) == 5)
    
    def test_round_has_minimum_bet() -> None:
        dealer = Dealer()
        p1 = Player()
        p2 = Player()
        p3 = Player()
        round  = dealer.start_round([p1, p2, p3])
        assert dealer.get_state(round)['min_bet'] is not None


<a id="orge1b02a2"></a>

## Next Steps


<a id="orgdd0888d"></a>

### DONE Add round to dealer object

1.  DONE small blind

2.  DONE large blind

3.  DONE deal cards to players

    -   Wrap up all of these functions into a start round one, which returns players with Hands

4.  send players state so they can decide action

    -   have player decide on action based on state
    -   internal state (cards held)
    -   external state (position, pot value, actions of other players)

5.  DONE Fix hand API

    -   have a hand class
    -   also have a bunch of functions that act on hand objects
    -   should join them together in holy matrimony/encapsulation
    
    1.  TODO deal<sub>cards</sub> apparently isn't used anywhere, delete
    
    2.  Player Updates
    
        1.  Change player function names to calculate<sub>bet</sub>, call etc
        
        2.  Make use of state object to decide action
    
    3.  Dealer Updates
    
        1.  Add dealer get action function
        
        2.  Add dealer logic for round structure
        
        3.  Add dealing of cards to start<sub>round</sub>
    
    4.  Deck Object
    
        1.  Move discard pile to deck object
        
        2.  Move replenish<sub>cards</sub> and update<sub>cards</sub> to dealer object
    
    5.  Round Structure
    
        1.  bet/call/fold in order
        
        2.  discard cards
        
        3.  get new cards
        
        4.  bet/call/fold in order
        
        5.  finish round
        
            -   award pot
            -   reset deck and cards
            -   log player/dealer state


<a id="org87522a4"></a>

## Design Thoughts

-   I can see that the deal<sub>cards</sub> API is not great
-   I have to do lots of jiggery-pokery to actually run the test
-   it's much harder than for the other functions

-   I probably need a dealer abstraction to hold the deck and the discard pile.
-   in general, i could probably just call the Deck with the players to deal
-   note that the rules for dealing differ based on the stage of the game
-   Useful overview of basic rules [here](https://www.bigfishgames.com/blog/casino/poker-guide/poker-gameplay/)
-   seems that cards will always be dealt one at a time to each player
-   normally around to the left
-   this is connected to the blind
-   need to account for this logic somewhere
-   seems like blinds, cards and betting should be handled by my hypothetical dealer object
-   but first I need test coverage for what exists now
-   split<sub>cards</sub> is incredibly awkward. Multiple unpacking returns are a dangerous thing.
-   score<sub>hand</sub> has the same multiple return problem
-   i'd like some way to generate random hands with particular sets of
    cards like make(two-pair)
-   this would help with all the repetition in test\\<sub>score</sub>\\<sub>hand</sub>

-   Discard cards needs some love:


<a id="org5b48922"></a>

### DONE i need to make some kind of stash object to hold the discarded cards


<a id="orgefce010"></a>

### DONE should probably exist as something off a Dealer/Game object


<a id="orgb930b1c"></a>

### Visualising Code graph

Found a useful article, with the following instructions

    pip install git+https://github.com/ttylec/pyan
    alias pygraph='find . -iname "*.py" | xargs pyan --dot --colored --no-defines --grouped | dot -Tpng -Granksep=1.5 > graph.png'

I've done this in the pkr virtual env, and it produced a file, graph.png

    cd deck
    pygraph

The resulting graph seems useful.
I should figure out how to do this for R and other languages. 

