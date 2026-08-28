# Skeleton data for Tarot module
TAROT_DECK = {
    "fool": {"name": "The Fool", "meaning": "New beginnings, spontaneity, and a free spirit."},
    "magician": {"name": "The Magician", "meaning": "Manifestation, resourcefulness, power, and inspired action."},
    # Add more cards as needed
}

def get_random_card():
    import random
    return random.choice(list(TAROT_DECK.values()))
