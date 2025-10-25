"""
Bubble Widget Component
Displays animated bubble with user avatar, name, and event info
"""

from PyQt6.QtWidgets import QWidget, QLabel
from PyQt6.QtCore import Qt, QRect, QTimer, QUrl, QPointF
from PyQt6.QtGui import (QPainter, QPixmap, QPainterPath, QColor,
                        QFont, QLinearGradient, QRadialGradient, QPen)
from PyQt6.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply
import config
from effects import EFFECT_REGISTRY
import random


class BubbleWidget(QWidget):
    """
    Animated bubble widget that displays user info and event details
    """

    def __init__(self, parent=None, event_data=None):
        super().__init__(parent)

        self.event_data = event_data or {}
        self.avatar_pixmap = None
        self.network_manager = QNetworkAccessManager()

        self._setup_ui()
        self._load_avatar()

    def _setup_ui(self):
        """Setup the bubble UI"""
        # Get event configuration
        event_type = self.event_data.get('type', 'join')
        event_config = config.EVENT_CONFIGS.get(event_type, config.EVENT_CONFIGS['join'])

        # Check for gift tier overrides (takes precedence over default config)
        if 'tier_size' in self.event_data:
            # Use tier settings for gifts
            size = self.event_data['tier_size']
            color = self.event_data['tier_color']
            effect = self.event_data['tier_effect']
            duration = self.event_data['tier_duration']
            self.tier_border_width = self.event_data.get('tier_border_width', 3)
            self.tier_glow_intensity = self.event_data.get('tier_glow_intensity', 40)
        else:
            # Use default config
            size = event_config['size']
            color = event_config['color']
            effect = event_config.get('effect', 'fade_in_out')
            duration = event_config.get('duration', 3000)
            self.tier_border_width = None
            self.tier_glow_intensity = None

        # Set size and position
        parent_width = self.parent().width() if self.parent() else config.WINDOW_WIDTH
        parent_height = self.parent().height() if self.parent() else config.WINDOW_HEIGHT

        # Random position (ensure valid range)
        max_x = max(50, parent_width - size - 50)
        max_y = max(50, parent_height - size - 50)

        x = random.randint(50, max_x) if max_x > 50 else 50
        y = random.randint(50, max_y) if max_y > 50 else 50

        self.setGeometry(x, y, size, size)

        # Store configuration
        self.bubble_color = QColor(color)
        self.emoji = event_config.get('emoji', '')
        self.effect_name = effect
        self.duration = duration

        # Enable custom painting
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)

    def _load_avatar(self):
        """Load user avatar from URL"""
        # Always create placeholder first (instant display)
        self._create_placeholder_avatar()

        # Then try to load real avatar if URL exists
        avatar_url = self.event_data.get('avatar_url', '')
        if avatar_url and avatar_url.startswith('http'):
            try:
                request = QNetworkRequest(QUrl(avatar_url))
                request.setTransferTimeout(3000)  # 3 second timeout
                reply = self.network_manager.get(request)
                reply.finished.connect(lambda: self._on_avatar_loaded(reply))
            except Exception:
                # Keep placeholder if loading fails
                pass

    def _on_avatar_loaded(self, reply):
        """Handle avatar loaded from network"""
        if reply.error() == QNetworkReply.NetworkError.NoError:
            data = reply.readAll()
            pixmap = QPixmap()
            pixmap.loadFromData(data)

            if not pixmap.isNull():
                # Create circular avatar
                self.avatar_pixmap = self._create_circular_pixmap(pixmap)
                self.update()
            else:
                self._create_placeholder_avatar()
        else:
            self._create_placeholder_avatar()

        reply.deleteLater()

    def _create_placeholder_avatar(self):
        """Create placeholder avatar with initials and better design"""
        username = self.event_data.get('username', 'User')
        initial = username[0].upper() if username else 'U'

        size = 200  # Larger for better quality
        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.GlobalColor.transparent)

        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)

        # Gradient background for better look
        from PyQt6.QtCore import QPointF
        center = QPointF(size / 2, size / 2)
        gradient = QRadialGradient(center, size / 2)

        # Use username hash for consistent color per user
        username_hash = hash(username) % 10
        color_pairs = [
            ('#FF6B6B', '#C44569'),  # Red
            ('#4ECDC4', '#2C7A7B'),  # Teal
            ('#45B7D1', '#2E86AB'),  # Blue
            ('#FFA07A', '#FF6348'),  # Orange
            ('#98D8C8', '#5F9EA0'),  # Mint
            ('#A29BFE', '#6C5CE7'),  # Purple
            ('#FD79A8', '#E84393'),  # Pink
            ('#FDCB6E', '#E17055'),  # Yellow
            ('#00B894', '#00796B'),  # Green
            ('#74B9FF', '#0984E3'),  # Sky Blue
        ]

        color_light, color_dark = color_pairs[username_hash]
        gradient.setColorAt(0, QColor(color_light))
        gradient.setColorAt(1, QColor(color_dark))

        painter.setBrush(gradient)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(0, 0, size, size)

        # Add border
        painter.setPen(QPen(QColor(255, 255, 255, 150), 4))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawEllipse(2, 2, size - 4, size - 4)

        # Draw initial with shadow
        painter.setPen(QColor(0, 0, 0, 80))
        font = QFont('Arial', size // 2, QFont.Weight.Bold)
        painter.setFont(font)
        painter.drawText(2, 2, size, size, Qt.AlignmentFlag.AlignCenter, initial)

        painter.setPen(QColor('white'))
        painter.drawText(0, 0, size, size, Qt.AlignmentFlag.AlignCenter, initial)

        painter.end()

        self.avatar_pixmap = pixmap
        self.update()

    def _create_circular_pixmap(self, source_pixmap):
        """Create circular version of pixmap"""
        size = min(source_pixmap.width(), source_pixmap.height())
        scaled = source_pixmap.scaled(size, size, Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                                     Qt.TransformationMode.SmoothTransformation)

        # Create circular mask
        circular = QPixmap(size, size)
        circular.fill(Qt.GlobalColor.transparent)

        painter = QPainter(circular)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        path = QPainterPath()
        path.addEllipse(0, 0, size, size)

        painter.setClipPath(path)
        painter.drawPixmap(0, 0, scaled)
        painter.end()

        return circular

    def paintEvent(self, event):
        """Custom paint event for bubble"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Draw bubble background with gradient
        self._draw_bubble_background(painter)

        # Draw avatar
        self._draw_avatar(painter)

        # Draw username
        self._draw_username(painter)

        # Draw emoji/icon
        self._draw_emoji(painter)

        # Draw additional info (gift, comment, etc.)
        self._draw_event_info(painter)

    def _draw_bubble_background(self, painter):
        """Draw gradient bubble background"""
        rect = self.rect()
        is_gift = self.event_data.get('type') == 'gift'

        # Create radial gradient (convert QPoint to QPointF)
        center = QPointF(rect.center())
        gradient = QRadialGradient(center, rect.width() / 2)
        gradient.setColorAt(0, self.bubble_color.lighter(120))
        gradient.setColorAt(0.7, self.bubble_color)
        gradient.setColorAt(1, self.bubble_color.darker(120))

        # Draw circle
        painter.setBrush(gradient)

        # Border settings (use tier settings if available)
        if self.tier_border_width is not None:
            # Use tier-specific border
            border_width = self.tier_border_width
            painter.setPen(QPen(QColor(255, 215, 0), border_width))  # Gold
        elif is_gift:
            # Default gift border
            painter.setPen(QPen(QColor(255, 215, 0), 6))  # Gold
        else:
            # Default normal border
            painter.setPen(QPen(QColor(255, 255, 255, 100), 3))

        painter.drawEllipse(rect.adjusted(5, 5, -5, -5))

        # Glow effect (use tier settings if available)
        if self.tier_glow_intensity is not None:
            # Use tier-specific glow
            glow_alpha = self.tier_glow_intensity
            glow_radius = rect.width() / 2 + (self.tier_glow_intensity // 5)
        elif is_gift:
            # Default gift glow
            glow_alpha = 80
            glow_radius = rect.width() / 2 + 20
        else:
            # Default normal glow
            glow_alpha = 50
            glow_radius = rect.width() / 2 + 10

        glow_gradient = QRadialGradient(center, glow_radius)
        glow_color = self.bubble_color
        glow_color.setAlpha(glow_alpha)
        glow_gradient.setColorAt(0, Qt.GlobalColor.transparent)
        glow_gradient.setColorAt(0.7, Qt.GlobalColor.transparent)
        glow_gradient.setColorAt(1, glow_color)

        painter.setBrush(glow_gradient)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(rect)

    def _draw_avatar(self, painter):
        """Draw user avatar"""
        if self.avatar_pixmap:
            is_gift = self.event_data.get('type') == 'gift'

            # Calculate avatar size (LARGER for gifts!)
            if is_gift:
                avatar_size = int(self.width() * 0.55)  # 55% of bubble
                y = int(self.height() * 0.12)  # Slightly higher
            else:
                avatar_size = int(self.width() * 0.4)  # 40% for others
                y = int(self.height() * 0.15)

            x = (self.width() - avatar_size) // 2

            # Scale avatar
            scaled_avatar = self.avatar_pixmap.scaled(
                avatar_size, avatar_size,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )

            # Draw with border (thicker for gifts)
            if is_gift:
                # Double border for gift
                painter.setPen(QPen(QColor(255, 215, 0), 4))  # Gold outer
                painter.setBrush(Qt.BrushStyle.NoBrush)
                painter.drawEllipse(x - 4, y - 4, avatar_size + 8, avatar_size + 8)

                painter.setPen(QPen(QColor(255, 255, 255), 3))  # White inner
                painter.drawEllipse(x - 1, y - 1, avatar_size + 2, avatar_size + 2)
            else:
                painter.setPen(QPen(QColor(255, 255, 255), 2))
                painter.setBrush(Qt.BrushStyle.NoBrush)
                painter.drawEllipse(x - 2, y - 2, avatar_size + 4, avatar_size + 4)

            painter.drawPixmap(x, y, scaled_avatar)

    def _draw_username(self, painter):
        """Draw username text"""
        username = self.event_data.get('username', 'Unknown')
        is_gift = self.event_data.get('type') == 'gift'

        # Setup font (larger for gifts)
        if is_gift:
            font_size = max(12, self.width() // 10)
            text_y = int(self.height() * 0.68)
        else:
            font_size = max(8, self.width() // 12)
            text_y = int(self.height() * 0.65)

        font = QFont('Arial', font_size, QFont.Weight.Bold)
        painter.setFont(font)

        # Draw text with shadow
        painter.setPen(QColor(0, 0, 0, 100))
        painter.drawText(1, text_y + 1, self.width(), 25,
                        Qt.AlignmentFlag.AlignCenter, username)

        painter.setPen(QColor(255, 255, 255))
        painter.drawText(0, text_y, self.width(), 25,
                        Qt.AlignmentFlag.AlignCenter, username)

    def _draw_emoji(self, painter):
        """Draw emoji icon"""
        if self.emoji:
            is_gift = self.event_data.get('type') == 'gift'

            # Larger emoji for gifts
            if is_gift:
                font_size = max(24, self.width() // 5)  # Bigger!
                emoji_y = int(self.height() * 0.82)
            else:
                font_size = max(16, self.width() // 6)
                emoji_y = int(self.height() * 0.78)

            font = QFont('Segoe UI Emoji', font_size)
            painter.setFont(font)

            painter.drawText(0, emoji_y, self.width(), 40,
                           Qt.AlignmentFlag.AlignCenter, self.emoji)

    def _draw_event_info(self, painter):
        """Draw additional event information"""
        event_type = self.event_data.get('type', '')

        info_text = ''
        if event_type == 'gift':
            gift_name = self.event_data.get('gift_name', 'Gift')
            info_text = f"{gift_name}"
        elif event_type == 'comment':
            comment = self.event_data.get('comment', '')
            if len(comment) > 20:
                comment = comment[:20] + '...'
            info_text = comment

        if info_text:
            font = QFont('Arial', max(6, self.width() // 15))
            painter.setFont(font)
            painter.setPen(QColor(255, 255, 255, 200))

            info_y = int(self.height() * 0.90)
            painter.drawText(5, info_y, self.width() - 10, 15,
                           Qt.AlignmentFlag.AlignCenter, info_text)

    def start_animation(self):
        """Start the animation effect"""
        effect_func = EFFECT_REGISTRY.get(self.effect_name)

        if effect_func:
            effect_func(self, self.duration)
        else:
            # Fallback to fade
            EFFECT_REGISTRY['fade_in_out'](self, self.duration)

    def showEvent(self, event):
        """Override show event to auto-start animation"""
        super().showEvent(event)
        # Start animation after a brief delay to ensure rendering
        QTimer.singleShot(50, self.start_animation)
