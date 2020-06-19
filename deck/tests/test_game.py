from pkr import Dealer, Deck, Player, deal_cards
def test_dealer_is_dealer() -> None:
    dealer = Dealer()
    assert isinstance(dealer, Dealer)

def test_dealer_has_deck() -> None:
    dealer = Dealer()
    assert isinstance(dealer.deck, Deck)

def test_dealer_pot_is_zero() -> None:
    dealer = Dealer()
    assert dealer.pot == 0

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




def test_dealer_set_blind() -> None:
    dealer = Dealer()
    small_blind = dealer.get_blind('small')
    big_blind = dealer.get_blind('big')
    assert big_blind > small_blind

def test_dealer_get_blind() -> None:
    dealer = Dealer()
    p1 = Player()
    p2 = Player()
    p3 = Player()
    list_players = [p1, p2, p3]
    dealer.get_blinds(list_players)
    assert dealer.get_pot_value() == 300

def test_dealer_ask_for_action() -> None:
    dealer = Dealer()
    p1 = Player()
    p2 = Player()
    p3 = Player()
    list_players = [p1, p2, p3]
    p1, p2, p3 = dealer.get_blinds(list_players)
    p1, p2, p3 = dealer.deals([p1, p2, p3])
    
    p1_action = p1.decide_action(dealer)
    p2_action = p2.decide_action(dealer)
    p3_action = p3.decide_action(dealer)
    assert all([p1_action, p2_action, p3_action]) is not  None


def test_dealer_has_state() -> None:
    dealer = Dealer()
    state = dealer.get_state()
    assert state is not None

def test_dealer_state_is_dict() -> None:
    dealer = Dealer()
    state = dealer.get_state()
    assert isinstance(state, dict)

def test_dealer_state_has_pot_value() -> None:
    dealer = Dealer()
    state = dealer.get_state()
    assert state['pot_value'] is not None
    
def test_dealer_update_cards() -> None:
    p1 = Player()
    dealer = Dealer()
    p1 = dealer.update_cards(p1)
    assert len(p1.hand) == 5
    
def test_dealer_pot_value_state() -> None:
    dealer = Dealer()
    p1 = Player()
    p2 = Player()
    p3 = Player()
    list_players = [p1, p2, p3]
    dealer.get_blinds(list_players)
    state = dealer.get_state()
    assert state['pot_value'] == 300
    
def test_dealer_state_has_player_pos() -> None:
    dealer = Dealer()
    p1 = Player()
    p2 = Player()
    p3 = Player()
    state = dealer.get_state()
    assert state['position'] is not None

def test_dealer_set_position() -> None:
    pos = random_choice(0, 4)
    dealer = Dealer()
    dealer.set_position(pos)
    assert dealer.get_state()['position'] == pos


def test_dealer_can_start_round() -> None:
    pass
