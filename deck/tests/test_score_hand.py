from pkr import Card, Suit, Rank, Hand, score_hand, make_straight
def test_score_full_house() -> None:
    full_house = Hand([Card(Rank(14), Suit(1)), Card(Rank(14),Suit(2)),
                       Card(Rank(14), Suit(3)), Card(Rank(8),Suit(1)),
                       Card(Rank(8),Suit(2))])
    score, name = score_hand(full_house)
    assert name == 'FULL-HOUSE'

def test_score_pair() -> None:
    pair = Hand([Card(Rank(8),Suit(1)), Card(Rank(8), Suit(2)),
                 Card(Rank(2), Suit(1)), Card( Rank(3), Suit(2)),
                 Card(Rank(5), Suit(3))])
    score, name = score_hand(pair)
    assert name == 'PAIR'
    
def test_score_straight() -> None:
    straight = make_straight(start=5)
    score, name = score_hand(straight)
    ## make straight sometimes returns a straight flush
    assert name.startswith('STRAIGHT')

def test_score_straight_flush() -> None:
    straight_flush = Hand([Card( Rank(7),Suit(1)),  Card(Rank(8),Suit(1)),
                           Card(Rank(9), Suit(1)), Card( Rank(10), Suit(1)),
                           Card(Rank(11), Suit(1))])
    score, name = score_hand(straight_flush)
    assert name == 'STRAIGHT-FLUSH'

def test_score_three_of_a_kind() -> None:
    three_of_a_kind = Hand([Card(Rank(14), Suit(1)), Card( Rank(14), Suit(2)),
                            Card(Rank(14), Suit(3)), Card( Rank(3), Suit(1)),
                            Card(Rank(5), Suit(1))])
    score, name = score_hand(three_of_a_kind)
    assert name == 'THREE-OF-A-KIND'

def test_score_twopair() -> None:
    twopair = Hand([Card(Rank(8), Suit(1)), Card(Rank(8), Suit(2)),
                    Card(Rank(2), Suit(1)), Card( Rank(2), Suit(2)),
                    Card(Rank(5), Suit(3))])
    score, name = score_hand(twopair)
    assert name == 'TWO-PAIR'