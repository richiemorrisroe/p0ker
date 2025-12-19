import pytest
from typing import List

from hypothesis import given, assume, strategies as st


import deck.pkr
from deck.pkr import Hand, Card, Player, Round, Rank, Suit, random_hand

card_strategy = st.builds(Card, rank=st.sampled_from(Rank),
                          suit=st.sampled_from(Suit))
# This hand_strategy generates hands with unique cards within themselves,
# but does not model drawing from a single 52-card deck without replacement.
# For tests requiring this constraint (e.g., multi-player games or deck interactions),
# a more sophisticated strategy (e.g., using st.composite to draw from a deck)
# will be necessary.
hand_strategy = st.lists(card_strategy, unique_by=lambda c: (c.rank, c.suit),
                         min_size=0, max_size=5).map(Hand)


@given(rank=st.sampled_from(deck.pkr.Rank),
       suit=st.sampled_from(deck.pkr.Suit))
def test_fuzz_Card(rank, suit) -> None:
    deck.pkr.Card(rank=rank, suit=suit)


@given(cards=st.sets(card_strategy, max_size=5))
def test_fuzz_Hand(cards) -> None:
    assume(len(cards) <= 5)
    # Convert the set of cards to a list before passing to Hand
    deck.pkr.Hand(cards=list(cards))


@given(hand=hand_strategy)
def test_fuzz_discard_cards(hand: Hand) -> None:
    assume(len(hand) <= 5)
    hand.discard()


@given(hand=hand_strategy)
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
    _ = dealer.start_round(players)


@pytest.mark.slow
@given(name=st.just("poker"), ante=st.just(100), n_players=st.integers(2, 10))
def test_dealer_maintains_total_value_of_stash(name,
                                               ante,
                                               n_players: int) -> None:
    dealer = deck.pkr.Dealer(name=name, ante=ante)
    players = dealer.start_game(n_players)
    round = dealer.start_round(players)
    players = dealer.update_round(players, round)
    stashes = [p.stash for p in players]
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
    card_count = [len(p.hand) for p in players]
    deck_length = len(dealer.deck)
    discard_pile_length = len(dealer.discard_pile)
    assert sum(card_count) + deck_length + discard_pile_length == 52

## need to re-use cards to make this work for 5+ players    
# @pytest.mark.slow
# @given(name=st.just("poker"), ante=st.just(100), n_players=st.integers(2, 4))
# def test_fuzz_dealer_play_round_maintains_consistent_stashes(name, ante, n_players: int) -> None:
#     dealer = deck.pkr.Dealer(name=name, ante=ante)
#     players = dealer.start_game(n_players)
#     original_stash = [p.stash for p in players]
#     r = dealer.start_round(players)
#     winner = dealer.play_round(players)
#     final_stash = [p.stash for p in players]
#     assert sum(original_stash) == sum(final_stash)

