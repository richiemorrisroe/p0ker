import pytest
from pkr import Rank, Suit


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

def test_rank_ordering() -> bool:
    assert Ace > Deuce

def test_wrong_rank_ordering() -> bool:
    with pytest.raises(AssertionError):
        assert Deuce > Ace

def test_court_cards() -> bool:
    assert Rank(13) > Rank(12) > Rank(11)
