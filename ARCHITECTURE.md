# 🏗️ Architecture Documentation

Dokumentasi arsitektur dan struktur kode TikTok Live Bubble Application.

## 📐 System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Main Application                      │
│                     (main.py)                           │
└────────────────┬────────────────────────────────────────┘
                 │
                 ├─────────────────────────────────────────┐
                 │                                         │
         ┌───────▼────────┐                     ┌─────────▼─────────┐
         │  Main Window   │                     │  TikTok Handler   │
         │ (main_window.py)│◄────signals────────┤(tiktok_handler.py)│
         └───────┬────────┘                     └─────────┬─────────┘
                 │                                         │
                 │                                         │
    ┌────────────┼────────────┐                  ┌────────▼────────┐
    │            │            │                  │  TikTokLive     │
┌───▼───┐  ┌────▼────┐  ┌───▼────┐            │   Library       │
│Bubble │  │Controls │  │  Log   │            └─────────────────┘
│Widget │  │ Panel   │  │ Panel  │
└───┬───┘  └─────────┘  └────────┘
    │
┌───▼───────┐
│  Effects  │
│(effects.py)│
└───────────┘
```

## 📁 File Structure & Responsibilities

### Core Files

#### 1. `main.py` - Application Entry Point
**Purpose**: Bootstrap aplikasi

**Responsibilities**:
- Initialize QApplication
- Create main window
- Setup high DPI scaling
- Start event loop

**Key Code**:
```python
app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())
```

---

#### 2. `main_window.py` - Main UI Controller
**Purpose**: Main window dan UI management

**Responsibilities**:
- Create dan manage UI layout
- Handle user interactions
- Coordinate antara components
- Manage application state

**Components**:
```
MainWindow
├── Bubble Container (QFrame)
│   └── Multiple Bubble Widgets
├── Control Panel (QWidget)
│   ├── Connection Controls
│   ├── Simulation Panel
│   ├── Event Log
│   └── Settings
```

**Key Methods**:
- `_create_bubble_container()`: Setup bubble display area
- `_create_control_panel()`: Setup control UI
- `_on_event_received()`: Handle TikTok events
- `_create_bubble()`: Create dan show bubble widget
- `_simulate_event()`: Simulate events for testing

**Signals**:
```python
# From TikTok Handler
event_received(dict) → _on_event_received()
connection_status(str) → _on_connection_status()
error_occurred(str) → _on_error()
log_message(str) → _add_log()
```

---

#### 3. `bubble_widget.py` - Bubble Component
**Purpose**: Individual bubble widget dengan animasi

**Responsibilities**:
- Display user avatar
- Show username dan event info
- Custom painting (circular bubble)
- Avatar loading (network)
- Start animation effect

**Lifecycle**:
```
Create → Load Avatar → Paint → Show → Animate → Delete
```

**Key Methods**:
- `_setup_ui()`: Initialize bubble properties
- `_load_avatar()`: Load dari URL atau create placeholder
- `paintEvent()`: Custom drawing
- `start_animation()`: Trigger animation effect

**Custom Painting**:
```python
paintEvent():
├── _draw_bubble_background()  # Gradient circle
├── _draw_avatar()              # User picture
├── _draw_username()            # Name text
├── _draw_emoji()               # Event emoji
└── _draw_event_info()          # Additional info
```

---

#### 4. `effects.py` - Animation Effects Library
**Purpose**: Collection of reusable animation effects

**Responsibilities**:
- Define animation effects
- Provide modular animations
- Handle timing dan easing
- Manage animation lifecycle

**Structure**:
```python
class BubbleEffects:
    @staticmethod
    def effect_name(widget, duration):
        # Create animations
        # Setup timing
        # Return animation group

EFFECT_REGISTRY = {
    'effect_name': BubbleEffects.effect_name,
    # ...
}
```

**Animation Framework**:
```
QPropertyAnimation
├── Opacity (QGraphicsOpacityEffect)
├── Geometry (position & size)
├── Position (movement)
└── Custom Properties

Animation Groups
├── QSequentialAnimationGroup (one after another)
└── QParallelAnimationGroup (simultaneous)
```

**10 Built-in Effects**:
1. fade_in_out
2. sparkle_zoom
3. slide_bounce
4. float_away
5. heart_pulse
6. quick_pop
7. firework_explosion
8. rainbow_rotate
9. shake_vibrate
10. spiral_in

---

#### 5. `tiktok_handler.py` - TikTok Live Integration
**Purpose**: Handle TikTok Live connection dan events

**Responsibilities**:
- Connect to TikTok Live
- Process live events
- Emit signals to UI
- Handle reconnection
- Error handling

**Classes**:

**TikTokHandler (QObject)**:
```python
Signals:
├── event_received(dict)     # New event data
├── connection_status(str)   # Connection updates
├── error_occurred(str)      # Error messages
└── log_message(str)         # Log entries

Methods:
├── connect_to_live()        # Start connection
├── disconnect_from_live()   # Stop connection
└── _register_events()       # Setup event handlers
```

**TikTokThread (QThread)**:
```python
# Run TikTok client in background thread
# Prevents UI blocking
```

**Event Flow**:
```
TikTok Live Event
    ↓
TikTokLive Library
    ↓
Event Handler (@client.on)
    ↓
Process Event Data
    ↓
Emit Signal (event_received)
    ↓
MainWindow._on_event_received()
    ↓
Create Bubble Widget
```

**Supported Events**:
- ConnectEvent
- DisconnectEvent
- JoinEvent
- CommentEvent
- GiftEvent
- ShareEvent
- FollowEvent
- LikeEvent

---

#### 6. `config.py` - Configuration
**Purpose**: Central configuration file

**Responsibilities**:
- Define constants
- Event configurations
- Effect settings
- Dummy data for simulation

**Sections**:
```python
# Window Settings
WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE

# Bubble Settings
BUBBLE_MIN_SIZE, BUBBLE_MAX_SIZE, BUBBLE_DURATION

# Event Configurations
EVENT_CONFIGS = {
    'event_type': {
        'size': int,
        'duration': int,
        'color': str,
        'emoji': str,
        'effect': str
    }
}

# Effect Settings
EFFECTS_CONFIG

# TikTok Settings
TIKTOK_USERNAME, RECONNECT_DELAY, MAX_RECONNECT_ATTEMPTS

# Dummy Data
DUMMY_USERS, DUMMY_GIFTS, DUMMY_COMMENTS
```

---

## 🔄 Data Flow

### Real TikTok Live Flow

```
User Interaction (TikTok Live)
    ↓
TikTok Server
    ↓
TikTokLive Library (websocket)
    ↓
TikTokHandler Event Callback
    ↓
Data Processing & Formatting
    ↓
Signal Emission (event_received)
    ↓
MainWindow._on_event_received()
    ↓
Create Event Data Dictionary
    ↓
BubbleWidget(parent, event_data)
    ↓
Load Avatar (network request)
    ↓
Show Widget
    ↓
Start Animation (from EFFECT_REGISTRY)
    ↓
Animation Complete
    ↓
Widget Deleted
```

### Simulation Flow

```
User Click (Simulation Button)
    ↓
MainWindow._simulate_event(type)
    ↓
Random Dummy Data Selection
    ↓
Create Event Data Dictionary
    ↓
BubbleWidget(parent, event_data)
    ↓
[Same as Real Flow from here]
```

---

## 🎨 UI Component Tree

```
QMainWindow (MainWindow)
└── QWidget (centralWidget)
    └── QHBoxLayout
        └── QSplitter
            ├── QFrame (bubble_container) [80%]
            │   └── Multiple BubbleWidget instances
            │       ├── Custom painted content
            │       └── QGraphicsOpacityEffect
            │
            └── QWidget (control_panel) [20%]
                └── QVBoxLayout
                    ├── QGroupBox (Connection)
                    │   ├── QLineEdit (username_input)
                    │   ├── QPushButton (connect_btn)
                    │   ├── QPushButton (disconnect_btn)
                    │   └── QLabel (status_label)
                    │
                    ├── QGroupBox (Simulation)
                    │   ├── QPushButton (join_btn)
                    │   ├── QPushButton (gift_btn)
                    │   ├── QPushButton (comment_btn)
                    │   ├── QPushButton (share_btn)
                    │   ├── QPushButton (follow_btn)
                    │   ├── QPushButton (like_btn)
                    │   └── QPushButton (rapid_test_btn)
                    │
                    ├── QGroupBox (Log)
                    │   ├── QTextEdit (log_text)
                    │   └── QPushButton (clear_log_btn)
                    │
                    └── QGroupBox (Settings)
                        ├── QPushButton (fullscreen_btn)
                        └── QComboBox (effect_combo)
```

---

## 🧵 Threading Model

### Main Thread
- UI rendering
- User interaction
- Bubble animations
- Window management

### TikTok Thread
- TikTok Live connection
- WebSocket communication
- Event processing
- Signal emission

**Communication**: Qt Signals/Slots (thread-safe)

```python
# TikTok Thread
self.event_received.emit(event_data)
    ↓ (signal/slot mechanism)
# Main Thread
@pyqtSlot(dict)
def _on_event_received(self, event_data):
    # Safe to update UI here
```

---

## 🎯 Design Patterns Used

### 1. **Signal-Slot Pattern** (Observer)
```python
# Publisher
class TikTokHandler(QObject):
    event_received = pyqtSignal(dict)

# Subscriber
handler.event_received.connect(self._on_event_received)
```

### 2. **Factory Pattern**
```python
# Effect Factory
effect_func = EFFECT_REGISTRY.get(effect_name)
effect_func(widget, duration)
```

### 3. **Strategy Pattern**
```python
# Different animation strategies
class BubbleEffects:
    @staticmethod
    def fade_in_out(widget, duration): ...

    @staticmethod
    def sparkle_zoom(widget, duration): ...
```

### 4. **Template Method**
```python
# BubbleWidget.paintEvent()
def paintEvent(self, event):
    painter = QPainter(self)
    self._draw_bubble_background(painter)
    self._draw_avatar(painter)
    self._draw_username(painter)
    # Each step can be overridden
```

### 5. **Singleton-like Config**
```python
# config.py - single source of truth
import config
config.WINDOW_WIDTH
```

---

## 🔌 Extension Points

### Add New Effect

```python
# 1. Define in effects.py
@staticmethod
def my_effect(widget, duration):
    # Implementation

# 2. Register
EFFECT_REGISTRY['my_effect'] = BubbleEffects.my_effect

# 3. Use in config
EVENT_CONFIGS['gift']['effect'] = 'my_effect'
```

### Add New Event Type

```python
# 1. Add config
EVENT_CONFIGS['new_event'] = {
    'size': 120,
    'duration': 3000,
    'color': '#FF0000',
    'emoji': '🆕',
    'effect': 'fade_in_out'
}

# 2. Add TikTok handler
@self.client.on(NewEvent)
async def on_new(event: NewEvent):
    event_data = {'type': 'new_event', ...}
    self.event_received.emit(event_data)

# 3. Add simulation
self._simulate_event('new_event')
```

### Custom Bubble Widget

```python
# Inherit and override
class CustomBubbleWidget(BubbleWidget):
    def _draw_bubble_background(self, painter):
        # Custom background
        pass

    def _draw_avatar(self, painter):
        # Custom avatar rendering
        pass
```

---

## 📊 Performance Considerations

### Memory Management

**Bubble Lifecycle**:
```python
create → show → animate → (auto-delete after duration)
```

**Cleanup**:
```python
# Animation groups cleanup
anim_group.finished.connect(widget.deleteLater)

# Parent tracking
self.active_bubbles.append(bubble)
QTimer.singleShot(duration, lambda: self._cleanup_bubble(bubble))
```

### Optimization Strategies

1. **Limit Concurrent Bubbles**
```python
MAX_BUBBLES = 10
if len(active_bubbles) >= MAX_BUBBLES:
    oldest.deleteLater()
```

2. **Avatar Caching**
```python
# TODO: Implement avatar cache
avatar_cache = {}
if url in avatar_cache:
    return avatar_cache[url]
```

3. **Throttle High-Frequency Events**
```python
# Only show every Nth like
if like_count % 10 == 0:
    emit_event()
```

4. **Reuse Animation Objects**
```python
# Animation pools for common effects
# Reduce object creation overhead
```

---

## 🔒 Security Considerations

### Input Validation
```python
# Username sanitization
username = username.strip().lstrip('@')
if not username:
    return error
```

### Network Safety
```python
# Avatar loading with timeout
reply.finished.connect(lambda: self._on_avatar_loaded(reply))
# Handle network errors gracefully
```

### Dependency Management
```python
# Pinned versions in requirements.txt
PyQt6>=6.6.0
TikTokLive>=5.0.0
```

---

## 🧪 Testing Strategy

### Manual Testing
```python
# Simulation panel provides:
- Individual event testing
- Rapid batch testing
- Visual verification
- Log verification
```

### Unit Testing (Future)
```python
# tests/test_effects.py
def test_fade_in_out():
    widget = MockWidget()
    effect = BubbleEffects.fade_in_out(widget, 1000)
    assert effect is not None

# tests/test_bubble_widget.py
def test_bubble_creation():
    data = {'type': 'gift', ...}
    bubble = BubbleWidget(None, data)
    assert bubble.bubble_color is not None
```

---

## 📦 Build Process

### PyInstaller Configuration

```
build.spec
├── Analysis (scan imports)
├── PYZ (package python files)
└── EXE (create executable)
    ├── Include all .py files
    ├── Include assets
    ├── Bundle dependencies
    └── Set console=False (no terminal)
```

### Build Steps
```
1. Analyze dependencies
2. Collect all imports
3. Bundle into .exe
4. Include Qt plugins
5. Package in dist folder
```

---

## 🚀 Deployment

### Portable Distribution
```
dist/
├── TikTokLiveBubble.exe
├── Qt6 DLLs
├── Python runtime
└── Dependencies
```

### Requirements
- Windows 10/11
- No Python installation needed
- No admin rights needed
- ~100-200MB total size

---

## 🔄 Future Improvements

### Planned Features
1. **Particle System**
   - Confetti
   - Sparkles
   - Fireworks particles

2. **Sound Effects**
   - Event sounds
   - Background music
   - Text-to-speech

3. **Database Integration**
   - Event history
   - Statistics
   - Analytics

4. **AI Features**
   - Sentiment analysis
   - Auto-moderation
   - Smart filtering

5. **Advanced Graphics**
   - 3D effects
   - Shader effects
   - Video backgrounds

### Architecture Improvements
1. Plugin system for effects
2. Theme system
3. Multi-language support
4. Cloud sync settings

---

## 📚 Dependencies Map

```
Application
├── PyQt6 (UI Framework)
│   ├── QtCore (signals, threads, timers)
│   ├── QtGui (painting, colors, fonts)
│   ├── QtWidgets (UI components)
│   └── QtNetwork (avatar loading)
│
├── TikTokLive (Live integration)
│   └── websocket connection
│
├── Pillow (image processing)
├── requests (HTTP requests)
└── PyInstaller (build tool)
```

---

## 🎓 Learning Resources

### To Understand This Code

**PyQt6**:
- [Official Docs](https://doc.qt.io/qtforpython/)
- Animation Framework
- Custom Widgets
- Signal/Slot mechanism

**TikTokLive**:
- [GitHub](https://github.com/isaackogan/TikTokLive)
- Event types
- WebSocket protocol

**Design Patterns**:
- Observer (Signal/Slot)
- Factory (Effect Registry)
- Strategy (Animation Effects)

---

**Architecture crafted with ❤️**
