# type: ignore 
import pytest

from pkr import Card, Deck, Player, Suit, Rank, random_hand, Hand, deal_cards


def test_deck_length() -> None:
    deck = Deck()
    assert len(deck) == 52

def test_deck_deal() -> None:
    deck = Deck()
    card = deck.deal(num_cards = 1)
    assert isinstance(card, Card)


def test_deck_getitem() -> None:
    first_card = Deck()[0]
    assert isinstance(first_card, Card)

def test_deck_deal_hand() -> None:
    d = Deck()
    hand = d.deal(num_cards=5)
    assert len(hand)==5


def test_hand_uniqueness() -> None:
    rhand = random_hand()
    assert len(set(rhand.cards)) == len(rhand.cards)

def test_deck_length_after_dealing() -> None:
    d = Deck()
    cards = d.deal(num_cards=2)
    assert len(d) + len(cards) == 52

def test_negative_number_deal() -> None:
    d = Deck()
    with pytest.raises(ValueError):
        d.deal(-1)

def test_hand_rejects_invalid_card_combinations() -> None:
    invalid_hand = [Card(Rank(2), Suit(1)), Card(Rank(2), Suit(1))]
    with pytest.raises(ValueError):
        Hand(invalid_hand)

def test_deck_deal_one_card() -> None:
    d = Deck()
    cards = d.deal(num_cards=1)
    assert len(d) + len(cards) == 52

def test_deck_shuffle() -> None:
    d = Deck()
    len1 = len(d)
    d.shuffle()
    assert len(d) == len1
