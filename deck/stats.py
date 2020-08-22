from typing import List
from collections import defaultdict


from .pkr import Hand, random_hand

def generate_hands(n:int) -> List[Hand]:
    manyhands = [random_hand() for _ in range(n)]
    return(manyhands)

def score_hand_distribution(hands:List[Hand]):
    dist = {}
    scores = [hand.score() for hand in hands]
    assert len(scores) == len(hands)
    for score, name in scores:
        try:
            dist[name] += 1
        except KeyError:
            dist[name] = 1
            
    return(dist)
