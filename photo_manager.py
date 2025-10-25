"""
Photo Manager - Draggable and Resizable Photo Widgets
Handles Team A and Team B photo display with full customization
"""

from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QFileDialog
from PyQt6.QtCore import Qt, QRect, QPoint, pyqtSignal
from PyQt6.QtGui import QPixmap, QPainter, QPainterPath, QColor, QPen, QCursor
import os


class DraggablePhoto(QWidget):
    """
    Draggable and resizable photo widget with circular crop
    """

    position_changed = pyqtSignal(QPoint, int)  # position, size

    def __init__(self, parent=None, team='A', default_size=300):
        super().__init__(parent)

        self.team = team
        self.photo_pixmap = None
        self.default_size = default_size
        self.current_size = default_size

        # Drag state
        self.is_dragging = False
        self.drag_start_pos = None

        # Resize state
        self.is_resizing = False
        self.resize_start_pos = None
        self.resize_start_size = None

        # Rotation state
        self.rotation_angle = 0  # Degrees

        # Setup UI
        self.setFixedSize(self.current_size, self.current_size)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setMouseTracking(True)

        # Create placeholder
        self._create_placeholder()

    def _create_placeholder(self):
        """Create placeholder image when no photo loaded"""
        size = self.current_size
        self.photo_pixmap = QPixmap(size, size)
        self.photo_pixmap.fill(Qt.GlobalColor.transparent)

        painter = QPainter(self.photo_pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Draw circle background
        color = QColor('#FF6B6B') if self.team == 'A' else QColor('#4ECDC4')
        painter.setBrush(color)
        painter.setPen(QPen(QColor(255, 255, 255), 4))
        painter.drawEllipse(4, 4, size - 8, size - 8)

        # Draw text
        painter.setPen(QColor(255, 255, 255))
        font = painter.font()
        font.setPointSize(32)
        font.setBold(True)
        painter.setFont(font)
        text = f"TEAM {self.team}"
        painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, text)

        painter.end()
        self.update()

    def load_photo(self, file_path):
        """
        Load photo from file path

        Args:
            file_path: Path to image file
        """
        if not os.path.exists(file_path):
            return False

        pixmap = QPixmap(file_path)
        if pixmap.isNull():
            return False

        # Create circular crop
        self.photo_pixmap = self._create_circular_pixmap(pixmap, self.current_size)
        self.update()
        return True

    def _create_circular_pixmap(self, pixmap, size):
        """
        Create circular cropped version of pixmap

        Args:
            pixmap: Source pixmap
            size: Output size

        Returns:
            QPixmap: Circular cropped pixmap
        """
        # Scale to size while maintaining aspect ratio
        scaled = pixmap.scaled(
            size, size,
            Qt.AspectRatioMode.KeepAspectRatioByExpanding,
            Qt.TransformationMode.SmoothTransformation
        )

        # Create circular mask
        output = QPixmap(size, size)
        output.fill(Qt.GlobalColor.transparent)

        painter = QPainter(output)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Create circular path
        path = QPainterPath()
        path.addEllipse(0, 0, size, size)
        painter.setClipPath(path)

        # Draw image centered
        x = (size - scaled.width()) // 2
        y = (size - scaled.height()) // 2
        painter.drawPixmap(x, y, scaled)

        # Draw border
        painter.setClipping(False)
        color = QColor('#FF6B6B') if self.team == 'A' else QColor('#4ECDC4')
        painter.setPen(QPen(color, 6))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawEllipse(3, 3, size - 6, size - 6)

        painter.end()
        return output

    def resize_photo(self, new_size):
        """
        Resize photo to new size

        Args:
            new_size: New size (width = height for circle)
        """
        if new_size < 100 or new_size > 600:
            return  # Limit size

        self.current_size = new_size
        self.setFixedSize(new_size, new_size)

        # Reload photo with new size
        if self.photo_pixmap:
            # We need to reload from original, but for now just recreate placeholder
            self._create_placeholder()

        self.position_changed.emit(self.pos(), self.current_size)

    def wheelEvent(self, event):
        """Handle mouse wheel for rotation"""
        if event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            # Ctrl + Wheel = Rotate
            delta = event.angleDelta().y()
            self.rotation_angle += delta / 8  # 1 degree per wheel step
            self.rotation_angle = self.rotation_angle % 360  # Keep in 0-360 range
            self.update()
        else:
            super().wheelEvent(event)

    def paintEvent(self, event):
        """Custom paint event with rotation - FIXED"""
        if self.photo_pixmap:
            painter = QPainter(self)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)

            # Apply rotation if needed
            if self.rotation_angle != 0:
                # Save state
                painter.save()

                # Rotate around center
                center = self.rect().center()
                painter.translate(center.x(), center.y())
                painter.rotate(self.rotation_angle)
                painter.translate(-center.x(), -center.y())

                # Draw pixmap
                painter.drawPixmap(0, 0, self.photo_pixmap)

                # Restore state
                painter.restore()
            else:
                # No rotation - just draw
                painter.drawPixmap(0, 0, self.photo_pixmap)

    def mousePressEvent(self, event):
        """Handle mouse press for drag/resize"""
        if event.button() == Qt.MouseButton.LeftButton:
            # Check if clicking on edge (resize zone)
            edge_threshold = 20
            pos = event.pos()
            w = self.width()
            h = self.height()

            # Check if near corners (resize)
            near_edge = (pos.x() < edge_threshold or pos.x() > w - edge_threshold or
                        pos.y() < edge_threshold or pos.y() > h - edge_threshold)

            if near_edge:
                self.is_resizing = True
                self.resize_start_pos = event.globalPosition().toPoint()
                self.resize_start_size = self.current_size
                self.setCursor(QCursor(Qt.CursorShape.SizeFDiagCursor))
            else:
                # Start drag
                self.is_dragging = True
                self.drag_start_pos = event.globalPosition().toPoint() - self.pos()
                self.setCursor(QCursor(Qt.CursorShape.ClosedHandCursor))

    def mouseMoveEvent(self, event):
        """Handle mouse move for drag/resize"""
        if self.is_dragging:
            # Drag mode
            new_pos = event.globalPosition().toPoint() - self.drag_start_pos
            self.move(new_pos)
            self.position_changed.emit(new_pos, self.current_size)

        elif self.is_resizing:
            # Resize mode
            delta = event.globalPosition().toPoint() - self.resize_start_pos
            new_size = max(100, min(600, self.resize_start_size + delta.x()))
            self.resize_photo(new_size)

        else:
            # Check if hovering near edge
            edge_threshold = 20
            pos = event.pos()
            w = self.width()
            h = self.height()

            near_edge = (pos.x() < edge_threshold or pos.x() > w - edge_threshold or
                        pos.y() < edge_threshold or pos.y() > h - edge_threshold)

            if near_edge:
                self.setCursor(QCursor(Qt.CursorShape.SizeFDiagCursor))
            else:
                self.setCursor(QCursor(Qt.CursorShape.OpenHandCursor))

    def mouseReleaseEvent(self, event):
        """Handle mouse release"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.is_dragging = False
            self.is_resizing = False
            self.setCursor(QCursor(Qt.CursorShape.ArrowCursor))


class PhotoUploadWidget(QWidget):
    """
    Photo upload UI for Team A and Team B
    """

    photo_loaded = pyqtSignal(str, str)  # team, file_path

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self):
        """Setup upload UI"""
        layout = QVBoxLayout(self)

        # Title
        title = QLabel("📸 Team Photos Setup")
        title.setStyleSheet("font-size: 16px; font-weight: bold; color: white;")
        layout.addWidget(title)

        # Team A
        layout.addWidget(QLabel("Team A Photo:"))
        self.team_a_btn = QPushButton("📁 Browse Photo for Team A")
        self.team_a_btn.clicked.connect(lambda: self._browse_photo('A'))
        self.team_a_btn.setStyleSheet("""
            QPushButton {
                background-color: #FF6B6B;
                color: white;
                padding: 10px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #FF5252;
            }
        """)
        layout.addWidget(self.team_a_btn)

        self.team_a_label = QLabel("No photo selected")
        self.team_a_label.setStyleSheet("color: #888; font-size: 11px;")
        layout.addWidget(self.team_a_label)

        layout.addWidget(QLabel(""))  # Spacer

        # Team B
        layout.addWidget(QLabel("Team B Photo:"))
        self.team_b_btn = QPushButton("📁 Browse Photo for Team B")
        self.team_b_btn.clicked.connect(lambda: self._browse_photo('B'))
        self.team_b_btn.setStyleSheet("""
            QPushButton {
                background-color: #4ECDC4;
                color: white;
                padding: 10px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #3DBDB3;
            }
        """)
        layout.addWidget(self.team_b_btn)

        self.team_b_label = QLabel("No photo selected")
        self.team_b_label.setStyleSheet("color: #888; font-size: 11px;")
        layout.addWidget(self.team_b_label)

        layout.addStretch()

    def _browse_photo(self, team):
        """
        Browse for photo file

        Args:
            team: 'A' or 'B'
        """
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            f"Select Team {team} Photo",
            "",
            "Image Files (*.png *.jpg *.jpeg *.webp *.bmp *.gif)"
        )

        if file_path:
            # Emit signal
            self.photo_loaded.emit(team, file_path)

            # Update label
            filename = os.path.basename(file_path)
            if team == 'A':
                self.team_a_label.setText(f"✓ {filename}")
                self.team_a_label.setStyleSheet("color: #4CAF50; font-size: 11px;")
            else:
                self.team_b_label.setText(f"✓ {filename}")
                self.team_b_label.setStyleSheet("color: #4CAF50; font-size: 11px;")
