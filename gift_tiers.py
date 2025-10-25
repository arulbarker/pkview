"""
Gift Tier System
Different effects and sizes based on gift value
"""

# Gift tier configuration
GIFT_TIERS = {
    'micro': {
        'name': 'Micro Gift',
        'min_value': 1,
        'max_value': 10,
        'effect': 'quick_pop',
        'size': 140,
        'duration': 2000,
        'color': '#FFA500',  # Orange
        'border_width': 3,
        'glow_intensity': 40,
        'sound': 'pop.wav',
        'description': 'Small appreciation'
    },
    'small': {
        'name': 'Small Gift',
        'min_value': 11,
        'max_value': 50,
        'effect': 'bounce_cascade',
        'size': 180,
        'duration': 3000,
        'color': '#FFD700',  # Gold
        'border_width': 4,
        'glow_intensity': 60,
        'sound': 'bling.wav',
        'description': 'Nice gift!'
    },
    'medium': {
        'name': 'Medium Gift',
        'min_value': 51,
        'max_value': 200,
        'effect': 'sparkle_zoom',
        'size': 240,
        'duration': 4000,
        'color': '#FF1493',  # Deep Pink
        'border_width': 5,
        'glow_intensity': 80,
        'sound': 'sparkle.wav',
        'description': 'Great support!'
    },
    'large': {
        'name': 'Large Gift',
        'min_value': 201,
        'max_value': 1000,
        'effect': 'explosion_particles',
        'size': 300,
        'duration': 5000,
        'color': '#9400D3',  # Dark Violet
        'border_width': 6,
        'glow_intensity': 100,
        'sound': 'explosion.wav',
        'description': 'Amazing generosity!'
    },
    'mega': {
        'name': 'MEGA GIFT',
        'min_value': 1001,
        'max_value': 999999,
        'effect': 'screen_takeover',
        'size': 400,
        'duration': 8000,
        'color': '#FF0000',  # Red
        'border_width': 8,
        'glow_intensity': 150,
        'sound': 'mega.wav',
        'screen_shake': True,
        'description': '🔥 LEGENDARY SUPPORT! 🔥'
    }
}

# TikTok gift value mapping (approximate coin values)
TIKTOK_GIFT_VALUES = {
    'Rose': 1,
    'TikTok': 1,
    'Finger Heart': 5,
    'Doughnut': 30,
    'Heart': 10,
    'Rainbow Puke': 100,
    'Drama Queen': 5000,
    'Motorcycle': 100,
    'Sports Car': 1000,
    'Yacht': 7000,
    'Castle': 20000,
    'Planet': 40000,
    'Universe': 50000,
    'Lion': 29999,
    'Falcon': 10999,
    'Drama King': 5000,
}


def get_gift_tier(gift_value):
    """
    Get gift tier based on value

    Args:
        gift_value: Coin value of the gift

    Returns:
        dict: Tier configuration
    """
    for tier_name, tier_config in GIFT_TIERS.items():
        if tier_config['min_value'] <= gift_value <= tier_config['max_value']:
            return tier_config

    # Default to small if not found
    return GIFT_TIERS['small']


def get_gift_value_from_name(gift_name):
    """
    Get gift coin value from TikTok gift name

    Args:
        gift_name: Name of the TikTok gift

    Returns:
        int: Coin value
    """
    return TIKTOK_GIFT_VALUES.get(gift_name, 1)


def get_tier_name(gift_value):
    """Get tier name from gift value"""
    tier = get_gift_tier(gift_value)
    return tier['name']


# Example usage:
if __name__ == '__main__':
    # Test different gift values
    test_values = [1, 5, 50, 100, 500, 5000]

    for value in test_values:
        tier = get_gift_tier(value)
        print(f"Gift value {value}: {tier['name']} - Effect: {tier['effect']}")

    # Test TikTok gifts
    print("\nTikTok Gift Examples:")
    test_gifts = ['Rose', 'Castle', 'Universe', 'Lion']
    for gift in test_gifts:
        value = get_gift_value_from_name(gift)
        tier = get_gift_tier(value)
        print(f"{gift} ({value} coins): {tier['name']}")
