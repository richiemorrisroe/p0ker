def test_player_decide_action() -> None:
    hand = random_hand()
    player = Player(hand=hand)
    p2 = Player()
    dealer = Dealer()
    round = dealer.start_round([player, p2])
    state = dealer.get_state(round)
    assert player.decide_action(state) is not None

def test_player_send_action() -> None:
    dealer = Dealer()
    p1, p2 = dealer.start_game(2)
    p1, p2 = dealer.deals([p1, p2])
    action = p1.decide_action()
    assert action["action"] in ["CALL", "BET", "FOLD", "RAISE"]

def test_player_action_response_is_dict() -> None:
    dealer = Dealer()
    list_players = dealer.start_game(3)
    round = dealer.start_round(list_players)
    state = dealer.update_state(round)
    p1, p2, p3 = list_players
    action = p1.send_action(state)
    assert isinstance(action, dict)

def test_dealer_updates_state_after_action() -> None:
    dealer = Dealer()
    list_players = dealer.start_game(n_players = 3)
    round = dealer.start_round(list_players)
    state = round.update_state()
    dealer.take_action(list_players[0])
    state2 = dealer.get_state(round)
    assert len(state2['actions']) > len(state['actions'])


def test_dealer_associates_player_name_with_action() -> None:
    dealer = Dealer()
    list_players = dealer.start_game(3)
    round = dealer.start_round(list_players)
    state_0 = round.update_state()
    dealer.take_action(list_players[0])
    state_1 = round.update_state()
    p1_name = list_players[0].name
    assert state_1['actions'][0]['name'] == p1_name
    # assert state_1['action'][p1_name] is not None

    
def test_dealer_can_take_one_action_from_all_players() -> None:
    dealer = Dealer()
    list_players = dealer.start_game(3)
    round = dealer.start_round(list_players)
    for player in list_players:
        dealer.take_action(player)
    state = dealer.update_state(round)
    # assert state is None
    assert len(state['actions']) == len(list_players)
