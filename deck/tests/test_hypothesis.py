from collections import OrderedDict

import deck.pkr
from deck.pkr import Hand, Card, Player, Round
from hypothesis import given, assume, strategies as st
from typing import List


@given(rank=st.sampled_from(deck.pkr.Rank), suit=st.sampled_from(deck.pkr.Suit))
def test_fuzz_Card(rank, suit) -> None:
    deck.pkr.Card(rank=rank, suit=suit)

# @given(cards=st.dictionaries(Card, int))
# def test_fuzz_Hand(cards) -> None:
#     assume(len(cards)<=5)
#     deck.pkr.Hand(cards=cards)

@given(hand=st.builds(Hand))
def test_fuzz_discard_cards(hand: Hand) -> None:
    assume(len(hand)<=5)
    deck.pkr.discard_cards(hand=hand)

# @given(hand=st.builds(Hand))
# def test_fuzz_score_hand(hand) -> None:
#     assume(len(hand)<=5)
#     hand.score()

@given(name=st.just("poker"), ante=st.just(100))
def test_fuzz_Dealer(name, ante) -> None:
    deck.pkr.Dealer(name=name, ante=ante)

# @given(name=st.just("poker"), ante=st.just(100), players=st.integers(1, 10))
# def test_fuzz_Dealer_start_game(name, ante, players):
#     dealer = deck.pkr.Dealer(name=name, ante=ante)
#     players = dealer.start_game(integers)

@given(name=st.just("poker"), ante=st.just(100), players=st.lists(st.builds(Player)))
def test_fuzz_Dealer_start_round(name, ante, players: List[Player]) -> None:
    dealer = deck.pkr.Dealer(name=name, ante=ante)
    assume(len(players)>1 and len(players)<10)
    players = dealer.start_round(players)
