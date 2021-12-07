import pytest

from deck.pkr import Action, Actions, Dealer, Player, random_hand
from .fixtures import dealer_3_players

def test_player_send_action(dealer_3_players) -> None:
    dealer, players, round = dealer_3_players
    p1, p2, _ = players.values()
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


def test_player_action_response_is_action(dealer_3_players) -> None:
    dealer, players, round = dealer_3_players
    state = dealer.update_state(round)
    p1, p2, p3 = players.values()
    action = p1.send_action(state)
    assert isinstance(action, Action)


def test_dealer_updates_state_after_action(dealer_3_players) -> None:
    dealer, players, round = dealer_3_players
    state = round.update_state()
    player_names = list(players.keys())
    dealer.take_action(players[player_names[0]])
    state2 = dealer.get_state(round)
    assert len(state2["actions"]) > len(state["actions"])


def test_dealer_associates_player_name_with_action(dealer_3_players) -> None:
    dealer, players, round = dealer_3_players
    state_0 = round.update_state()
    player_names = list(players.keys())
    dealer.take_action(players[player_names[0]])
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


def test_dealer_take_action_can_be_passed_an_action(dealer_3_players):
    dealer, players, round = dealer_3_players
    p1, p2, _ = players.values()
    action = Action("FOLD", 0)
    print(action)
    dealer.take_action(player=p1, action=action)


def test_all_but_one_player_folding_ends_round(dealer_3_players):
    dealer, players, round = dealer_3_players
    rc = dealer.round_count
    print(f"round_count is {rc}")
    p1, p2, p3 = players.values()
    pnames = list(players.keys())
    dp = {name:player for name, player in zip(pnames, [p1, p2, p3])}
    dealer.take_action(p1, Action("FOLD", 0))
    dealer.take_action(p2, Action("FOLD", 0))
    state = dealer.update_state(round)
    print("round_count is {rc}".format(rc=dealer.round_count))
    players = dealer.update_round(dp)
    assert dealer.round_count == 1

def test_check_action_keeps_no_bet_state(dealer_3_players):
    dealer, players, round = dealer_3_players
    p1, p2, p3 = players.values()
    pnames = list(players.keys())
    dp = {name:player for name, player in zip(pnames, [p1, p2, p3])}
    dealer.take_action(p1, Action("CHECK", 0))
    dealer.take_action(p2, Action("CHECK", 0))
    state = dealer.update_state(round)
    valid_actions = state['valid_actions']
    players = dealer.update_round(dp)
    actions = [action.action() for action in valid_actions]
    assert actions == ['CHECK', 'BET', 'FOLD']



    
def test_all_but_one_player_folding_ends_round_and_updates_player_stashes(dealer_3_players):
    dealer, players, round = dealer_3_players
    rc = dealer.round_count
    print(f"round_count is {rc}")
    p1, p2, p3 = players.values()
    dealer.take_action(p1, Action("FOLD", 0))
    dealer.take_action(p2, Action("FOLD", 0))
    state = dealer.update_state(round)
    pnames = list(players.keys())
    dp = {name:player for name, player in zip(pnames, [p1, p2, p3])}
    dp2 = dealer.update_round(round=round, players=dp)
    p1, p2, p3 = dp2.values()
    print("round_count is {rc}".format(rc=dealer.round_count))
    assert p3.stash > max([p1.stash,p2.stash])

def test_pot_is_reduced_to_zero_after_round_ends(dealer_3_players):
    dealer, players, round = dealer_3_players
    rc = dealer.round_count
    p1, p2, p3 = players.values()
    dealer.take_action(p1, Action("FOLD", 0))
    dealer.take_action(p2, Action("FOLD", 0))
    pnames = list(players.keys())
    dp = {name:player for name, player in zip(pnames, [p1, p2, p3])}
    state = dealer.update_state(round)
    dp2 = dealer.update_round(players=dp)
    assert dealer.round.get_pot_value() == 0

def test_valid_actions_are_some_bet_state_after_bet(dealer_3_players):
    dealer, players, round = dealer_3_players
    p1, p2, p3 = players.values()
    dealer.take_action(p1, Action("BET", 150))
    state = dealer.update_state(round)
    va = state['valid_actions']
    print(f"valid_actions are {va}")
    kinds = [x.kind for x in va]
    amounts = [x.amount for x in va]
    assert ['BET',  'FOLD', 'RAISE'] == sorted(kinds)
    assert [0, 200, 400] == sorted(amounts)


def test_dealer_can_provide_list_of_valid_actions(dealer_3_players):
    dealer, players, round = dealer_3_players
    state = dealer.update_state(round)
    assert state["valid_actions"] is not None


def test_dealer_only_check_bet_and_fold_possible_for_first_player(dealer_3_players):
    dealer, players, round = dealer_3_players
    state = dealer.update_state(round)
    valid_actions = [a.action() for a in state["valid_actions"]]
    assert ["CHECK", "BET", "FOLD"] == valid_actions


def test_player_can_only_take_a_valid_action(dealer_3_players):
    dealer, players, round = dealer_3_players
    state = dealer.update_state(round)
    p1, _, _ = players.values()
    p1_action = p1.send_action(state)
    val_act = [a.action() for a in state["valid_actions"]]
    assert p1_action.action() in val_act


def test_dealer_can_take_one_action_from_all_players(dealer_3_players) -> None:
    dealer, players, round = dealer_3_players
    for name, player in players.items():
        dealer.take_action(player)
        state = dealer.update_state(round)
        dealer.update_round(players=players)
    # assert state is None
    assert len(state['actions']) == len(players)

def test_dealer_can_validate_action(dealer_3_players) -> None:
    dealer, players, round = dealer_3_players
    first_player = list(players.values())[0]
    state = dealer.update_state(round)
    action = first_player.send_action(state)
    print(action)
    assert dealer.is_valid_action(action) is True


def test_bet_causes_sum_bets_to_increase(dealer_3_players):
    dealer, players, round = dealer_3_players
    p1, p2, p3 = players.values()
    dealer.take_action(p1, Action("BET", 100))
    dealer.take_action(p2, Action("BET", 200))
    pnames = list(players.keys())
    dp = {name:player for name, player in zip(pnames, [p1, p2, p3])}
    state = dealer.update_state(round)
    assert state['sum_bets'] == 300

def test_raise_causes_sum_bets_to_increase(dealer_3_players):
    dealer, players, round = dealer_3_players
    p1, p2, p3 = players.values()
    dealer.take_action(p1, Action("BET", 100))
    dealer.take_action(p2, Action("RAISE", 200))
    pnames = list(players.keys())
    dp = {name:player for name, player in zip(pnames, [p1, p2, p3])}
    state = dealer.update_state(round)
    assert state['sum_bets'] == 300

# def test_update_round_ensures_that_all_players_bet_equal_amounts(dealer_3_players):
#     dealer, players, round = dealer_3_players
#     p1, p2, p3 = players.values()
#     dealer.take_action(p1, Action("BET", 100))
#     dealer.take_action(p2, Action("RAISE", 200))
#     dealer.take_action(p3, Action("BET", 300))
#     pnames = list(players.keys())
#     dp = {name:player for name, player in zip(pnames, [p1, p2, p3])}
#     state = dealer.update_state(round)
#     dp = dealer.update_round(players=players)
#     pv = round.get_pot_value()
#     assert pv == 1200    

def test_raise_reduces_player_stashes(dealer_3_players):
    dealer, players, round = dealer_3_players
    p1, p2, p3 = players.values()
    dealer.take_action(p1, Action("BET", 100))
    dealer.take_action(p2, Action("RAISE", 200))
    pnames = list(players.keys())
    dp = {name:player for name, player in zip(pnames, [p1, p2, p3])}
    state = dealer.update_state(round)
    assert p1.stash == 4800 and p2.stash == 4700
    

def test_actions_object_exists():
    actions = Actions(actions=[Action("BET", 100, name="richie")])
    assert actions is not None


def test_actions_has_add_action():
    actions = Actions(actions=[Action("BET", 100, name="richie")])
    actions.update(Action("RAISE", 200, name = "libbie"))
    # assert len(actions) == 2
    assert len(actions) == 2

def test_actions_has_action_count():
    actions = Actions(actions=[Action("BET", 100, name="richie")])
    assert actions.kind_count == {"CHECK":0, "BET":1,
                                  "FOLD":0, "RAISE":0, "END":0}

def test_actions_can_take_empty_actions():
    actions = Actions(actions=[])
    assert actions.action_list == []

def test_actions_has_a_get_bets_function():
    actions = Actions([Action("BET", 100, name="richie")])
    assert actions.get_bets() is not None


def test_actions_has_a_maximum_bet_function():
    actions = Actions([Action("BET", 100, name="richie")])
    assert actions.max_bet() == 100

def test_actions_has_a_sum_bet_function():
    actions = Actions([Action("BET", 100, name="richie"),
                       Action("RAISE", 200, name="libbie")])
    assert actions.sum_bets() == 300
    assert actions.max_bet() == 200
