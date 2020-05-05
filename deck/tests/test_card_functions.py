from pkr import Card, Player, Suit, Rank,  Deck, deal_cards, random_hand, split_cards, count, anyrep
def test_deal_cards() -> None:
    p1 = Player()
    p2 = Player()
    list_players = [p1, p2]
    d = Deck()
    cards_in_hand = 5
    d, p = deal_cards(d, list_players)
    p1, p2 = p
    assert len(p1.hand)==5

def test_split_cards() -> None:
    rhand = random_hand()
    ranks, suits = split_cards(rhand)
    assert len(ranks) and len(suits) == 5

def test_count() -> None:
    hand = [Card(Suit(1), Rank(14)), Card(Suit(2), Rank(14)),
            Card(Suit(3), Rank(14)), Card(Suit(1), Rank(8)),
            Card(Suit(1), Rank(8))]
    ranks, suits = split_cards(hand)
    count_ranks = count(ranks)
    assert max(count_ranks.values()) == 3

# def test_anyrep() -> None:
#     hand = [Card(Suit(1), Rank(14)), Card(Suit(2), Rank(14)),
#             Card(Suit(3), Rank(14)), Card(Suit(1), Rank(8)),
#             Card(Suit(1), Rank(8))]
#     ranks, suits = split_cards(hand)
#     ranks_count = count(ranks)
#     assert anyrep(ranks_count) is True
