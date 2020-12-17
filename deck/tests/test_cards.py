# type: ignore 
import pytest
from deck.pkr import Rank, Suit, Card, Round


def generate_rank(num) -> Rank:
    rank = Rank(num)
    return rank


def generate_suit(num) -> Suit:
    s = Suit(num)
    return s

def test_suit_min() -> None:
    with pytest.raises(ValueError):
        suit = generate_suit(0)

def test_suit_max() -> None:
    with pytest.raises(ValueError):
        suit = generate_suit(5)


def test_rank_min() -> None:
    with pytest.raises(ValueError):
        rank = generate_rank(1)

def test_rank_max() -> None:
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
