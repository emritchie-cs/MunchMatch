import numpy as np

def adjust_rating(base_rating, sentiment_score, weight=1.2):
    """
    Adjusts the restaurant rating based on the sentiment analysis of taste preferences.
    
    Parameters:
        base_rating (float): Original restaurant rating (0-5 scale)
        sentiment_score (float): Sentiment match factor (-1 to 1)
            - 1.0: Strong match (inflates rating)
            - 0.0: Neutral (keeps rating the same)
            - -1.0: Lacks key flavor (deflates rating)
        weight (float): Impact factor for sentiment influence (default: 1.2)

    Returns:
        float: Adjusted rating (capped between 0 and 5)
    """
    adjusted_rating = base_rating + (sentiment_score * weight)
    return np.clip(adjusted_rating, 0, 5)  # Ensure rating stays in range

# Example Usage:
if __name__ == "__main__":
    test_cases = [
        {"base_rating": 4.0, "sentiment_score": 1.0, "weight": 1.2},  # Strong match
        {"base_rating": 4.2, "sentiment_score": 0.0, "weight": 1.2},  # Neutral (no change)
        {"base_rating": 4.5, "sentiment_score": -1.0, "weight": 1.5},  # Lacks key flavor
    ]
    
    for test in test_cases:
        adjusted = adjust_rating(**test)
        print(f"Base Rating: {test['base_rating']}, Sentiment: {test['sentiment_score']}, Adjusted Rating: {adjusted}")