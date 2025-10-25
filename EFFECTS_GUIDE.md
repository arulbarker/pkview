# 🎨 Panduan Lengkap Efek Animasi

Dokumen ini menjelaskan semua efek animasi yang tersedia di TikTok Live Bubble Application, termasuk karakteristik, use case terbaik, dan cara customization.

## 📚 Daftar Efek

1. [Fade In Out](#1-fade-in-out)
2. [Sparkle Zoom](#2-sparkle-zoom)
3. [Slide Bounce](#3-slide-bounce)
4. [Float Away](#4-float-away)
5. [Heart Pulse](#5-heart-pulse)
6. [Quick Pop](#6-quick-pop)
7. [Firework Explosion](#7-firework-explosion)
8. [Rainbow Rotate](#8-rainbow-rotate)
9. [Shake Vibrate](#9-shake-vibrate)
10. [Spiral In](#10-spiral-in)

---

## 1. Fade In Out

### 📝 Deskripsi
Efek fade sederhana dan elegan. Bubble muncul dengan fade in, hold sebentar, lalu fade out.

### ✨ Karakteristik
- **Durasi**: Customizable (default 2000ms)
- **Easing**: InOutQuad (smooth acceleration/deceleration)
- **Opacity**: 0 → 1 → 1 → 0
- **Position**: Static (tidak bergerak)
- **Impact Level**: Low (subtle)

### 🎯 Use Case Terbaik
- User join events
- Background notifications
- Low-priority events
- Minimalist design preference

### ⚙️ Customization

```python
# Duration breakdown
fade_in: 25% of total duration
hold: 50% of total duration
fade_out: 25% of total duration

# Example: 4000ms total
# - Fade in: 1000ms
# - Hold: 2000ms
# - Fade out: 1000ms
```

### 💡 Tips
- Cocok untuk event yang sering terjadi (tidak overwhelming)
- Bisa dikombinasikan dengan sound effect untuk impact lebih
- Ideal untuk background ambient notifications

---

## 2. Sparkle Zoom

### 📝 Deskripsi
Zoom in dari kecil dengan efek berkilau. Bubble mulai kecil, membesar dengan elastic effect, lalu kembali normal dan fade out. Includes optional sparkle particles.

### ✨ Karakteristik
- **Durasi**: Customizable (default 4000ms)
- **Easing**: OutElastic (bouncy zoom)
- **Scale**: 0.5x → 1.3x → 1.0x
- **Opacity**: 0 → 1 → 1 → 0
- **Impact Level**: Very High (eye-catching)

### 🎯 Use Case Terbaik
- **Gift events** (BEST!)
- High-value donations
- Special achievements
- VIP user actions
- Celebration moments

### ⚙️ Customization

```python
# Scale factors
small_size = start_rect.width() * 0.5  # Starting size
large_size = start_rect.width() * 1.3  # Peak size
normal_size = start_rect.width() * 1.0  # End size

# Timeline
0.0s: Scale 0.5x, Opacity 0
0.2s: Scale 1.3x, Opacity 1 (zoom in complete)
0.7s: Scale 1.3x, Opacity 1 (hold at large)
1.0s: Scale 1.0x, Opacity 0 (return & fade)
```

### 💡 Tips
- Untuk gift besar, increase scale ke 1.5x atau 1.8x
- Tambahkan sound effect "bling" atau "sparkle"
- Combine dengan particle effects untuk extra wow factor

### 🌟 Advanced: Sparkle Particles

```python
# Add sparkle particles (future enhancement)
def _add_sparkles(widget, duration):
    particle_count = 20
    for i in range(particle_count):
        # Create small sparkle widgets
        # Animate outward from center
        # Fade out quickly
        pass
```

---

## 3. Slide Bounce

### 📝 Deskripsi
Slide dari samping kiri atau kanan dengan bouncing effect. Bubble masuk dengan bounce, hold, lalu fade out.

### ✨ Karakteristik
- **Durasi**: Customizable (default 3000ms)
- **Easing**: OutBounce (bouncy landing)
- **Direction**: Random (left or right)
- **Movement**: Horizontal slide
- **Impact Level**: High (dynamic)

### 🎯 Use Case Terbaik
- **Comment events** (BEST!)
- Chat messages
- User reactions
- Interactive content

### ⚙️ Customization

```python
# Direction options
from_left = True   # Slide from left edge
from_left = False  # Slide from right edge
from_left = random.choice([True, False])  # Random

# Starting position
if from_left:
    start_x = -bubble_width  # Off-screen left
else:
    start_x = screen_width   # Off-screen right

# Bounce intensity (via easing curve)
OutBounce  # Default (3-4 bounces)
InOutBounce  # Bounce in AND out
```

### 💡 Tips
- Untuk comment panjang, increase duration
- Bisa alternate direction untuk variasi
- Combine dengan text-to-speech untuk accessibility

---

## 4. Float Away

### 📝 Deskripsi
Bubble melayang ke atas screen sambil fade out. Movement smooth dengan slight horizontal drift.

### ✨ Karakteristik
- **Durasi**: Customizable (default 2500ms)
- **Easing**: InOutQuad (smooth)
- **Direction**: Upward with random drift
- **Movement**: Vertical + horizontal
- **Impact Level**: Medium (gentle)

### 🎯 Use Case Terbaik
- **Share events** (BEST!)
- User leave events
- Temporary notifications
- Ambient effects

### ⚙️ Customization

```python
# Vertical movement
start_y = current_position
end_y = -bubble_height  # Float to top of screen

# Horizontal drift
drift_x = random.randint(-50, 50)  # Random drift
end_x = start_x + drift_x

# Speed control
fast_float: duration = 1500ms
normal_float: duration = 2500ms
slow_float: duration = 4000ms
```

### 💡 Tips
- Untuk "blessed" effect, make drift upward only
- Increase drift range untuk more dynamic movement
- Combine dengan wind/particle effects

---

## 5. Heart Pulse

### 📝 Deskripsi
Pulsing effect seperti detak jantung. Bubble expand dan contract beberapa kali (default 3x) sebelum fade out.

### ✨ Karakteristik
- **Durasi**: Customizable (default 3500ms)
- **Easing**: OutQuad + InQuad (pulse)
- **Pulse Count**: 3 pulses
- **Scale**: 1.0x ↔ 1.2x
- **Impact Level**: High (romantic)

### 🎯 Use Case Terbaik
- **Follow events** (BEST!)
- Love/heart reactions
- Subscription events
- Romantic moments
- Health/wellness content

### ⚙️ Customization

```python
# Pulse parameters
pulse_count = 3  # Number of pulses
scale_factor = 1.2  # How much to expand (1.0 = no change)

# Pulse speed
for i in range(pulse_count):
    expand_duration = total_duration // (pulse_count * 2)
    contract_duration = total_duration // (pulse_count * 2)

# Pulse intensity options
gentle_pulse: scale = 1.1
normal_pulse: scale = 1.2
strong_pulse: scale = 1.4
```

### 💡 Tips
- Untuk dramatic effect, use 5-7 pulses
- Sync dengan heartbeat sound effect (60-80 BPM)
- Add red/pink glow effect during pulse

### ❤️ Advanced: Heart Shape

```python
# Future enhancement: actual heart shape
def _draw_heart_shape(painter, rect):
    path = QPainterPath()
    # Draw heart using bezier curves
    # ...
    painter.drawPath(path)
```

---

## 6. Quick Pop

### 📝 Deskripsi
Pop in/out cepat dengan bounce. Bubble mulai tiny, pop ke normal size, lalu shrink dan disappear.

### ✨ Karakteristik
- **Durasi**: Short (default 1500ms)
- **Easing**: OutBounce (energetic)
- **Scale**: Tiny → Normal → Tiny
- **Speed**: Fast
- **Impact Level**: Medium (snappy)

### 🎯 Use Case Terbaik
- **Like events** (BEST!)
- Quick reactions
- Rapid fire events
- Energy bursts
- Count milestones

### ⚙️ Customization

```python
# Scale timeline
0.0s: Scale 0.01x (tiny - almost invisible)
0.3s: Scale 1.0x (pop to full size)
1.0s: Scale 0.01x (shrink back)

# Speed variants
ultra_quick: 800ms
quick: 1500ms (default)
normal: 2000ms

# Tiny size
tiny_size = 10px  # Starting/ending size
```

### 💡 Tips
- Perfect for high-frequency events (likes, reactions)
- Batch multiple likes into one bubble with counter
- Add "pop" sound effect for satisfaction
- Consider throttling to avoid spam

---

## 7. Firework Explosion

### 📝 Deskripsi
Efek ledakan kembang api. Bubble fade out sementara particles terbang ke segala arah.

### ✨ Karakteristik
- **Durasi**: Customizable (default 2000ms)
- **Particles**: Multiple (8-20)
- **Direction**: Radial (all directions)
- **Colors**: Multi-color option
- **Impact Level**: Very High (spectacular)

### 🎯 Use Case Terbaik
- Special gifts (super gifts)
- Milestones (1000 viewers, etc.)
- Celebrations
- Big achievements
- Event highlights

### ⚙️ Customization

```python
# Particle settings
particle_count = 16  # Number of particles
explosion_radius = 200  # How far particles fly
particle_size = 10  # Size of each particle

# Color schemes
single_color: all particles same color
rainbow: each particle different color
gradient: particles fade from one color to another

# Explosion patterns
radial: particles fly in all directions (default)
upward: particles mostly fly upward (fountain)
circular: particles form expanding circle
```

### 💡 Tips
- Reserve for special moments only (high impact)
- Combine dengan screen shake untuk earthquake effect
- Add sound effect: explosion or firework
- Consider camera flash effect

### 🎆 Advanced: Particle System

```python
def _create_explosion_particles(widget, duration):
    center_x, center_y = widget.rect().center()

    for i in range(particle_count):
        angle = (360 / particle_count) * i
        distance = explosion_radius

        # Create particle widget
        particle = ParticleWidget(widget.parent())

        # Animate to position
        end_x = center_x + distance * cos(angle)
        end_y = center_y + distance * sin(angle)

        # Add physics (gravity, friction)
        # ...
```

---

## 8. Rainbow Rotate

### 📝 Deskripsi
Rainbow gradient dengan rotation effect. Colors cycle through spectrum.

### ✨ Karakteristik
- **Durasi**: Customizable (default 3000ms)
- **Colors**: Rainbow spectrum
- **Rotation**: Optional (if implemented)
- **Gradient**: Radial or linear
- **Impact Level**: High (colorful)

### 🎯 Use Case Terbaik
- Pride events
- Colorful celebrations
- Fun/party atmosphere
- Diversity celebrations
- Special themed events

### ⚙️ Customization

```python
# Rainbow colors (HSV)
colors = [
    QColor.fromHsv(h, 255, 255)
    for h in range(0, 360, 30)  # 12 colors
]

# Gradient types
radial_gradient: colors from center
linear_gradient: colors in direction
conical_gradient: colors rotate around center

# Animation speed
color_cycle_speed = 200ms  # How fast colors change
```

### 💡 Tips
- Sync color changes dengan beat music (if applicable)
- Add sparkle effect untuk extra flair
- Consider accessibility (some users color blind)

### 🌈 Advanced: Color Cycling

```python
def _animate_rainbow(widget, duration):
    # Cycle through HSV hue values
    current_hue = 0
    timer = QTimer()

    def update_color():
        nonlocal current_hue
        current_hue = (current_hue + 5) % 360
        widget.bubble_color = QColor.fromHsv(current_hue, 255, 255)
        widget.update()

    timer.timeout.connect(update_color)
    timer.start(50)  # Update every 50ms
```

---

## 9. Shake Vibrate

### 📝 Deskripsi
Shake dan vibrate effect. Bubble bergetar di tempat sebelum fade out.

### ✨ Karakteristik
- **Durasi**: Customizable (default 2000ms)
- **Intensity**: Adjustable shake strength
- **Frequency**: High (multiple shakes per second)
- **Direction**: Random multidirectional
- **Impact Level**: High (energetic)

### 🎯 Use Case Terbaik
- Excitement/hype events
- Surprise reveals
- Shock reactions
- High energy moments
- Emergency/alert notifications

### ⚙️ Customization

```python
# Shake parameters
shake_intensity = 10  # Pixel offset range
shake_count = 10  # Number of shakes
shake_duration = duration // shake_count

# Intensity levels
gentle_shake: intensity = 5px
normal_shake: intensity = 10px (default)
intense_shake: intensity = 20px
earthquake: intensity = 50px

# Pattern options
random_shake: random direction each time
horizontal_shake: only left-right
vertical_shake: only up-down
circular_shake: circular motion
```

### 💡 Tips
- Add camera shake effect untuk full screen impact
- Combine dengan sound effect (rumble, impact)
- Use sparingly to avoid annoying users
- Good for alert/alarm type notifications

---

## 10. Spiral In

### 📝 Deskripsi
Spiral in from corner dengan smooth path animation. Bubble bergerak dalam spiral path menuju position.

### ✨ Karakteristik
- **Durasi**: Customizable (default 2500ms)
- **Path**: Spiral/curved
- **Origin**: Corner of screen
- **Easing**: InOutCubic (smooth)
- **Impact Level**: Medium-High (elegant)

### 🎯 Use Case Terbaik
- VIP user entrance
- Special guest arrival
- Premium content reveal
- Elegant transitions
- Portal/teleport effects

### ⚙️ Customization

```python
# Spiral parameters
spiral_turns = 2  # Number of rotations
spiral_radius_start = 200  # Starting radius
spiral_radius_end = 0  # Ending radius (at center)

# Origin corners
top_left: (0, 0)
top_right: (width, 0)
bottom_left: (0, height)
bottom_right: (width, height)

# Path calculations
for t in range(0, duration, step):
    progress = t / duration
    angle = progress * spiral_turns * 360
    radius = lerp(spiral_radius_start, spiral_radius_end, progress)

    x = center_x + radius * cos(angle)
    y = center_y + radius * sin(angle)
```

### 💡 Tips
- Slower spiral (4s+) lebih dramatic
- Add trail effect untuk motion blur
- Combine dengan glow effect
- Good for "summoning" or "materializing" effect

### 🌀 Advanced: Custom Paths

```python
# Future: Bezier curve paths
def _create_spiral_path(start, end, turns):
    path = QPainterPath()
    path.moveTo(start)

    # Calculate spiral points
    points = calculate_spiral_points(start, end, turns)

    # Create smooth curve through points
    for point in points:
        path.lineTo(point)

    return path
```

---

## 🎨 Efek Kombinasi (Mix & Match)

Anda bisa combine multiple effects untuk hasil yang lebih kompleks:

### Example Combinations

#### 1. **Super Gift Combo**
```python
# Sparkle Zoom + Firework + Screen Flash
- Start: Sparkle zoom in
- Peak: Firework explosion
- End: Screen flash white
```

#### 2. **VIP Entrance**
```python
# Spiral In + Heart Pulse + Glow
- Entry: Spiral in from corner
- Arrival: Heart pulse effect
- Ambient: Continuous glow
```

#### 3. **Mega Celebration**
```python
# Rainbow + Shake + Particles
- Background: Rainbow colors
- Movement: Shake vibrate
- Effects: Continuous particles
```

---

## ⚡ Performance Considerations

### Optimization Tips

1. **Limit Concurrent Bubbles**
```python
MAX_BUBBLES = 10  # Limit active bubbles
if len(active_bubbles) >= MAX_BUBBLES:
    oldest_bubble.deleteLater()
```

2. **Use Appropriate Durations**
```python
# Fast events (likes): 1-2s
# Normal events (comments): 2-3s
# Special events (gifts): 3-5s
```

3. **Throttle High-Frequency Events**
```python
# Only show every Nth like
if like_count % 10 == 0:
    show_bubble()
```

4. **Disable Particles on Low-End Systems**
```python
if low_performance_mode:
    use_simple_effects = True
```

---

## 🎯 Event Matching Guide

| Event Type | Primary Effect | Alternative 1 | Alternative 2 |
|-----------|---------------|---------------|---------------|
| Join | fade_in_out | quick_pop | slide_bounce |
| Gift | sparkle_zoom | firework | rainbow |
| Comment | slide_bounce | quick_pop | fade_in_out |
| Share | float_away | spiral | rainbow |
| Follow | heart_pulse | sparkle_zoom | rainbow |
| Like | quick_pop | fade_in_out | - |
| Super Gift | firework | sparkle_zoom | rainbow |
| VIP Join | spiral | sparkle_zoom | heart_pulse |

---

## 📊 Effect Comparison Matrix

| Effect | Duration | Impact | Complexity | CPU Usage | Best For |
|--------|----------|--------|------------|-----------|----------|
| Fade In Out | Short | Low | Simple | Low | Background |
| Sparkle Zoom | Medium | Very High | Medium | Medium | Gifts |
| Slide Bounce | Medium | High | Medium | Low | Comments |
| Float Away | Medium | Medium | Simple | Low | Shares |
| Heart Pulse | Medium | High | Medium | Low | Follows |
| Quick Pop | Short | Medium | Simple | Low | Likes |
| Firework | Medium | Very High | High | High | Special |
| Rainbow | Medium | High | Medium | Medium | Fun |
| Shake | Medium | High | Medium | Medium | Hype |
| Spiral | Long | High | High | Medium | VIP |

---

## 🔧 Custom Effect Template

Untuk membuat efek custom Anda sendiri:

```python
@staticmethod
def my_custom_effect(widget, duration=3000):
    """
    My Custom Effect Description

    Args:
        widget: The bubble widget to animate
        duration: Animation duration in milliseconds
    """
    # Setup opacity effect
    opacity_effect = QGraphicsOpacityEffect(widget)
    widget.setGraphicsEffect(opacity_effect)

    # Create animation group
    anim_group = QParallelAnimationGroup(widget)

    # Add your animations here
    # Example: Opacity animation
    opacity_anim = QPropertyAnimation(opacity_effect, b"opacity")
    opacity_anim.setDuration(duration)
    opacity_anim.setStartValue(0)
    opacity_anim.setEndValue(1)

    # Example: Position animation
    pos_anim = QPropertyAnimation(widget, b"pos")
    pos_anim.setDuration(duration)
    # Set start/end positions...

    # Add to group
    anim_group.addAnimation(opacity_anim)
    anim_group.addAnimation(pos_anim)

    # Cleanup when done
    anim_group.finished.connect(widget.deleteLater)
    anim_group.start()

    return anim_group
```

---

## 📚 Additional Resources

- [Qt Animation Framework](https://doc.qt.io/qt-6/animation-overview.html)
- [Easing Curves Reference](https://doc.qt.io/qt-6/qeasingcurve.html)
- [PyQt6 Documentation](https://www.riverbankcomputing.com/static/Docs/PyQt6/)

---

**Happy Animating! 🎉**
