"""
Persistent Bubble System
Bubbles that stay on screen until users leave
"""

from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt, QTimer, QRect, pyqtSignal
from bubble_widget import BubbleWidget
import random


class PersistentBubble(BubbleWidget):
    """
    Bubble that doesn't auto-delete
    Stays on screen until explicitly removed
    """

    # Signal when user wants to remove this bubble
    remove_requested = pyqtSignal(str)  # user_id

    def __init__(self, parent=None, event_data=None):
        super().__init__(parent, event_data)
        self.user_id = event_data.get('user_id', '')
        self.is_persistent = True

    def start_animation(self):
        """Override to NOT auto-delete"""
        # Use gentle fade-in effect instead
        from effects import BubbleEffects
        from PyQt6.QtWidgets import QGraphicsOpacityEffect
        from PyQt6.QtCore import QPropertyAnimation

        opacity_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(opacity_effect)

        # Simple fade in (no auto-delete!)
        fade_in = QPropertyAnimation(opacity_effect, b"opacity")
        fade_in.setDuration(500)
        fade_in.setStartValue(0)
        fade_in.setEndValue(1)
        fade_in.start()

        # Store animation to prevent garbage collection
        self._fade_anim = fade_in

    def remove_with_animation(self):
        """Remove this bubble with fade out"""
        from PyQt6.QtWidgets import QGraphicsOpacityEffect
        from PyQt6.QtCore import QPropertyAnimation

        opacity_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(opacity_effect)

        fade_out = QPropertyAnimation(opacity_effect, b"opacity")
        fade_out.setDuration(500)
        fade_out.setStartValue(1)
        fade_out.setEndValue(0)
        fade_out.finished.connect(self.deleteLater)
        fade_out.start()

        # Store to prevent GC
        self._fade_out_anim = fade_out


class PersistentViewerManager:
    """
    Manages persistent viewer bubbles
    Keeps track of who's watching and their bubbles
    """

    def __init__(self, parent_container):
        self.container = parent_container
        self.active_viewers = {}  # {user_id: bubble_widget}
        self.max_viewers = 20  # Max bubbles on screen

        # Grid layout parameters
        self.columns = 5
        self.bubble_size = 100  # Smaller for persistent view
        self.spacing = 10

    def add_viewer(self, event_data):
        """Add or update a viewer"""
        user_id = event_data.get('user_id', '')

        if not user_id:
            return

        # If already exists, just update (pulse effect maybe)
        if user_id in self.active_viewers:
            self._pulse_existing(user_id)
            return

        # Check max limit
        if len(self.active_viewers) >= self.max_viewers:
            # Remove oldest viewer
            oldest_id = list(self.active_viewers.keys())[0]
            self.remove_viewer(oldest_id)

        # Create persistent bubble
        bubble_data = event_data.copy()
        bubble = PersistentBubble(self.container, bubble_data)

        # Calculate position in grid
        index = len(self.active_viewers)
        row = index // self.columns
        col = index % self.columns

        x = 10 + col * (self.bubble_size + self.spacing)
        y = 10 + row * (self.bubble_size + self.spacing)

        bubble.setGeometry(x, y, self.bubble_size, self.bubble_size)
        bubble.show()
        bubble.start_animation()

        # Track viewer
        self.active_viewers[user_id] = bubble

    def remove_viewer(self, user_id):
        """Remove a viewer (they left)"""
        if user_id in self.active_viewers:
            bubble = self.active_viewers[user_id]
            bubble.remove_with_animation()
            del self.active_viewers[user_id]

            # Reorganize remaining bubbles
            self._reorganize_bubbles()

    def _pulse_existing(self, user_id):
        """Pulse effect for existing viewer (they did something)"""
        if user_id in self.active_viewers:
            bubble = self.active_viewers[user_id]

            from PyQt6.QtCore import QPropertyAnimation, QSequentialAnimationGroup

            # Quick pulse effect
            anim_group = QSequentialAnimationGroup(bubble)

            # Grow
            grow = QPropertyAnimation(bubble, b"geometry")
            grow.setDuration(150)
            rect = bubble.geometry()
            big_rect = QRect(
                rect.x() - 5,
                rect.y() - 5,
                rect.width() + 10,
                rect.height() + 10
            )
            grow.setStartValue(rect)
            grow.setEndValue(big_rect)

            # Shrink back
            shrink = QPropertyAnimation(bubble, b"geometry")
            shrink.setDuration(150)
            shrink.setStartValue(big_rect)
            shrink.setEndValue(rect)

            anim_group.addAnimation(grow)
            anim_group.addAnimation(shrink)
            anim_group.start()

            # Store to prevent GC
            bubble._pulse_anim = anim_group

    def _reorganize_bubbles(self):
        """Reorganize bubbles after removal"""
        for index, (user_id, bubble) in enumerate(self.active_viewers.items()):
            row = index // self.columns
            col = index % self.columns

            x = 10 + col * (self.bubble_size + self.spacing)
            y = 10 + row * (self.bubble_size + self.spacing)

            # Animate to new position
            from PyQt6.QtCore import QPropertyAnimation

            move_anim = QPropertyAnimation(bubble, b"geometry")
            move_anim.setDuration(300)
            move_anim.setStartValue(bubble.geometry())
            move_anim.setEndValue(QRect(x, y, self.bubble_size, self.bubble_size))
            move_anim.start()

            # Store to prevent GC
            bubble._move_anim = move_anim

    def clear_all(self):
        """Clear all viewers"""
        for user_id in list(self.active_viewers.keys()):
            self.remove_viewer(user_id)

    def get_viewer_count(self):
        """Get current viewer count"""
        return len(self.active_viewers)
