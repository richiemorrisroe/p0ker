import pytest
from pkr import Rank, Suit


def generate_rank(num):
    rank = deck.Rank(num)
    return rank


def generate_suit(num):
    s = deck.Suit(num)
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


# ace_of_spades = deck.Card(deck.Suit(1), deck.Rank(14))
# def test_suit_and_rank():
#     assert (ace_of_spades == deck.Card(deck.Suit(1), deck.Rank(14)))
    
Ace = deck.Rank(14)
Deuce = deck.Rank(2)

def test_rank_ordering():
    assert Ace > Deuce

def test_wrong_rank_ordering():
    with pytest.raises(AssertionError):
        assert Deuce > Ace

def test_court_cards():
    assert deck.Rank(13) > deck.Rank(12) > deck.Rank(11)
