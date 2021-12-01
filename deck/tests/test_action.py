import pytest

from deck.pkr import random_hand, Player, Dealer, Action


def test_player_send_action() -> None:
    dealer = Dealer()
    players = dealer.start_game(2)
    round = dealer.start_round(players)
    p1, p2 = players.values()
    state = dealer.update_state(round)
    action = p1.decide_action(state)
    assert action.action() in ["CALL", "BET", "FOLD", "RAISE", "CHECK"]


def test_action_can_get_name():
    action = Action("FOLD", 0, "Richie")
    assert action.get_name() == "Richie"


def test_action_can_set_name():
    action = Action("FOLD", 0, None)
    action.set_name("Richie")
    assert action.get_name() == "Richie"


def test_action_cannot_set_name_if_not_none():
    action = Action("FOLD", 0, "richie")
    with pytest.raises(ValueError):
        action.set_name("Eveline")


def test_player_action_response_is_action() -> None:
    dealer = Dealer()
    dict_players = dealer.start_game(3)
    round = dealer.start_round(dict_players)
    state = dealer.update_state(round)
    p1, p2, p3 = dict_players.values()
    action = p1.send_action(state)
    assert isinstance(action, Action)


def test_dealer_updates_state_after_action() -> None:
    dealer = Dealer()
    dict_players = dealer.start_game(n_players=3)
    round = dealer.start_round(dict_players)
    state = round.update_state()
    player_names = list(dict_players.keys())
    dealer.take_action(dict_players[player_names[0]])
    state2 = dealer.get_state(round)
    assert len(state2["actions"]) > len(state["actions"])


def test_dealer_associates_player_name_with_action() -> None:
    dealer = Dealer()
    dict_players = dealer.start_game(3)
    round = dealer.start_round(dict_players)
    state_0 = round.update_state()
    player_names = list(dict_players.keys())
    dealer.take_action(dict_players[player_names[0]])
    state_1 = round.update_state()
    p1_name = player_names[0]
    assert state_1["actions"][0].name == p1_name
    # assert state_1['action'][p1_name] is not None


# def test_dealer_can_take_one_action_from_all_players() -> None:
#     dealer = Dealer()
#     list_players = dealer.start_game(3)
#     round = dealer.start_round(list_players)
#     for player in list_players:
#         dealer.take_action(player)
#         state = dealer.update_state(round)
#     # assert state is None
#     assert len(state['actions']) == len(list_players)


def test_action_is_one_of_four_actions():
    bet = Action(kind="BET", amount=100)
    assert isinstance(bet, Action)


def test_action_fold_cannot_have_an_amount_greater_than_zero():
    wrong_fold = Action(kind="FOLD", amount=100)
    assert not wrong_fold.is_valid()


def test_bet_must_have_an_amount_greater_than_zero():
    wrong_bet = Action(kind="BET", amount=0)
    assert not wrong_bet.is_valid()


def test_call_cannot_have_amount_of_zero():
    dealer = Dealer()
    wrong_call = Action(kind="CALL", amount=0)
    wrong_call.set_name("Eveline")
    assert not dealer.is_valid_action(wrong_call)


def test_dealer_take_action_can_be_passed_an_action():
    dealer = Dealer()
    dict_players = dealer.start_game(2)
    round = dealer.start_round(dict_players)
    p1, p2 = dict_players.values()
    action = Action("FOLD", 0)
    print(action)
    dealer.take_action(player=p1, action=action)


def test_all_but_one_player_folding_ends_round():
    dealer = Dealer()
    list_players = dealer.start_game(3)
    round = dealer.start_round(list_players)
    rc = dealer.round_count
    print(f"round_count is {rc}")
    p1, p2, p3 = list_players.values()
    pnames = list(list_players.keys())
    dp = {name:player for name, player in zip(pnames, [p1, p2, p3])}
    dealer.take_action(p1, Action("FOLD", 0))
    dealer.take_action(p2, Action("FOLD", 0))
    state = dealer.update_state(round)
    print("round_count is {rc}".format(rc=dealer.round_count))
    players = dealer.update_round(dp)
    assert dealer.round_count == 1

def test_all_but_one_player_folding_ends_round_and_updates_player_stashes():
    dealer = Dealer()
    list_players = dealer.start_game(3)
    round = dealer.start_round(list_players)
    rc = dealer.round_count
    print(f"round_count is {rc}")
    p1, p2, p3 = list_players.values()
    dealer.take_action(p1, Action("FOLD", 0))
    dealer.take_action(p2, Action("FOLD", 0))
    state = dealer.update_state(round)
    pnames = list(list_players.keys())
    dp = {name:player for name, player in zip(pnames, [p1, p2, p3])}
    dp2 = dealer.update_round(round=round, players=dp)
    p1, p2, p3 = dp2.values()
    print("round_count is {rc}".format(rc=dealer.round_count))
    assert p3.stash > max([p1.stash,p2.stash])

def test_pot_is_reduced_to_zero_after_round_ends():
    dealer = Dealer()
    list_players = dealer.start_game(3)
    round = dealer.start_round(list_players)
    rc = dealer.round_count
    print(f"round_count is {rc}")
    p1, p2, p3 = list_players.values()
    dealer.take_action(p1, Action("FOLD", 0))
    dealer.take_action(p2, Action("FOLD", 0))
    pnames = list(list_players.keys())
    dp = {name:player for name, player in zip(pnames, [p1, p2, p3])}
    state = dealer.update_state(round)
    dp2 = dealer.update_round(players=dp)
    assert dealer.round.get_pot_value() == 0

def test_valid_actions_are_some_bet_state_after_bet():
    dealer = Dealer()
    list_players = dealer.start_game(3)
    round = dealer.start_round(list_players)
    p1, p2, p3 = list_players.values()
    dealer.take_action(p1, Action("BET", 150))
    state = dealer.update_state(round)
    va = state['valid_actions']
    print(f"valid_actions are {va}")
    kinds = [x.kind for x in va]
    amounts = [x.amount for x in va]
    assert ['BET',  'FOLD', 'RAISE'] == sorted(kinds)
    assert [0, 200, 400] == sorted(amounts)


def test_dealer_can_provide_list_of_valid_actions():
    dealer = Dealer()
    list_players = dealer.start_game(3)
    round = dealer.start_round(list_players)
    state = dealer.update_state(round)
    assert state["valid_actions"] is not None


def test_dealer_only_check_bet_and_fold_possible_for_first_player():
    dealer = Dealer()
    list_players = dealer.start_game(3)
    round = dealer.start_round(list_players)
    state = dealer.update_state(round)
    valid_actions = [a.action() for a in state["valid_actions"]]
    assert ["CHECK", "BET", "FOLD"] == valid_actions


def test_player_can_only_take_a_valid_action():
    dealer = Dealer()
    list_players = dealer.start_game(3)
    round = dealer.start_round(list_players)
    state = dealer.update_state(round)
    p1, _, _ = list_players.values()
    p1_action = p1.send_action(state)
    val_act = [a.action() for a in state["valid_actions"]]
    assert p1_action.action() in val_act


# def test_dealer_can_take_one_action_from_all_players() -> None:
#     dealer = Dealer()
#     list_players = dealer.start_game(3)
#     round = dealer.start_round(list_players)
#     for player in list_players:
#         dealer.take_action(player)
#         state = dealer.update_state(round)
#     # assert state is None
#     assert len(state['actions']) == len(list_players)

def test_dealer_can_validate_action() -> None:
    dealer = Dealer()
    list_players = dealer.start_game(4)
    round = dealer.start_round(list_players)
    first_player = list(list_players.values())[0]
    state = dealer.update_state(round)
    action = first_player.send_action(state)
    print(action)
    assert dealer.is_valid_action(action) is True

    
def test_dealer_ends_round_if_all_but_one_player_has_folded():
    pass
