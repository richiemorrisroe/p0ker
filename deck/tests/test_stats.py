from deck.pkr import random_hand
from deck.stats import score_hand_distribution, generate_hands

def test_generate_hands_returns_n_hands() -> None:
    manyhands = generate_hands(n=100)
    assert len(manyhands) == 100

def test_score_hand_dist_returns_all_hands() -> None:
    n = 100
    manyhands = generate_hands(n)
    score_dist = score_hand_distribution(manyhands)
    total_sum = sum(score_dist.values())
    assert total_sum == n
    
    
def test_count_list_of_hands() -> None:
    manyhands = [random_hand() for x in range(100)]
    hand_dist = score_hand_distribution(manyhands)
    assert hand_dist is not None

def test_score_hand_dist_returns_scores() -> None:
    manyhands = [random_hand() for x in range(100)]
    hand_dist = score_hand_distribution(manyhands)
    assert hand_dist['NOTHING'] > 0
