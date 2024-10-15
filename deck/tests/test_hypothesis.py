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
    hand.discard()


@given(hand=st.builds(random_hand))
def test_fuzz_score_hand(hand) -> None:
    assume(len(hand) <= 5)
    hand.score()


@given(name=st.just("poker"), ante=st.just(100))
def test_fuzz_Dealer(name, ante) -> None:
    deck.pkr.Dealer(name=name, ante=ante)


@given(name=st.just("poker"), ante=st.just(100), players=st.integers(1, 10))
def test_fuzz_Dealer_start_game(name, ante, players):
    dealer = deck.pkr.Dealer(name=name, ante=ante)
    players = dealer.start_game(players)

@pytest.mark.slow
@given(name=st.just("poker"), ante=st.just(100), n_players=st.integers(1, 10))
def test_fuzz_Dealer_start_round(name, ante, n_players: int) -> None:
    dealer = deck.pkr.Dealer(name=name, ante=ante)
    players = dealer.start_game(n_players)
    round = dealer.start_round(players)


@pytest.mark.slow
@given(name=st.just("poker"), ante=st.just(100), n_players=st.integers(2, 10))
def test_dealer_maintains_total_value_of_stash(name,
                                               ante,
                                               n_players: int) -> None:
    dealer = deck.pkr.Dealer(name=name, ante=ante)
    players = dealer.start_game(n_players)
    round = dealer.start_round(players)
    players = dealer.update_round(players, round)
    stashes = [p.stash for _, p in players.items()]
    pot_value = round.get_pot_value()
    assert sum(stashes) + pot_value == n_players * 5000

    
@given(name=st.just("poker"), ante=st.just(100), n_players=st.integers(2, 10))
def test_dealer_maintains_total_number_of_cards(name,
                                               ante,
                                               n_players: int) -> None:
    dealer = deck.pkr.Dealer(name=name, ante=ante)
    players = dealer.start_game(n_players)
    round = dealer.start_round(players)
    players = dealer.update_round(players, round)
    card_count = [len(p.hand) for _, p in players.items()]
    deck_length = len(dealer.deck)
    discard_pile_length = len(dealer.discard_pile)
    assert sum(card_count) + deck_length + discard_pile_length == 52
    
    
