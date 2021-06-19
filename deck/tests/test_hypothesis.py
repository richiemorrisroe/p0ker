import pytest
from typing import List

from hypothesis import given, assume, strategies as st


import deck.pkr
from deck.pkr import Hand, Card, Player, Round, random_hand


@given(rank=st.sampled_from(deck.pkr.Rank),
       suit=st.sampled_from(deck.pkr.Suit))
def test_fuzz_Card(rank, suit) -> None:
    deck.pkr.Card(rank=rank, suit=suit)


@given(cards=st.sets(st.builds(Card)))
def test_fuzz_Hand(cards) -> None:
    assume(len(cards) <= 5)
    deck.pkr.Hand(cards=cards)


@given(hand=st.builds(random_hand))
def test_fuzz_discard_cards(hand: Hand) -> None:
    assume(len(hand) <= 5)
    deck.pkr.discard_cards(hand=hand)


@given(hand=st.builds(random_hand))
def test_fuzz_score_hand(hand) -> None:
    assume(len(hand) <= 5)
    hand.score()


@given(name=st.just("poker"), ante=st.just(100))
def test_fuzz_Dealer(name, ante) -> None:
    deck.pkr.Dealer(name=name, ante=ante)


# @given(name=st.just("poker"), ante=st.just(100), players=st.integers(1, 10))
# def test_fuzz_Dealer_start_game(name, ante, players):
#     dealer = deck.pkr.Dealer(name=name, ante=ante)
#     players = dealer.start_game(integers)

@pytest.mark.slow
@given(name=st.just("poker"), ante=st.just(100), n_players=st.integers(1, 10))
def test_fuzz_Dealer_start_round(name, ante, n_players: int) -> None:
    dealer = deck.pkr.Dealer(name=name, ante=ante)
    players = dealer.start_game(n_players)
    players = dealer.start_round(players)
