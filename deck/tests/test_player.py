from pkr import Player, random_hand, Card, Suit, Rank, Dealer
import pytest
def test_player_exists() -> None:
    player = Player()
    assert isinstance(player, Player)


def test_player_hand_score() -> None:
    rhand = random_hand()
    player = Player(hand=rhand)
    assert player.scores() is not None

def test_player_discard_cards() -> None:
    twopair = [Card(Rank(8),Suit(1)), Card(Rank(8), Suit(2)),
            Card(Rank(2), Suit(1) ), Card(Rank(2), Suit(2)),
            Card( Rank(5), Suit(3))]
    player = Player(hand=twopair)
    discard = player.discard()
    keep = player.hand
    assert len(keep)==4 and len(discard)==1

def test_player_bet_amount() -> None:
    p = Player()
    bet = 200
    new_bet = p.bet(bet=bet)
    assert bet == new_bet

def test_player_always_calculate_bet() -> None:
    hand = random_hand()
    p = Player(hand=hand)
    assert p.bet() is not  None

def test_player_bet_always_positive() -> None:
    hand = random_hand()
    p = Player(hand=hand)
    assert p.bet() > 0

def test_player_call() -> None:
    p = Player(hand=random_hand())
    assert p.call() is not None

def test_player_call_true() -> None:
    twopair = [Card(Rank(8),Suit(1)), Card(Rank(8), Suit(2)),
            Card(Rank(2), Suit(1) ), Card(Rank(2), Suit(2)),
            Card( Rank(5), Suit(3))]
    p = Player(hand=twopair)
    assert p.call() is True


def test_player_call_false() -> None:
    testhand = [Card(Rank(2), Suit(1)), Card(Rank(5), Suit(2)),
                Card(Rank(14), Suit(3)), Card(Rank(7), Suit(1)),
                Card(Rank(11), Suit(2))]
    p = Player(hand=testhand)
    assert p.call() is False

def test_player_negative_bet_impossible() -> None:
    hand = [Card(Rank(7), Suit.DIAMONDS),
            Card(Rank(3), Suit.DIAMONDS),
            Card(Rank(13), Suit.SPADES),
            Card(Rank(9), Suit.DIAMONDS),
            Card(Rank(5), Suit.SPADES)]
    player = Player(stash=5077, hand=hand)
    assert player.bet() > 0
    
def test_player_stash_identical() -> None:
    player = Player(stash=100)
    assert player.stash == 100

def test_player_fold() -> None:
    testhand = [Card(Rank(2), Suit(1)), Card(Rank(5), Suit(2)),
                Card(Rank(14), Suit(3)), Card(Rank(7), Suit(1)),
                Card(Rank(11), Suit(2))]
    player = Player(stash=100, hand=testhand)
    assert player.fold() is True

def test_player_fold_false() -> None:
    full_house = [Card(Rank(14), Suit(1)), Card(Rank(14),Suit(2)),
                       Card(Rank(14), Suit(3)), Card(Rank(8),Suit(1)),
                       Card(Rank(8),Suit(2))]
    player = Player(stash=100, hand=full_house)
    assert player.fold() is False

def test_player_stash_default_correct() -> None:
    hand = random_hand()
    player = Player(hand=hand)
    assert player.stash == 5000

def test_player_decide_action():
    hand = random_hand()
    player = Player(hand=hand)
    dealer = Dealer()
    assert player.decide_action(dealer) is not None

def test_player_cannot_go_into_debt() -> None:
    p = Player(stash=100)
    with pytest.raises(ValueError):
        p.bet(101)

def test_player_can_pay() -> None:
    p = Player()
    dealer = Dealer()
    small_blind = dealer.get_blind('small')
    pay_blind = p.pay(small_blind)
    assert pay_blind == small_blind
