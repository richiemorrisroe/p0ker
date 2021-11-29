from deck.pkr import Round, Dealer, Player, random_choice, Action


def test_dealer_round_is_round() -> None:
    dealer = Dealer()
    p1, p2 = dealer.start_game(2)
    round = dealer.start_round([p1, p2])
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
    p1, p2 = dealer.start_game(2)
    round = dealer.start_round([p1, p2])
    state = dealer.get_state(round)
    assert state is not None


def test_round_state_is_dict() -> None:
    dealer = Dealer()
    p1, p2, p3 = dealer.start_game(3)
    round = dealer.start_round([p1, p2, p3])
    state = dealer.get_state(round)
    assert isinstance(state, dict)


def test_round_state_has_pot_value() -> None:
    dealer = Dealer()
    p1, p2 = dealer.start_game(2)
    round = dealer.start_round([p1, p2])
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
    p1, p2, p3 = dealer.start_game(3)
    round = dealer.start_round([p1, p2, p3])
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
    p1, p2, p3 = dealer.start_game(3)
    round = dealer.start_round([p1, p2, p3])
    assert round is not None


def test_round_returns_players_with_hands() -> None:
    dealer = Dealer()
    p1, p2, p3 = dealer.start_game(3)
    round = dealer.start_round([p1, p2, p3])
    assert (len(p1.hand) == 5 and len(p2.hand) == 5
            and len(p3.hand) == 5)


def test_round_has_minimum_bet() -> None:
    dealer = Dealer()
    p1, p2, p3 = dealer.start_game(3)
    round = dealer.start_round([p1, p2, p3])
    assert dealer.get_state(round)['min_bet'] is not None


def test_round_has_minimum_bet_greater_than_zero() -> None:
    dealer = Dealer()
    p1, p2, p3 = dealer.start_game(3)
    round = dealer.start_round([p1, p2, p3])
    assert dealer.get_state(round)['min_bet'] > 0


def test_round_minimum_bet_equal_to_sum_of_bets() -> None:
    dealer = Dealer()
    p1, p2, p3 = dealer.start_game(3)
    round = dealer.start_round([p1, p2, p3])


def test_round_can_update_minimum_bet():
    dealer = Dealer()
    list_players = dealer.start_game(3)
    round = dealer.start_round(list_players)
    state = dealer.update_state(round)
    p1, p2, p3 = list_players
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
    assert action.action() == "BET" and action.amount == 100

def test_round_stores_player_names_in_order():
    dealer = Dealer()
    list_players = dealer.start_game(3)
    round = dealer.start_round(list_players)
    state = dealer.update_state(round)
    p_names = [p.name for p in list_players]
    assert round.player_names == p_names


def test_round_returns_winning_name_with_end_state_action():
    dealer = Dealer()
    list_players = dealer.start_game(3)
    round = dealer.start_round(list_players)
    rc = dealer.round_count
    p1, p2, p3 = list_players
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
                                            

