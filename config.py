"""
Configuration file for TikTok Live Bubble Application
"""

# Window Settings
WINDOW_WIDTH = 1920
WINDOW_HEIGHT = 1080
WINDOW_TITLE = "TikTok Live Bubble Animation"

# Ratio Modes (Flexible aspect ratios)
RATIO_MODES = {
    'vertical': {
        'width': 1080,
        'height': 1920,
        'name': '📱 Vertical (9:16)',
        'description': 'Mobile portrait mode'
    },
    'horizontal': {
        'width': 1920,
        'height': 1080,
        'name': '🖥️ Horizontal (16:9)',
        'description': 'Desktop landscape mode'
    },
    'square': {
        'width': 1080,
        'height': 1080,
        'name': '⬛ Square (1:1)',
        'description': 'Instagram/Social media format'
    }
}
DEFAULT_RATIO = 'horizontal'  # Default ratio mode

# Bubble Settings
BUBBLE_MIN_SIZE = 80
BUBBLE_MAX_SIZE = 200
BUBBLE_DURATION = 3000  # milliseconds
BUBBLE_FADE_DURATION = 500  # milliseconds

# Event Type Configurations
EVENT_CONFIGS = {
    'join': {
        'size': 100,
        'duration': 2000,
        'color': '#4CAF50',
        'emoji': '👋',
        'effect': 'fade_in_out'
    },
    'gift': {
        'size': 280,  # Much larger! Was 180
        'duration': 5000,  # Longer duration to appreciate
        'color': '#FFD700',
        'emoji': '🎁',
        'effect': 'sparkle_zoom',
        'special': True,  # Flag for special treatment
        'avatar_size_ratio': 0.5  # 50% of bubble = larger photo
    },
    'comment': {
        'size': 120,
        'duration': 3000,
        'color': '#2196F3',
        'emoji': '💬',
        'effect': 'slide_bounce'
    },
    'share': {
        'size': 110,
        'duration': 2500,
        'color': '#FF5722',
        'emoji': '🔗',
        'effect': 'float_away'
    },
    'follow': {
        'size': 140,
        'duration': 3500,
        'color': '#E91E63',
        'emoji': '❤️',
        'effect': 'heart_pulse'
    },
    'like': {
        'size': 90,
        'duration': 1500,
        'color': '#FF69B4',
        'emoji': '👍',
        'effect': 'quick_pop'
    }
}

# Animation Effects Settings
EFFECTS_CONFIG = {
    'particle_count': 20,
    'sparkle_intensity': 0.8,
    'glow_radius': 30,
    'shake_intensity': 5,
    'bounce_height': 50,
    'rotation_degrees': 360,
    'trail_length': 10
}

# TikTok Settings
TIKTOK_USERNAME = ""  # Will be set from UI
RECONNECT_DELAY = 5000  # milliseconds
MAX_RECONNECT_ATTEMPTS = 5

# Dummy Data for Simulation
DUMMY_USERS = [
    {"username": "user_001", "nickname": "Alice", "avatar": "https://i.pravatar.cc/150?img=1"},
    {"username": "user_002", "nickname": "Bob", "avatar": "https://i.pravatar.cc/150?img=2"},
    {"username": "user_003", "nickname": "Charlie", "avatar": "https://i.pravatar.cc/150?img=3"},
    {"username": "user_004", "nickname": "Diana", "avatar": "https://i.pravatar.cc/150?img=4"},
    {"username": "user_005", "nickname": "Eve", "avatar": "https://i.pravatar.cc/150?img=5"},
]

DUMMY_GIFTS = [
    # MICRO tier (1-10 coins)
    {"name": "Rose", "emoji": "🌹", "value": 1},
    {"name": "TikTok", "emoji": "🎵", "value": 1},
    {"name": "Finger Heart", "emoji": "💗", "value": 5},

    # SMALL tier (11-50 coins)
    {"name": "Heart", "emoji": "❤️", "value": 10},
    {"name": "Doughnut", "emoji": "🍩", "value": 30},

    # MEDIUM tier (51-200 coins)
    {"name": "Rainbow Puke", "emoji": "🌈", "value": 100},
    {"name": "Motorcycle", "emoji": "🏍️", "value": 100},

    # LARGE tier (201-1000 coins)
    {"name": "Sports Car", "emoji": "🏎️", "value": 1000},

    # MEGA tier (1001+ coins)
    {"name": "Drama Queen", "emoji": "👑", "value": 5000},
    {"name": "Yacht", "emoji": "🛥️", "value": 7000},
    {"name": "Castle", "emoji": "🏰", "value": 20000},
    {"name": "Lion", "emoji": "🦁", "value": 29999},
    {"name": "Planet", "emoji": "🪐", "value": 40000},
    {"name": "Universe", "emoji": "🌌", "value": 50000},
]

DUMMY_COMMENTS = [
    "Amazing stream! 🔥",
    "Love your content!",
    "Hello from Indonesia! 🇮🇩",
    "You're the best! ❤️",
    "Keep it up!",
    "This is so cool! 😎",
]
