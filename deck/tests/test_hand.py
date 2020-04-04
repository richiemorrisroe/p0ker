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


def test_iter_hand() -> bool:
    res = []
    for card in hand:
        res.append(card)
    assert len(res) == len(hand)


def test_random_suit() -> bool:
    assert isinstance(random_suit(), Suit)


def test_random_rank() -> bool:
    assert isinstance(random_rank(), Rank)


def test_random_card() -> bool:
    assert isinstance(random_card(), Card)


def test_random_hand() -> bool:
    assert isinstance(random_hand(), Hand)
#flaky test
def test_hand_uniqueness() -> bool:
    randhand = random_hand()
    assert len(set(randhand.cards)) == len(randhand.cards)
