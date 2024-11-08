from deck.pkr import Action, Actions, Dealer, Player, random_choice, Round
from .fixtures import dealer_3_players


def test_dealer_round_is_round() -> None:
    dealer = Dealer()
    dp = dealer.start_game(2)
    round = dealer.start_round(dp)
    assert isinstance(round, Round)


def test_round_exists() -> None:
    p1 = Player(name="richie")
    p2 = Player(name="libbie")
    r = Round(100, [p1, p2])
    assert r is not None


def test_round_get_blinds() -> None:
    dealer = Dealer()
    list_players = dealer.start_game(3)
    round = dealer.start_round(list_players)
    assert round.get_pot_value() == 300


def test_dealer_has_state() -> None:
    dealer = Dealer()
    dp = dealer.start_game(2)
    round = dealer.start_round(dp)
    state = dealer.get_state(round)
    assert state is not None


def test_round_state_is_dict() -> None:
    dealer = Dealer()
    dp = dealer.start_game(3)
    round = dealer.start_round(dp)
    state = dealer.get_state(round)
    assert isinstance(state, dict)


def test_round_state_has_pot_value() -> None:
    dealer = Dealer()
    dp = dealer.start_game(2)
    round = dealer.start_round(dp)
    state = dealer.get_state(round)
    assert state['pot_value'] is not None


def test_round_pot_value_state() -> None:
    dealer = Dealer()
    list_players = dealer.start_game(3)
    round = dealer.start_round(list_players)
    state = dealer.get_state(round)
    assert state['pot_value'] == 300


def test_round_state_has_player_pos() -> None:
    dealer = Dealer()
    dp = dealer.start_game(3)
    round = dealer.start_round(dp)
    state = dealer.get_state(round)
    assert state['position'] is not None


def test_round_set_position() -> None:
    dealer = Dealer()

    list_players = dealer.start_game(3)
    pos = random_choice(0, len(list_players))
    round = dealer.start_round(list_players)
    round.set_position(pos)
    assert dealer.get_state(round)['position'] == pos


def test_round_takes_a_list_of_players() -> None:
    dealer = Dealer()
    dp = dealer.start_game(3)
    round = dealer.start_round(dp)
    assert round is not None


def test_round_returns_players_with_hands() -> None:
    dealer = Dealer()
    dp = dealer.start_game(3)
    _ = dealer.start_round(dp)
    p1, p2, p3 = dp
    assert (len(p1.hand) == 5 and len(p2.hand) == 5
            and len(p3.hand) == 5)


def test_round_has_minimum_bet() -> None:
    dealer = Dealer()
    dp = dealer.start_game(3)
    round = dealer.start_round(dp)
    assert dealer.get_state(round)['min_bet'] is not None


def test_round_has_minimum_bet_greater_than_zero() -> None:
    dealer = Dealer()
    dp = dealer.start_game(3)
    round = dealer.start_round(dp)
    assert dealer.get_state(round)['min_bet'] > 0


def test_round_minimum_bet_equal_to_sum_of_bets() -> None:
    dealer = Dealer()
    dp = dealer.start_game(3)
    round = dealer.start_round(dp)


def test_round_can_update_minimum_bet():
    dealer = Dealer()
    players = dealer.start_game(3)
    round = dealer.start_round(players)
    state = dealer.update_state(round)
    p1, p2, p3 = players
    action = p1.send_action(state=state, action=Action("BET", 100))
    dealer.accept_action(action)
    state = dealer.update_state(round)
    action2 = p2.send_action(state=state, action=Action("BET", 100))
    state = dealer.update_state(round)
    assert state['min_bet'] == 100


def test_player_can_pass_in_action_argument_to_send_action():
    dealer = Dealer()
    list_players = dealer.start_game(3)
    round = dealer.start_round(list_players)
    state = dealer.update_state(round)
    p1, _, _ = list_players
    # print(state)
    action = p1.send_action(state=state, action=Action("BET", 100))
    assert action.get_action() == "BET" and action.amount == 100


def test_round_stores_player_names_in_order():
    dealer = Dealer()
    players = dealer.start_game(3)
    round = dealer.start_round(players)
    p_names = [p.name for p in players]
    assert round.player_names == p_names


def test_round_returns_winning_name_with_end_state_action():
    dealer = Dealer()
    dict_players = dealer.start_game(3)
    round = dealer.start_round(dict_players)
    p1, p2, p3 = dict_players
    dealer.take_action(p1, Action("FOLD", 0))
    dealer.take_action(p2, Action("FOLD", 0))
    state = dealer.update_state(round)
    winning_name = p3.name
    print(f"state in test_round is {state}")
    va = state['valid_actions'].pop()
    print(f"va is {va!r}")
    assert va.kind == 'END'
    assert va.amount == 0
    assert va.name == winning_name


def test_get_maximum_bet_is_the_max_of_bet_or_raise(dealer_3_players):
    dealer, players, round = dealer_3_players
    p1, p2, p3 = players
    dealer.take_action(p1, Action("BET", 100))
    dealer.take_action(p2, Action("RAISE", 200))
    dealer.take_action(p3, Action("BET", 300))
    state = dealer.update_state(round)
    assert state['max_bet'] == 300


def test_round_actions_is_actions(dealer_3_players):
    dealer, players, round = dealer_3_players
    p1, p2, p3 = players
    dealer.take_action(p1, Action("BET", 100))
    dealer.take_action(p2, Action("RAISE", 200))
    dealer.take_action(p3, Action("BET", 300))
    assert isinstance(round.actions, Actions)
