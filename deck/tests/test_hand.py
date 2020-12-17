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



def test_fake_hand() -> None:
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
