import pytest
from pkr import Card, Suit, Rank, Hand
ace_spades =Card(Suit(1), Rank(14))
king_clubs = Card(Suit(2), Rank(13))
hand = Hand([ace_spades, king_clubs])
fake_hand = [1, 2, 3]
hand_wrong = Hand(fake_hand)
def test_hand():
    all_cards = [x for x in hand if x is Card]
    assert len(all_cards)==len(hand)


def test_fake_hand():
    with pytest.raises(ValueError):
        h = Hand(fake_hand)
