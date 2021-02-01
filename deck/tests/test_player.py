from deck.pkr import Player, random_hand, Card, Suit, Rank, Dealer, Hand, Round
import pytest


def test_player_exists() -> None:
    player = Player()
    assert isinstance(player, Player)


def test_player_hand_score() -> None:
    rhand = random_hand()
    player = Player(hand=rhand)
    assert player.scores() is not None


def test_player_discard_cards() -> None:
    twopair = [
        Card(Rank(8), Suit(1)),
        Card(Rank(8), Suit(2)),
        Card(Rank(2), Suit(1)),
        Card(Rank(2), Suit(2)),
        Card(Rank(5), Suit(3)),
    ]
    player = Player(hand=twopair)
    discard = player.discard()
    keep = player.hand
    assert len(keep) == 4 and len(discard) == 1


def test_player_bet_amount() -> None:
    p = Player()
    bet = 200
    new_bet = p.bet(bet=bet)
    assert bet == new_bet


def test_player_always_calculate_bet() -> None:
    hand = random_hand()
    p = Player(hand=hand)
    assert p.bet() is not None


def test_player_bet_always_positive() -> None:
    hand = random_hand()
    p = Player(hand=hand)
    assert p.bet() > 0


def test_player_call() -> None:
    p = Player(hand=random_hand())
    assert p.call() is not None


def test_player_call_true() -> None:
    twopair = [
        Card(Rank(8), Suit(1)),
        Card(Rank(8), Suit(2)),
        Card(Rank(2), Suit(1)),
        Card(Rank(2), Suit(2)),
        Card(Rank(5), Suit(3)),
    ]
    p = Player(hand=twopair)
    assert p.call() is True


def test_player_call_false() -> None:
    testhand = [
        Card(Rank(2), Suit(1)),
        Card(Rank(5), Suit(2)),
        Card(Rank(14), Suit(3)),
        Card(Rank(7), Suit(1)),
        Card(Rank(11), Suit(2)),
    ]
    p = Player(hand=testhand)
    assert p.call() is False


def test_player_negative_bet_impossible() -> None:
    hand = [
        Card(Rank(7), Suit.DIAMONDS),
        Card(Rank(3), Suit.DIAMONDS),
        Card(Rank(13), Suit.SPADES),
        Card(Rank(9), Suit.DIAMONDS),
        Card(Rank(5), Suit.SPADES),
    ]
    player = Player(stash=5077, hand=hand)
    assert player.bet() > 0


def test_player_stash_identical() -> None:
    player = Player(stash=100)
    assert player.stash == 100


def test_player_fold() -> None:
    testhand = [
        Card(Rank(2), Suit(1)),
        Card(Rank(5), Suit(2)),
        Card(Rank(14), Suit(3)),
        Card(Rank(7), Suit(1)),
        Card(Rank(11), Suit(2)),
    ]
    player = Player(stash=100, hand=testhand)
    assert player.fold() is True


def test_player_fold_false() -> None:
    full_house = [
        Card(Rank(14), Suit(1)),
        Card(Rank(14), Suit(2)),
        Card(Rank(14), Suit(3)),
        Card(Rank(8), Suit(1)),
        Card(Rank(8), Suit(2)),
    ]
    player = Player(stash=100, hand=full_house)
    assert player.fold() is False


def test_player_stash_default_correct() -> None:
    hand = random_hand()
    player = Player(hand=hand)
    assert player.stash == 5000


def test_player_decide_action() -> None:
    hand = random_hand()
    player = Player(hand=hand)
    p2 = Player()
    dealer = Dealer()
    round = dealer.start_round([player, p2])
    state = dealer.get_state(round)
    assert player.decide_action(state) is not None


def test_player_cannot_go_into_debt() -> None:
    p = Player(stash=100)
    with pytest.raises(ValueError):
        p.bet(101)


def test_player_can_pay() -> None:
    p1 = Player()
    p2 = Player()
    dealer = Dealer()
    round = dealer.start_round([p1, p2])
    small_blind = round.get_blind("small")
    pay_blind = p1.pay(small_blind)
    assert pay_blind == small_blind


def test_player_add_card_to_hand() -> None:
    p = Player()
    c = Card(Rank(2), Suit(1))
    p.add_card(c)
    assert len(p.hand) == 1


def test_player_send_action() -> None:
    dealer = Dealer()
    p1, p2 = dealer.start_game(2)
    p1, p2 = dealer.deals([p1, p2])
    action = p1.decide_action()
    assert action["action"] in ["CALL", "BET", "FOLD", "RAISE"]


def test_player_has_name() -> None:
    dealer = Dealer()
    list_players = dealer.start_game(2)
    assert list_players[0].name is not None


def test_different_players_have_different_names() -> None:
    dealer = Dealer()
    list_players = dealer.start_game(2)
    p1, p2 = list_players
    assert p1.name != p2.name


def test_player_action_response_is_dict() -> None:
    dealer = Dealer()
    list_players = dealer.start_game(3)
    round = dealer.start_round(list_players)
    state = dealer.update_state(round)
    p1, p2, p3 = list_players
    action = p1.send_action(state)
    assert isinstance(action, dict)


def test_player_can_have_predetermined_hand() -> None:
    full_house = Hand(
        [
            Card(Rank(14), Suit(1)),
            Card(Rank(14), Suit(2)),
            Card(Rank(14), Suit(3)),
            Card(Rank(8), Suit(1)),
            Card(Rank(8), Suit(2)),
        ]
    )
    twopair = Hand(
        [
            Card(Rank(8), Suit(1)),
            Card(Rank(8), Suit(2)),
            Card(Rank(2), Suit(1)),
            Card(Rank(2), Suit(2)),
            Card(Rank(5), Suit(3)),
        ]
    )
    p1 = Player(hand=full_house)
    p2 = Player(hand=twopair)
    dealer = Dealer()
    round = dealer.start_round([p1, p2])
    assert p1.hand == full_house  # and p2.hand == twopair


def test_player_hand_has_class_hand() -> None:
    full_house = Hand(
        [
            Card(Rank(14), Suit(1)),
            Card(Rank(14), Suit(2)),
            Card(Rank(14), Suit(3)),
            Card(Rank(8), Suit(1)),
            Card(Rank(8), Suit(2)),
        ]
    )
    p1 = Player(hand=full_house)
    p2 = Player()
    dealer = Dealer()
    round = dealer.start_round([p1, p2])
    assert isinstance(p1.hand, Hand) and isinstance(p2.hand, Hand)


# def test_player_calls_if_has_good_hand() -> None:
#     full_house = Hand(
#         [
#             Card(Rank(14), Suit(1)),
#             Card(Rank(14), Suit(2)),
#             Card(Rank(14), Suit(3)),
#             Card(Rank(8), Suit(1)),
#             Card(Rank(8), Suit(2)),
#         ]
#     )
#     twopair = Hand(
#         [
#             Card(Rank(8), Suit(1)),
#             Card(Rank(8), Suit(2)),
#             Card(Rank(2), Suit(1)),
#             Card(Rank(2), Suit(2)),
#             Card(Rank(5), Suit(3)),
#         ]
#     )
#     p1 = Player(hand=full_house)
#     p2 = Player(hand=twopair)
#     dealer = Dealer()
#     dealer.start_game([p1, p2])
#     round = dealer.start_round([p1, p2])
#     state = dealer.get_state(round)
#     p1_action = p1.send_action(state)
#     p2_action = p2.send_action(state)
#     assert p1_action["actions"]['action'] and p2_action["actions"]["action"] == "CALL"


def test_round_adds_player_state() -> None:
    dealer = Dealer()
    list_players = dealer.start_game(3)
    round = dealer.start_round(list_players)
    state = dealer.get_state(round)
    p1, p2, p3 = list_players
    action = p1.decide_action(state)
    assert p1.send_action(state) is not None
