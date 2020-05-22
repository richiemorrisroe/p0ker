from pkr import (Card, Player, Suit, Rank,  Deck, deal_cards,
                 random_hand, split_cards, count, anyrep,
                 find_repeated_cards, make_straight, is_straight,
                 is_flush, score_hand)
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

def test_split_cards_suits() -> None:
    rhand = random_hand() 
    suits, ranks = split_cards(rhand)
    assert isinstance(ranks[0], Rank)

    
def test_count() -> None:
    hand = [Card(Suit(1), Rank(14)), Card(Suit(2), Rank(14)),
            Card(Suit(3), Rank(14)), Card(Suit(1), Rank(8)),
            Card(Suit(1), Rank(8))]
    suits, ranks = split_cards(hand)
    count_ranks = count(ranks)
    assert max(count_ranks.values()) == 3


def test_repeated_cards() -> None:
    hand = [Card(Suit(1), Rank(14)), Card(Suit(2), Rank(14)),
            Card(Suit(3), Rank(14)), Card(Suit(1), Rank(8)),
            Card(Suit(1), Rank(8))]
    ranks, suits = split_cards(hand)
    reps = find_repeated_cards(ranks)
    assert len(reps)==1

def test_has_straight_only_one_rank() -> None:
    straight = make_straight(Suit(1), start=5)
    ranks, suits = split_cards(straight)
    assert is_straight(ranks)


def test_straight_has_consecutive_numbers() -> None:
    straight = make_straight(Suit(1), start=5)
    suits, ranks = split_cards(straight)
    ranks_int = [int(rank) for rank in ranks]
    assert ranks_int == [5, 6, 7, 8, 9]

def test_is_flush_correct() -> None:
    flush = make_straight(Suit(1), start=5)
    suits, ranks = split_cards(flush)
    assert is_flush(suits)

def test_get_scores_scores_every_hand() -> None:
    rhand = random_hand()
    assert score_hand(rhand) is not None


# def test_make_straight_is_straight() -> None:
#     straight = make_straight(Suit(3))
#     assert is_straight
# def test_score_full_house() -> None:
#     full_house = [Card(Suit(1), Rank(14)), Card(Suit(2), Rank(14)),
#             Card(Suit(3), Rank(14)), Card(Suit(1), Rank(8)),
#             Card(Suit(1), Rank(8))]
#     score, name = score_hand(full_house)
#     assert name == 'FULL-HOUSE'

# def test_score_pair() -> None:
#     pair = [Card(Suit(1), Rank(8)), Card(Suit(2), Rank(8)),
#             Card(Suit(1), Rank(2)), Card(Suit(2), Rank(3)),
#             Card(Suit(3), Rank(5))]
#     score, name = score_hand(pair)
#     assert name == 'PAIR'
    
# def test_score_straight() -> None:
#     straight = make_straight(Suit(1), start=5)
#     score, name = score_hand(straight)
#     assert straight is None
