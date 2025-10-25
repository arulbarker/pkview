"""
Draggable, Rotatable, Resizable Label Widget
Can be used for score, points, and other text displays
"""

from PyQt6.QtWidgets import QLabel, QWidget
from PyQt6.QtCore import Qt, QPoint, QRect, QSize
from PyQt6.QtGui import QPainter, QTransform, QPen, QColor, QFont
import math


class DraggableLabel(QLabel):
    """
    Label that can be:
    - Dragged to move
    - Resized by dragging corners/edges
    - Rotated with mouse wheel
    """

    def __init__(self, parent=None, text="Label", font_size=24, text_color=None, bg_color=None, border_color=None):
        super().__init__(parent)

        self.setText(text)

        # Custom colors
        self.custom_text_color = QColor(text_color) if text_color else QColor(255, 255, 255)
        self.custom_bg_color = QColor(bg_color) if bg_color else QColor(0, 0, 0, 150)
        self.custom_border_color = QColor(border_color) if border_color else QColor(255, 255, 255, 80)

        # Set font size
        font = QFont('Arial', font_size, QFont.Weight.Bold)
        self.setFont(font)

        # State
        self.dragging = False
        self.resizing = False
        self.resize_corner = None
        self.drag_start_pos = QPoint()
        self.rotation_angle = 0  # Degrees

        # Settings
        self.min_width = 100
        self.max_width = 800
        self.min_height = 40
        self.max_height = 200

        # Enable mouse tracking
        self.setMouseTracking(True)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

    def wheelEvent(self, event):
        """Rotate with mouse wheel"""
        if event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            # Ctrl + Wheel = Rotate
            delta = event.angleDelta().y()
            self.rotation_angle += delta / 8  # 1 degree per wheel step
            self.rotation_angle = self.rotation_angle % 360  # Keep in 0-360 range

            # Apply rotation using QTransform
            from PyQt6.QtGui import QTransform
            transform = QTransform()
            transform.rotate(self.rotation_angle)
            # Note: setTransform() may not work on QLabel, so we use update()
            self.update()
        else:
            super().wheelEvent(event)

    def mousePressEvent(self, event):
        """Handle mouse press for drag/resize"""
        if event.button() == Qt.MouseButton.LeftButton:
            corner = self._get_corner_at_pos(event.pos())

            if corner:
                # Start resizing
                self.resizing = True
                self.resize_corner = corner
                self.drag_start_pos = event.pos()
            else:
                # Start dragging
                self.dragging = True
                self.drag_start_pos = event.globalPosition().toPoint() - self.pos()

    def mouseMoveEvent(self, event):
        """Handle mouse move for drag/resize"""
        if self.resizing:
            self._handle_resize(event.pos())
        elif self.dragging:
            # Move widget
            new_pos = event.globalPosition().toPoint() - self.drag_start_pos
            self.move(new_pos)
        else:
            # Update cursor based on position
            corner = self._get_corner_at_pos(event.pos())
            if corner:
                self.setCursor(Qt.CursorShape.SizeFDiagCursor)
            else:
                self.setCursor(Qt.CursorShape.SizeAllCursor)

    def mouseReleaseEvent(self, event):
        """Handle mouse release"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = False
            self.resizing = False
            self.resize_corner = None
            self.setCursor(Qt.CursorShape.ArrowCursor)

    def _get_corner_at_pos(self, pos):
        """Check if position is near a corner for resizing"""
        corner_size = 20
        w = self.width()
        h = self.height()

        # Check corners
        corners = {
            'top_left': QRect(0, 0, corner_size, corner_size),
            'top_right': QRect(w - corner_size, 0, corner_size, corner_size),
            'bottom_left': QRect(0, h - corner_size, corner_size, corner_size),
            'bottom_right': QRect(w - corner_size, h - corner_size, corner_size, corner_size),
        }

        for corner_name, rect in corners.items():
            if rect.contains(pos):
                return corner_name

        return None

    def _handle_resize(self, pos):
        """Handle resizing from corner"""
        if not self.resize_corner:
            return

        delta = pos - self.drag_start_pos
        new_width = self.width()
        new_height = self.height()
        new_x = self.x()
        new_y = self.y()

        if 'right' in self.resize_corner:
            new_width = max(self.min_width, min(self.max_width, self.width() + delta.x()))
        elif 'left' in self.resize_corner:
            new_width = max(self.min_width, min(self.max_width, self.width() - delta.x()))
            new_x = self.x() + delta.x()

        if 'bottom' in self.resize_corner:
            new_height = max(self.min_height, min(self.max_height, self.height() + delta.y()))
        elif 'top' in self.resize_corner:
            new_height = max(self.min_height, min(self.max_height, self.height() - delta.y()))
            new_y = self.y() + delta.y()

        self.setGeometry(new_x, new_y, new_width, new_height)
        self.drag_start_pos = pos

    def paintEvent(self, event):
        """Custom paint with rotation support - MANUAL PAINTING"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.TextAntialiasing)

        # Apply rotation if needed
        if self.rotation_angle != 0:
            # Save original state
            painter.save()

            # Rotate around center
            center = self.rect().center()
            painter.translate(center.x(), center.y())
            painter.rotate(self.rotation_angle)
            painter.translate(-center.x(), -center.y())

        # Manual painting (don't call super!)
        rect = self.rect()

        # Draw background
        painter.setBrush(self.custom_bg_color)
        painter.setPen(QPen(self.custom_border_color, 2))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), 10, 10)

        # Draw text
        painter.setPen(self.custom_text_color)
        font = self.font()
        painter.setFont(font)
        painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, self.text())

        # Draw resize handles at corners (only when not rotating)
        if abs(self.rotation_angle) < 5:
            painter.setPen(QPen(QColor(255, 255, 255, 100), 1))
            painter.setBrush(QColor(255, 255, 255, 50))
            corner_size = 8
            w = rect.width()
            h = rect.height()

            # Draw small circles at corners
            corners = [
                (0, 0), (w - corner_size, 0),
                (0, h - corner_size), (w - corner_size, h - corner_size)
            ]

            for x, y in corners:
                painter.drawEllipse(x, y, corner_size, corner_size)

        # Restore if rotated
        if self.rotation_angle != 0:
            painter.restore()

    def get_state(self):
        """Get current state for saving"""
        return {
            'x': self.x(),
            'y': self.y(),
            'width': self.width(),
            'height': self.height(),
            'rotation': self.rotation_angle,
            'text': self.text()
        }

    def set_state(self, state):
        """Restore state from saved data"""
        self.setGeometry(state['x'], state['y'], state['width'], state['height'])
        self.rotation_angle = state.get('rotation', 0)
        if 'text' in state:
            self.setText(state['text'])
        self.update()


class DraggableMultiLineLabel(QWidget):
    """
    Multi-line label that can be dragged, resized, and rotated
    Used for points display with multiple lines
    """

    def __init__(self, parent=None, lines=None):
        super().__init__(parent)

        self.lines = lines or ["Line 1", "Line 2"]
        self.font_size = 18

        # State
        self.dragging = False
        self.resizing = False
        self.resize_corner = None
        self.drag_start_pos = QPoint()
        self.rotation_angle = 0

        # Settings
        self.min_width = 100
        self.max_width = 400
        self.min_height = 60
        self.max_height = 300

        self.setMinimumSize(150, 80)
        self.setMouseTracking(True)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        # Style
        self.bg_color = QColor(0, 0, 0, 150)
        self.text_color = QColor(255, 255, 255)
        self.border_color = QColor(255, 255, 255, 80)

    def set_lines(self, lines):
        """Update lines of text"""
        self.lines = lines
        self.update()

    def wheelEvent(self, event):
        """Rotate with mouse wheel"""
        if event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            delta = event.angleDelta().y()
            self.rotation_angle += delta / 8
            self.rotation_angle = self.rotation_angle % 360
            self.update()
        else:
            super().wheelEvent(event)

    def mousePressEvent(self, event):
        """Handle mouse press"""
        if event.button() == Qt.MouseButton.LeftButton:
            corner = self._get_corner_at_pos(event.pos())

            if corner:
                self.resizing = True
                self.resize_corner = corner
                self.drag_start_pos = event.pos()
            else:
                self.dragging = True
                self.drag_start_pos = event.globalPosition().toPoint() - self.pos()

    def mouseMoveEvent(self, event):
        """Handle mouse move"""
        if self.resizing:
            self._handle_resize(event.pos())
        elif self.dragging:
            new_pos = event.globalPosition().toPoint() - self.drag_start_pos
            self.move(new_pos)
        else:
            corner = self._get_corner_at_pos(event.pos())
            if corner:
                self.setCursor(Qt.CursorShape.SizeFDiagCursor)
            else:
                self.setCursor(Qt.CursorShape.SizeAllCursor)

    def mouseReleaseEvent(self, event):
        """Handle mouse release"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = False
            self.resizing = False
            self.resize_corner = None
            self.setCursor(Qt.CursorShape.ArrowCursor)

    def _get_corner_at_pos(self, pos):
        """Check if near corner"""
        corner_size = 20
        w = self.width()
        h = self.height()

        corners = {
            'top_left': QRect(0, 0, corner_size, corner_size),
            'top_right': QRect(w - corner_size, 0, corner_size, corner_size),
            'bottom_left': QRect(0, h - corner_size, corner_size, corner_size),
            'bottom_right': QRect(w - corner_size, h - corner_size, corner_size, corner_size),
        }

        for corner_name, rect in corners.items():
            if rect.contains(pos):
                return corner_name

        return None

    def _handle_resize(self, pos):
        """Handle resizing"""
        if not self.resize_corner:
            return

        delta = pos - self.drag_start_pos
        new_width = self.width()
        new_height = self.height()
        new_x = self.x()
        new_y = self.y()

        if 'right' in self.resize_corner:
            new_width = max(self.min_width, min(self.max_width, self.width() + delta.x()))
        elif 'left' in self.resize_corner:
            new_width = max(self.min_width, min(self.max_width, self.width() - delta.x()))
            new_x = self.x() + delta.x()

        if 'bottom' in self.resize_corner:
            new_height = max(self.min_height, min(self.max_height, self.height() + delta.y()))
        elif 'top' in self.resize_corner:
            new_height = max(self.min_height, min(self.max_height, self.height() - delta.y()))
            new_y = self.y() + delta.y()

        self.setGeometry(new_x, new_y, new_width, new_height)
        self.drag_start_pos = pos

    def paintEvent(self, event):
        """Paint the multi-line label"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Apply rotation
        if self.rotation_angle != 0:
            center = self.rect().center()
            painter.translate(center)
            painter.rotate(self.rotation_angle)
            painter.translate(-center)

        # Draw background
        painter.setBrush(self.bg_color)
        painter.setPen(QPen(self.border_color, 2))
        painter.drawRoundedRect(self.rect().adjusted(2, 2, -2, -2), 10, 10)

        # Draw text lines
        font = QFont('Arial', self.font_size, QFont.Weight.Bold)
        painter.setFont(font)
        painter.setPen(self.text_color)

        line_height = self.height() // max(len(self.lines), 1)
        for i, line in enumerate(self.lines):
            y = (i + 0.5) * line_height + 5
            painter.drawText(QRect(10, int(y), self.width() - 20, line_height),
                           Qt.AlignmentFlag.AlignCenter, line)

        # Draw resize handles
        if abs(self.rotation_angle) < 5 or abs(self.rotation_angle - 360) < 5:
            painter.setPen(QPen(QColor(255, 255, 255, 150), 2))
            corner_size = 10
            w = self.width()
            h = self.height()

            corners = [
                (0, 0), (w - corner_size, 0),
                (0, h - corner_size), (w - corner_size, h - corner_size)
            ]

            for x, y in corners:
                painter.drawRect(x, y, corner_size, corner_size)

    def get_state(self):
        """Get state for saving"""
        return {
            'x': self.x(),
            'y': self.y(),
            'width': self.width(),
            'height': self.height(),
            'rotation': self.rotation_angle,
            'font_size': self.font_size
        }

    def set_state(self, state):
        """Restore state"""
        self.setGeometry(state['x'], state['y'], state['width'], state['height'])
        self.rotation_angle = state.get('rotation', 0)
        self.font_size = state.get('font_size', 18)
        self.update()
