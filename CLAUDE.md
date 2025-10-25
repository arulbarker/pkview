# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Application Overview

**TikTok Live PK Battle Application** - A PyQt6 desktop app that displays real-time animated bubbles for TikTok Live events with a competitive PK (Player Knockout) battle mode between two teams.

## Running the Application

```bash
# Development
python main.py

# Testing without launch window
python test_launch.py

# Run test suite
python test_pk_system.py
```

## Building

```bash
# Windows executable
build.bat
# or
pyinstaller build.spec
```

Output: `dist/TikTokLiveBubble.exe`

## Architecture Overview

### Two Window Modes

The application has **two distinct window implementations**:

1. **`main_window.py`** - Original bubble animation system (legacy, simple mode)
2. **`pk_main_window.py`** - PK Battle Mode (current active implementation)

The entry point (`main.py`) currently imports `PKMainWindow` from `pk_main_window.py`.

### Core System Components

#### PK Battle System (`pk_battle_system.py`)
- Soccer-style scoring: `[5] - [3]` format
- Round-based timer (default 60 minutes, configurable)
- Point calculation: `1 coin = 5 points`, `1 like/comment = 1 point`
- Auto-reset after round completion
- Signals: `points_updated`, `score_updated`, `timer_updated`, `round_won`, `round_reset`

#### Event Flow Architecture

```
TikTok Live Event
    ↓
tiktok_handler.py (QThread)
    ↓ emits event_received(dict)
pk_main_window.py → _on_tiktok_event()
    ↓
    ├─ Gift? → _handle_gift_event()
    │   ├─ Check gift_assignments (Team A/B)
    │   ├─ Calculate points (coins × 5)
    │   ├─ pk_system.add_gift_points()
    │   ├─ Play sound if enabled
    │   └─ Create bubble in BOTTOM zone (directional)
    │
    └─ Other? → _handle_bubble_event()
        ├─ Like/Comment? → add_interaction_points()
        ├─ Play event sound if enabled
        └─ Create bubble at configured position
```

### Widget System

#### Draggable Elements (`draggable_label.py`, `photo_manager.py`)
All major UI elements are draggable, resizable, and rotatable:
- **DraggableLabel**: Score, timer, and points displays
  - Manual painting with QPainter (no `super().paintEvent()` to avoid crashes)
  - Custom colors per instance
  - Rotation: `Ctrl + Mouse Wheel`
  - Resize: Drag corners
  - State persistence via `get_state()`/`set_state()`

- **DraggablePhoto**: Team photos
  - Circular crop with team color borders (Red: Team A, Teal: Team B)
  - Size limits: 100-600px
  - Rotation support with proper `painter.save()`/`restore()`

**Critical Implementation Detail**: DraggableLabel uses **manual painting** in `paintEvent()` without calling `super().paintEvent()` after applying transforms. This prevents QPainter state conflicts that cause crashes.

#### Bubble System (`bubble_widget.py`)
- Loads user avatars asynchronously via `QNetworkAccessManager`
- Creates placeholder avatars with user initials if loading fails
- Applies tier-based sizing for gifts (MICRO to MEGA)
- Positioned in three zones:
  - **TOP zone** (200px height): Like/Comment bubbles (configurable positions)
  - **CENTER zone** (600px height): PK battle view with draggable elements
  - **BOTTOM zone** (200px height): Gift bubbles (directional by team)

### Configuration System

#### Assignment Widgets (JSON-backed)
1. **`gift_assignment_widget.py`** → `gift_assignment.json`
   - Maps each TikTok gift to Team A or Team B
   - 16+ gifts from `gift_tiers.py` (Rose to Universe)

2. **`interaction_assignment_widget.py`** → `interaction_assignment.json`
   - Assigns Like/Comment events to teams
   - Each interaction type can go to different teams

3. **`bubble_position_widget.py`** → `bubble_positions.json`
   - Configures where Like/Comment bubbles appear
   - Options: `top`, `bottom`, `left`, `right` (not center)

4. **`event_sound_widget.py`** → `event_sounds.json`
   - Per-event sound file configuration
   - On/off toggle for each event type
   - Supports: Win sounds, Like, Comment, Share, Follow, Join, Gift

#### Gift Tier System (`gift_tiers.py`)
Maps TikTok gift names to coin values and tier classifications:
```python
GIFT_TIER_CONFIG = {
    'MICRO': {'min': 1, 'max': 10, 'size': 120, ...},
    'SMALL': {'min': 11, 'max': 100, ...},
    # ... up to MEGA tier
}
```

### Effects System (`effects.py`)

18+ animation effects using `QPropertyAnimation`:
- `fade_in_out`, `sparkle_zoom`, `slide_bounce`, `float_away`
- `heart_pulse`, `quick_pop`, `firework`, `rainbow`, `shake`, `spiral`
- Effects registered in `EFFECT_REGISTRY` dict
- Applied via `widget.start_animation()` in `BubbleWidget.showEvent()`

## Key Implementation Patterns

### Signal/Slot Architecture
All cross-component communication uses Qt signals:
```python
# TikTok Handler → Main Window
self.tiktok_handler.event_received.connect(self._on_tiktok_event)

# PK System → Main Window
self.pk_system.points_updated.connect(self._on_points_updated)
self.pk_system.round_won.connect(self._on_round_won)

# Assignment Widgets → Main Window
self.gift_assignment_widget.assignment_changed.connect(...)
```

### Thread Safety
- `TikTokThread` runs in separate QThread
- Emits signals to main thread for UI updates
- Never directly manipulate UI from worker thread

### Bubble Lifecycle
```python
# Creation
bubble = BubbleWidget(parent, event_data)
bubble.move(x, y)
bubble.show()
self.active_bubbles.append(bubble)

# Auto-cleanup with error handling
QTimer.singleShot(duration + 1000, lambda: self._cleanup_bubble(bubble))

# Cleanup (with try-except to prevent crashes)
def _cleanup_bubble(self, bubble):
    try:
        if bubble in self.active_bubbles:
            self.active_bubbles.remove(bubble)
        if bubble and not bubble.isHidden():
            bubble.deleteLater()
    except RuntimeError:
        pass  # Already deleted
```

### Rotation Implementation
Rotation uses QPainter transforms in `paintEvent()`:
```python
if self.rotation_angle != 0:
    painter.save()
    center = self.rect().center()
    painter.translate(center.x(), center.y())
    painter.rotate(self.rotation_angle)
    painter.translate(-center.x(), -center.y())
    # Draw content
    painter.restore()
```

**Never call `super().paintEvent(event)` after applying transforms** - causes crashes. Use manual drawing instead.

## Common Issues & Solutions

### Bubble Cleanup RuntimeError
**Problem**: `RuntimeError: wrapped C/C++ object of type BubbleWidget has been deleted`

**Solution**: Wrap `bubble.deleteLater()` in try-except and check `isHidden()` before deleting.

### PaintEvent Crashes
**Problem**: App crashes on launch with rotation enabled

**Solution**: Don't call `super().paintEvent()` after applying QPainter transforms. Draw manually.

### Photo Rotation Artifacts
**Problem**: Rotated photos show rendering issues

**Solution**: Use `painter.save()`/`restore()` around rotation transforms and ensure `SmoothPixmapTransform` hint is set.

## Testing

### Simulation Mode
All tabs have testing capabilities:
- **Test tab**: Simulate events without TikTok connection
- `_simulate_event(event_type)`: Creates fake events with dummy data
- `_simulate_gift(team)`: Tests gift point calculation
- Use `DUMMY_USERS` and `DUMMY_COMMENTS` from `config.py`

### Test Files
- `test_pk_system.py`: PK battle system unit tests
- `test_launch.py`: Import verification and basic launch test
- `minimal_test.py`: Minimal widget test for debugging

## Sound System

Managed by `sound_manager.py` using `QMediaPlayer`:
- One player per sound type to allow overlapping
- `play_team_win(team)`: Win celebration sounds
- `play_event_sound(event_type, sound_file)`: Dynamic event sounds
- Creates placeholder empty files if sound files don't exist

Place MP3 files in `sounds/` directory:
- `team_a_win.mp3`, `team_b_win.mp3`
- `like.mp3`, `comment.mp3`, `gift.mp3`, etc.

## UI Layout (pk_main_window.py)

### Vertical Arrangement in Horizontal Window (1920×1080)
```
┌─────────────────────────────────────┐
│ TOP Zone (200px) - Bubble container │  ← Like/Comment bubbles
├─────────────────────────────────────┤
│ CENTER Zone (600px) - PK View       │  ← Battle display
│  ├─ Score (draggable/rotatable)    │
│  ├─ Timer (draggable/rotatable)    │
│  ├─ Photos (Team A vs B)           │
│  ├─ Points labels (draggable)      │
│  └─ Progress bar                   │
├─────────────────────────────────────┤
│ BOTTOM Zone (200px) - Bubble zone  │  ← Gift bubbles (directional)
└─────────────────────────────────────┘
```

Content is arranged vertically within a horizontal window for portrait streaming (rotate monitor or in OBS).

## Tab System (8 Tabs)
1. **Battle**: Start/Pause/Reset, round duration, volume
2. **TikTok**: Connect to live stream
3. **Photos**: Upload Team A/B photos
4. **Gifts**: Assign gifts to teams
5. **Like/Comment**: Assign interactions to teams
6. **Posisi Bubble**: Configure bubble spawn positions
7. **Suara**: Event sound settings with on/off toggles
8. **Test**: Event simulation for testing

## State Persistence

JSON files auto-generated in root directory:
- `gift_assignment.json`: Gift → Team mappings
- `interaction_assignment.json`: Like/Comment → Team
- `bubble_positions.json`: Bubble spawn positions
- `event_sounds.json`: Sound file paths and enabled states

All loaded on startup if present.

## Custom Colors

Elements use custom color schemes:
- **Score**: White text, dark background
- **Timer**: Gold (`#FFD700`) text, dark background
- **Points Team A**: Red (`#FF6B6B`)
- **Points Team B**: Teal (`#4ECDC4`)

Set via `DraggableLabel` constructor parameters:
```python
label = DraggableLabel(parent, text, font_size=32,
                       text_color="#FF6B6B",
                       bg_color="rgba(255, 107, 107, 0.3)",
                       border_color="#FF6B6B")
```

## Performance Considerations

- Bubble cleanup uses `QTimer.singleShot` to avoid blocking
- Avatar loading is asynchronous with 3-second timeout
- Animation effects use hardware-accelerated `QPropertyAnimation`
- Maximum bubble tracking via `active_bubbles` list
- Efficient QPainter usage with proper save/restore states
