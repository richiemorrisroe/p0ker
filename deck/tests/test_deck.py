import pytest

from pkr import Card, Deck, Player


def test_deck_length() -> int:
    deck = Deck()
    assert len(deck) == 52


def test_deck_deal() -> bool:
    deck = Deck()
    card = deck.deal()
    assert isinstance(card, Card)


def test_deck_length() -> bool:
    d = Deck()
    assert (len(d) == 52)


def test_deck_getitem() -> bool:
    first_card = Deck()[0]
    assert isinstance(first_card, Card)

def test_deck_deal_hand() -> bool:
    assert isinstance(Deck.deal(), Card)
    
def test_hand_uniqueness() -> bool:
    random_hand = random_hand()
    assert len(set(random_hand.cards)) == len(random_hand.cards)
