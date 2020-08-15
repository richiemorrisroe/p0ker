from pkr import random_hand
from stats import score_hand_distribution
def test_count_list_of_hands() -> None:
    manyhands = [random_hand() for x in range(100)]
    hand_dist = score_hand_distribution(manyhands)
    assert hand_dist is not None
