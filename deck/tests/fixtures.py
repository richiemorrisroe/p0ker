import pytest

from deck.pkr import Dealer, Player, Round

@pytest.fixture
def dealer_3_players():
    dealer = Dealer()
    dict_players = dealer.start_game(3)
    round = dealer.start_round(dict_players)
    return (dealer, dict_players, round)
