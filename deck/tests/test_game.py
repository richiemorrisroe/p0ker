from deck.pkr import Dealer, Deck, Player, deal_cards, random_choice, Round
import pytest


def test_dealer_is_dealer() -> None:
    dealer = Dealer()
    assert isinstance(dealer, Dealer)


def test_dealer_has_deck() -> None:
    dealer = Dealer()
    assert isinstance(dealer.deck, Deck)


def test_dealer_pot_is_zero() -> None:
    dealer = Dealer()
    p1, p2 = dealer.start_game(2)
    list_players = [p1, p2]
    round = dealer.start_round(list_players)
    pot = round.get_pot_value()
    assert pot == dealer.ante * len(list_players)


def test_dealer_deal_cards() -> None:
    p1 = Player()
    p2 = Player()
    lp = [p1, p2]
    dealer = Dealer()
    original_len = len(dealer.deck)
    list_players = dealer.deals(lp)
    p1, p2 = list_players
    assert len(dealer.deck) == 42


def test_dealer_discard_pile_exists() -> None:
    d = Dealer()
    assert d.discard_pile is not None


def test_dealer_discard_pile_update() -> None:
    d = Dealer()
    p1 = Player()
    p2 = Player()
    p1, p2 = d.deals([p1, p2])
    discard = p1.discard()
    len_discard = len(discard)
    d.take_discards(discard)
    assert len(d.discard_pile) == len_discard


def test_round_state_gets_updated() -> None:
    d = Dealer()
    p1, p2 = d.start_game(2)
    lp = d.start_round([p1, p2])
    state = d.get_state(lp)
    from pprint import pprint

    pprint(state)
    assert state is not None


def test_round_update_state() -> None:
    dealer = Dealer()
    list_players = dealer.start_game(n_players=3)
    round = dealer.start_round(list_players)
    player_1, player_2, player_3 = list_players
    state1 = round.update_state()
    dealer.take_action(player_1)
    state2 = round.update_state()
    assert state2 != state1


def test_dealer_ask_for_action() -> None:
    dealer = Dealer()
    p1, p2, p3 = dealer.start_game(3)
    list_players = [p1, p2, p3]
    round = dealer.start_round(list_players)
    state = dealer.get_state(round)
    p1_action = p1.decide_action(state)
    p2_action = p2.decide_action(state)
    p3_action = p3.decide_action(state)
    assert all([p1_action, p2_action, p3_action]) is not None


def test_dealer_update_cards() -> None:
    p1 = Player()
    dealer = Dealer()
    p1 = dealer.update_cards(p1)
    assert len(p1.hand) == 5


def test_dealer_update_cards_two_player() -> None:
    p1 = Player()
    p2 = Player()
    dealer = Dealer()
    with pytest.raises(ValueError):
        dealer.update_cards([p1, p2])


def test_dealer_keeps_track_of_completed_rounds() -> None:
    dealer = Dealer()
    list_players = dealer.start_game(2)
    round = dealer.start_round(list_players)
    assert dealer.round_count is not None


def test_dealer_can_compare_players() -> None:
    dealer = Dealer()
    list_players = dealer.start_game(2)
    round = dealer.start_round(list_players)
    assert dealer.compare(list_players) is not None


def test_dealer_start_game_creates_n_players() -> None:
    dealer = Dealer()
    n_players = 3
    players = dealer.start_game(n_players=n_players)
    assert len(players) == 3


# def test_dealer_can_validate_action() -> None:
#     dealer = Dealer()
#     list_players = dealer.start_game(4)
#     round = dealer.start_round(list_players)
#     first_player = list_players[0]
#     state = dealer.update_state(round)
#     action = first_player.send_action(state)
#     print(action)
#     assert dealer.is_valid_action(action) is True
