import pytest

from pkr import Card, Deck, Player, random_hand, Hand


def test_deck_length() -> bool:
    deck = Deck()
    assert len(deck) == 52

def test_deck_deal() -> bool:
    deck = Deck()
    card = deck.deal(num_cards = 1)
    assert isinstance(card, Card)


def test_deck_getitem() -> bool:
    first_card = Deck()[0]
    assert isinstance(first_card, Card)

def test_deck_deal_hand() -> bool:
    d = Deck()
    hand = d.deal(num_cards=5)
    assert len(hand)==5
def test_hand_uniqueness() -> bool:
    rhand = random_hand()
    assert len(set(rhand.cards)) == len(rhand.cards)

def test_deck_length_after_dealing() -> bool:
    d = Deck()
    cards = d.deal(num_cards=2)
    assert len(d) + len(cards) == 52
