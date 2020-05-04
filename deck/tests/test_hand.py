import pytest
from pkr import (Card, Suit, Rank, Hand, random_suit, random_rank, random_card,
                 random_hand)
ace_spades = Card(Suit(1), Rank(14))
king_clubs = Card(Suit(2), Rank(13))
hand = Hand([ace_spades, king_clubs])
fake_hand = [1, 2, 3]


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


def test_random_hand() -> None:
    rhand = random_hand()
    assert isinstance(rhand, Hand)
