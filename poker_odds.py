import random
from collections import Counter
from enum import Enum
from itertools import combinations
values = {'2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, 
              '9':9, '10':10, 'J':11, 'Q':12, 'K':13, 'A':14}

class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __str__(self):
        return f"{self.rank} of {self.suit}"
    
    def __repr__(self):
        return f"{self.rank}{self.suit}"
    
    def __eq__(self, other):
        return self.rank == other.rank and self.suit == other.suit
    
    def __hash__(self):
        return hash((self.rank, self.suit))

    
class Hand:
    def __init__(self, cards):
        self.cards = cards

    def __str__(self):
        return ', '.join(str(card) for card in self.cards)
    
def create_deck():
    suits = 'HDCS'  # Hearts, Diamonds, Clubs, Spades
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    return [Card(rank, suit) for rank in ranks for suit in suits]


class HandRank(Enum):
    HIGH_CARD = 1
    ONE_PAIR = 2
    TWO_PAIR = 3
    THREE_OF_A_KIND = 4
    STRAIGHT = 5
    FLUSH = 6
    FULL_HOUSE = 7
    FOUR_OF_A_KIND = 8
    STRAIGHT_FLUSH = 9
    ROYAL_FLUSH = 10

def duplicate_card(cards):
    ''' Check if there are duplicate cards in the hand '''
    seen = set()
    for card in cards:
        if card in seen:
            return True
        seen.add(card)
    return False

def evaluate_hand(cards):
    ''' Evaluate the poker hand (5 cards only) '''
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    if len(cards) != 5:
        raise ValueError("Exactly 5 cards are required")
    if not all(card.rank in ranks and card.suit in ['H', 'D', 'C', 'S'] for card in cards):
        raise ValueError("Invalid card rank or suit")
    # Check for duplicate cards
    if duplicate_card(cards):
        raise ValueError("Duplicate cards found in the hand")
    ranks = [values[card.rank] for card in cards]
    suits = [card.suit for card in cards]
    rank_counts = Counter(ranks)
    
    is_flush = len(set(suits)) == 1
    is_straight = len(set(ranks)) == 5 and max(ranks) - min(ranks) == 4
    sorted_ranks = sorted(ranks, reverse=True)
    
    if set(ranks) == {2, 3, 4, 5, 14}:
        is_straight = True
        sorted_ranks = [5, 4, 3, 2, 14]

    counts = sorted(rank_counts.items(), key=lambda x: (-x[1], -x[0]))
    
    if is_flush and is_straight:
        if max(ranks) == 14 and min(ranks) == 10:
            return (HandRank.ROYAL_FLUSH.value, [])
        return (HandRank.STRAIGHT_FLUSH.value, [max(sorted_ranks)])
    elif counts[0][1] == 4:
        return (HandRank.FOUR_OF_A_KIND.value, [counts[0][0], counts[1][0]])
    elif counts[0][1] == 3 and counts[1][1] == 2:
        return (HandRank.FULL_HOUSE.value, [counts[0][0], counts[1][0]])
    elif is_flush:
        return (HandRank.FLUSH.value, sorted_ranks)
    elif is_straight:
        return (HandRank.STRAIGHT.value, [max(sorted_ranks)])
    elif counts[0][1] == 3:
        kickers = sorted([val for val in ranks if val != counts[0][0]], reverse=True)
        return (HandRank.THREE_OF_A_KIND.value, [counts[0][0]] + kickers)
    elif counts[0][1] == 2 and counts[1][1] == 2:
        return (HandRank.TWO_PAIR.value, sorted([counts[0][0], counts[1][0]], reverse=True) + [counts[2][0]])
    elif counts[0][1] == 2:
        kickers = sorted([val for val in ranks if val != counts[0][0]], reverse=True)
        return (HandRank.ONE_PAIR.value, [counts[0][0]] + kickers)
    else:
        return (HandRank.HIGH_CARD.value, sorted_ranks)
    
def calculate_odds(your_hand, opponent_hands, known_community_cards=None, num_simulations=10000):
    '''
    Simulate poker hand outcomes to calculate win/tie/loss probabilities.
    
    Args:
        your_hand: List of 2 Card objects (your hole cards).
        opponent_hands: List of lists, each containing 2 Card objects (opponent hole cards).
        known_community_cards: List of Card objects (known community cards, e.g., flop). Default None.
        num_simulations: Number of Monte Carlo simulations to run. Default 10,000.
    
    Returns:
        Dict with 'win', 'tie', and 'loss' probabilities (as percentages).
    '''
    # Initialize deck
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    suits = ['H', 'D', 'C', 'S']
    # Input validation
    if len(your_hand) != 2:
        raise ValueError("Your hand must have exactly 2 cards")
    for opp_hand in opponent_hands:
        if len(opp_hand) != 2:
            raise ValueError("Each opponent hand must have exactly 2 cards")
    if not all(card.rank in ranks and card.suit in 'HDCS' for card in your_hand):
        raise ValueError("Invalid card in your hand")
    for opp_hand in opponent_hands:
        if not all(card.rank in ranks and card.suit in ['H', 'D', 'C', 'S'] for card in opp_hand):
            raise ValueError("Invalid card in opponent hand")
    if known_community_cards and len(known_community_cards) > 5:
        raise ValueError("Too many community cards")
    if known_community_cards and not all(card.rank in ranks and card.suit in ['H', 'D', 'C', 'S'] for card in known_community_cards):
        raise ValueError("Invalid card in known community cards")

    
    deck = [Card(rank, suit) for rank in ranks for suit in suits]

    # Remove known cards from deck
    known_cards = your_hand + [card for opp_hand in opponent_hands for card in opp_hand]
    if known_community_cards:
        known_cards += known_community_cards
    known_card_ids = {(card.rank, card.suit) for card in known_cards}
    deck = [card for card in deck if (card.rank, card.suit) not in known_card_ids]
    
    # Initialize counters
    wins = 0
    ties = 0
    total_simulations = num_simulations
    
    # Number of community cards to simulate
    num_community_needed = 5 - (len(known_community_cards) if known_community_cards else 0)
    
    for _ in range(num_simulations):
        # Shuffle deck and draw community cards
        random.shuffle(deck)
        community = known_community_cards[:] if known_community_cards else []
        community += deck[:num_community_needed]
        
        # Evaluate your best hand by iterating through combinations
        your_combinations = list(combinations(your_hand + community, 5))
        your_best_hand = max(your_combinations, key=evaluate_hand, default=None)
        your_rank, your_tiebreakers = evaluate_hand(your_best_hand)
        
        # Evaluate opponent best hands
        opponent_ranks = []
        for opp_hand in opponent_hands:
            opp_combinations = list(combinations(opp_hand + community, 5))
            opp_best_hand = max(opp_combinations, key=evaluate_hand, default=None)
            opp_rank, opp_tiebreakers = evaluate_hand(opp_best_hand)
            opponent_ranks.append((opp_rank, opp_tiebreakers))
        
        # Compare hands
        max_opp_rank = max(opp_rank for opp_rank, _ in opponent_ranks)
        if your_rank > max_opp_rank:
            wins += 1
        elif your_rank < max_opp_rank:
            continue
        else:
            # Tiebreaker comparison
            your_score = (your_rank, your_tiebreakers)
            max_opp_score = max((opp_rank, opp_tiebreakers) for opp_rank, opp_tiebreakers in opponent_ranks)
            if your_score > max_opp_score:
                wins += 1
            elif your_score == max_opp_score:
                ties += 1
    
    # Calculate probabilities
    win_prob = (wins / total_simulations) * 100
    tie_prob = (ties / total_simulations) * 100
    loss_prob = 100 - win_prob - tie_prob
    print(your_hand)
    print(your_rank)
    print(opp_hand)
    print(opponent_ranks)
    print(community)
    return {
        'win': round(win_prob, 2),
        'tie': round(tie_prob, 2),
        'loss': round(loss_prob, 2)
    }



def precise_calculate_odds(your_hand, opponent_hands, known_community_cards=None):
    '''
    Calculate the odds of winning, tying, and losing a poker hand by exhaustively simulating all possible community card combinations.

    Args:
        your_hand: List of 2 Card objects (your hole cards).
        opponent_hands: List of lists, each containing 2 Card objects (opponent hole cards).
        known_community_cards: List of known community cards (can be empty or partial, e.g., flop only).

    Returns:
        Dictionary with win, tie, and loss percentages.
    '''
    from collections import Counter
    from itertools import combinations

    deck = create_deck()
    
    # Remove known cards
    known_cards = your_hand[:]
    for opp_hand in opponent_hands:
        known_cards += opp_hand
    if known_community_cards:
        known_cards += known_community_cards

    deck = [card for card in deck if card not in known_cards]
    num_community_needed = 5 - (len(known_community_cards) if known_community_cards else 0)
    
    community_combinations = list(combinations(deck, num_community_needed))
    print(len(community_combinations))
   
    wins = 0
    ties = 0
    total = len(community_combinations)

    for community_rest in community_combinations:
        community = known_community_cards[:] if known_community_cards else []
        community += list(community_rest)

        # Evaluate your best hand
        your_hands = combinations(your_hand + community, 5)
        your_best_hand = max(your_hands, key=evaluate_hand)
        your_rank, your_tiebreakers = evaluate_hand(your_best_hand)
        your_score = (your_rank, your_tiebreakers)

        # Track opponent best hand scores
        opponent_scores = []
        for opp_hand in opponent_hands:
            opp_hands = combinations(opp_hand + community, 5)
            opp_best_hand = max(opp_hands, key=evaluate_hand)
            opp_rank, opp_tiebreakers = evaluate_hand(opp_best_hand)
            opponent_scores.append((opp_rank, opp_tiebreakers))

        max_opp_score = max(opponent_scores)

        if your_score > max_opp_score:
            wins += 1
        elif your_score == max_opp_score:
            ties += 1
        # else: implicit loss

    losses = total - wins - ties

    return {
        'win': round(wins / total * 100, 2),
        'tie': round(ties / total * 100, 2),
        'loss': round(losses / total * 100, 2)
    }


# '''Test the calculate_odds function'''
your_hand = [Card('8', 'H'), Card('9', 'S')]
opponent_hands = [[Card('A', 'D'), Card('K', 'C')]]
odds = precise_calculate_odds(your_hand, opponent_hands)
print(odds)
    