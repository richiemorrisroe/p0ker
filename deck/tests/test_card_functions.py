from pkr import (Card, Player, Suit, Rank,  Deck, Hand, deal_cards,
                 random_hand, split_cards, count, anyrep,
                 find_repeated_cards, make_straight, is_straight,
                 is_flush, score_hand, make_flush, discard_cards, Game)
def test_deal_cards() -> None:
    p1 = Player()
    p2 = Player()
    list_players = [p1, p2]
    d = Deck()
    cards_in_hand = 5
    d, p = deal_cards(d, list_players)
    p1, p2 = p
    assert len(p1.hand)==5 and len(p2.hand) == 5

def test_game_deal_cards() -> None:
    game = Game()
    p1 = Player()
    p2 = Player()
    list_players = [p1, p2]
    game.deck, players = deal_cards(Game.deck, list_players)
    p1, p2 = players
    assert len(Game.deck) + len(p1.hand) + len(p2.hand) == 52

def test_split_cards() -> None:
    rhand = random_hand() 
    suits, ranks = split_cards(rhand)
    assert len(ranks) and len(suits) == 5

def test_split_cards_suits() -> None:
    rhand = random_hand() 
    suits, ranks = split_cards(rhand)
    assert isinstance(suits[0], Suit)

def test_split_cards_ranks() -> None:
    rhand = random_hand() 
    suits, ranks = split_cards(rhand)
    assert isinstance(ranks[0], Rank)

    
def test_count() -> None:
    hand = Hand([Card(Rank(14), Suit(1)), Card(Rank(14),Suit(2)),
            Card(Rank(14), Suit(3)), Card(Rank(8),Suit(1)),
            Card(Rank(8),Suit(2))])
    suits, ranks = split_cards(hand)
    count_ranks = count(ranks)
    assert max(count_ranks.values()) == 3


def test_repeated_cards() -> None:
    hand = Hand([Card(Rank(14), Suit(1)), Card(Rank(14),Suit(2)),
            Card(Rank(14), Suit(3)), Card(Rank(8),Suit(1)),
            Card(Rank(8),Suit(2))])
    suits, ranks = split_cards(hand)
    reps = find_repeated_cards(ranks)
    assert len(reps)==2

def test_make_straight_is_straight() -> None:
    straight = make_straight(start=5)
    suits, ranks = split_cards(straight)
    assert is_straight(ranks)


def test_straight_has_consecutive_numbers() -> None:
    straight = make_straight(start=5)
    suits, ranks = split_cards(straight)
    ranks_int = [int(rank) for rank in ranks]
    assert ranks_int == [5, 6, 7, 8, 9]

def test_is_flush_correct() -> None:
    flush = make_flush()
    suits, ranks = split_cards(flush)
    assert is_flush(suits)

def test_get_scores_scores_every_hand() -> None:
    rhand = random_hand()
    assert score_hand(rhand) is not None




def test_discard_cards() -> None:
    testhand = [Card(Rank(2), Suit(1)), Card(Rank(2), Suit(2)), Card(Rank(2), Suit(3)),
                Card(Rank(8), Suit(1)), Card(Rank(7), Suit(4))]
    keep, discarded = discard_cards(testhand)
    assert len(keep) == 3 and len(discarded) == 2

def test_discard_cards_nothing() -> None:
    testhand = [Card(Rank(2), Suit(1)), Card(Rank(5), Suit(2)),
                Card(Rank(14), Suit(3)), Card(Rank(7), Suit(1)),
                Card(Rank(11), Suit(2))]
    keep, discarded = discard_cards(testhand)
    assert len(keep) == 2 and len(discarded) == 3

def test_discard_cards_straight() -> None:
    straight = make_straight(5)
    keep, discarded = discard_cards(straight)
    assert len(keep) == 5

def test_discard_cards_flush() -> None:
    flush = make_flush()
    keep, discarded = discard_cards(flush)
    assert len(discarded) == 0
