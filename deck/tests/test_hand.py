# type: ignore
import pytest

from deck.pkr import (
    Card,
    Suit,
    Rank,
    Hand,
    random_suit,
    random_rank,
    random_card,
    random_hand,
    Round,
    make_straight
)


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

def test_hand_scoring() -> None:
    twopair_8_2 = Hand([Card(Rank(8), Suit(1)), Card(Rank(8), Suit(2)),
                    Card(Rank(2), Suit(1)), Card( Rank(2), Suit(2)),
                    Card(Rank(5), Suit(3))])
    twopair_8_3 = Hand([Card(Rank(8), Suit(1)), Card(Rank(8), Suit(2)),
                    Card(Rank(3), Suit(1)), Card( Rank(3), Suit(2)),
                    Card(Rank(5), Suit(3))])
    score_82, name_82 = twopair_8_2.score()
    score_83, name_83 = twopair_8_3.score()
    assert name_82 == 'TWO-PAIR' and name_83 == 'TWO-PAIR'
    assert score_83 > score_82


def test_hand_score_straight_comparison():
    straight5 = make_straight(5)
    straight6 = make_straight(6)
    handscore5, _ = straight5.score()
    handscore6, _ = straight6.score()
    assert handscore6 > handscore5
