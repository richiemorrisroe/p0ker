from deck.pkr import Round, Dealer, Player, random_choice


def test_dealer_round_is_round() -> None:
    dealer = Dealer()
    p1 = Player()
    p2 = Player()
    round =  dealer.start_round([p1, p2])
    assert isinstance(round, Round)

def test_round_exists() -> None:
    p1 = Player()
    p2 = Player()
    r = Round(100, [p1, p2])
    assert r is not None



def test_dealer_set_blind() -> None:
    dealer = Dealer()
    p1 = Player()
    p2 = Player()
    round = dealer.start_round([p1, p2])
    small_blind = round.get_blind('small')
    big_blind = round.get_blind('big')
    assert big_blind > small_blind

def test_round_get_blind() -> None:
    dealer = Dealer()
    p1 = Player()
    p2 = Player()
    p3 = Player()
    list_players = [p1, p2, p3]
    round = dealer.start_round(list_players)
    assert round.get_pot_value() == 300

def test_dealer_has_state() -> None:
    p1 = Player()
    p2 = Player()
    
    dealer = Dealer()
    round = dealer.start_round([p1, p2])
    state = dealer.get_state(round)
    assert state is not None


def test_round_state_is_dict() -> None:
    p1 = Player()
    p2 = Player()
    p3 = Player()
    dealer = Dealer()
    round = dealer.start_round([p1, p2, p3])
    state = dealer.get_state(round)
    assert isinstance(state, dict)


def test_round_state_has_pot_value() -> None:
    dealer = Dealer()
    p1 = Player()
    p2 = Player()
    round = dealer.start_round([p1, p2])
    state = dealer.get_state(round)
    assert state['pot_value'] is not None

def test_round_pot_value_state() -> None:
    dealer = Dealer()
    p1 = Player()
    p2 = Player()
    p3 = Player()
    list_players = [p1, p2, p3]
    round = dealer.start_round(list_players)
    state = dealer.get_state(round)
    assert state['pot_value'] == 300


def test_round_state_has_player_pos() -> None:
    dealer = Dealer()
    p1 = Player()
    p2 = Player()
    p3 = Player()
    round = dealer.start_round([p1, p2, p3])
    state = dealer.get_state(round)
    assert state['position'] is not None


def test_round_set_position() -> None:
    
    dealer = Dealer()
    p1 = Player()
    p2 = Player()
    list_players = [p1, p2]
    pos = random_choice(0, len(list_players))
    round = dealer.start_round(list_players)
    round.set_position(pos)
    assert dealer.get_state(round)['position'] == pos


def test_round_takes_a_list_of_players() -> None:
    dealer = Dealer()
    p1 = Player()
    p2 = Player()
    p3 = Player()
    round = dealer.start_round([p1, p2, p3])
    assert round is not None

def test_round_returns_players_with_hands() -> None:
    dealer = Dealer()
    p1 = Player()
    p2 = Player()
    p3 = Player()
    round = dealer.start_round([p1, p2, p3])
    assert (len(p1.hand) == 5 and len(p2.hand) == 5
            and len(p3.hand) == 5)

def test_round_has_minimum_bet() -> None:
    dealer = Dealer()
    p1 = Player()
    p2 = Player()
    p3 = Player()
    round  = dealer.start_round([p1, p2, p3])
    assert dealer.get_state(round)['min_bet'] is not None

def test_round_has_minimum_bet_greater_than_zero() -> None:
    dealer = Dealer()
    p1 = Player()
    p2 = Player()
    p3 = Player()
    round  = dealer.start_round([p1, p2, p3])
    assert dealer.get_state(round)['min_bet'] > 0 


def test_round_minimum_bet_equal_to_sum_of_bets() -> None:
    dealer = Dealer()
    p1 = Player()
    p2 = Player()
    p3 = Player()
    round  = dealer.start_round([p1, p2, p3])
