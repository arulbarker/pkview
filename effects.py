"""
Advanced Animation Effects for Bubble Widgets
Contains modular animation effects that can be applied to bubbles
"""

from PyQt6.QtCore import (QPropertyAnimation, QEasingCurve, QPoint,
                          QRect, QSequentialAnimationGroup,
                          QParallelAnimationGroup, QTimer, pyqtProperty)
from PyQt6.QtGui import QColor, QPainter, QRadialGradient, QPen, QBrush
from PyQt6.QtWidgets import QGraphicsOpacityEffect
import random
import math


class BubbleEffects:
    """Collection of animation effects for bubbles"""

    @staticmethod
    def fade_in_out(widget, duration=2000):
        """Simple fade in and fade out effect"""
        opacity_effect = QGraphicsOpacityEffect(widget)
        widget.setGraphicsEffect(opacity_effect)

        anim_group = QSequentialAnimationGroup(widget)

        # Fade in
        fade_in = QPropertyAnimation(opacity_effect, b"opacity")
        fade_in.setDuration(duration // 4)
        fade_in.setStartValue(0)
        fade_in.setEndValue(1)
        fade_in.setEasingCurve(QEasingCurve.Type.InOutQuad)

        # Hold
        hold = QPropertyAnimation(opacity_effect, b"opacity")
        hold.setDuration(duration // 2)
        hold.setStartValue(1)
        hold.setEndValue(1)

        # Fade out
        fade_out = QPropertyAnimation(opacity_effect, b"opacity")
        fade_out.setDuration(duration // 4)
        fade_out.setStartValue(1)
        fade_out.setEndValue(0)
        fade_out.setEasingCurve(QEasingCurve.Type.InOutQuad)

        anim_group.addAnimation(fade_in)
        anim_group.addAnimation(hold)
        anim_group.addAnimation(fade_out)

        anim_group.finished.connect(widget.deleteLater)
        anim_group.start()

        return anim_group

    @staticmethod
    def sparkle_zoom(widget, duration=4000):
        """Zoom in with sparkle effect - DRAMATIC for gifts!"""
        opacity_effect = QGraphicsOpacityEffect(widget)
        widget.setGraphicsEffect(opacity_effect)

        # Get initial position and size
        start_rect = widget.geometry()
        center_x = start_rect.x() + start_rect.width() // 2
        center_y = start_rect.y() + start_rect.height() // 2

        # Create animation group
        anim_group = QParallelAnimationGroup(widget)

        # Opacity animation
        opacity_anim = QPropertyAnimation(opacity_effect, b"opacity")
        opacity_anim.setDuration(duration)
        opacity_anim.setKeyValueAt(0, 0)
        opacity_anim.setKeyValueAt(0.15, 1)
        opacity_anim.setKeyValueAt(0.85, 1)
        opacity_anim.setKeyValueAt(1, 0)

        # DRAMATIC Geometry animation (zoom effect)
        geom_anim = QPropertyAnimation(widget, b"geometry")
        geom_anim.setDuration(duration)

        # Start VERY TINY (10% size) - DRAMATIC!
        tiny_size = int(start_rect.width() * 0.1)  # Was 0.5, now 0.1!
        start_tiny = QRect(
            center_x - tiny_size // 2,
            center_y - tiny_size // 2,
            tiny_size, tiny_size
        )

        # Zoom to EXTRA LARGE (150% size) - HUGE!
        huge_size = int(start_rect.width() * 1.5)  # Was 1.3, now 1.5!
        huge_rect = QRect(
            center_x - huge_size // 2,
            center_y - huge_size // 2,
            huge_size, huge_size
        )

        # Animation timeline: tiny → HUGE → normal
        geom_anim.setKeyValueAt(0, start_tiny)      # Start tiny (10%)
        geom_anim.setKeyValueAt(0.4, huge_rect)     # Zoom to HUGE (150%)
        geom_anim.setKeyValueAt(0.7, huge_rect)     # Hold at HUGE
        geom_anim.setKeyValueAt(1, start_rect)      # Back to normal (100%)
        geom_anim.setEasingCurve(QEasingCurve.Type.OutElastic)  # Bouncy!

        anim_group.addAnimation(opacity_anim)
        anim_group.addAnimation(geom_anim)

        # Add sparkle particles
        BubbleEffects._add_sparkles(widget, duration)

        anim_group.finished.connect(widget.deleteLater)
        anim_group.start()

        return anim_group

    @staticmethod
    def slide_bounce(widget, duration=3000):
        """Slide from side with bounce effect - perfect for comments"""
        opacity_effect = QGraphicsOpacityEffect(widget)
        widget.setGraphicsEffect(opacity_effect)

        # Random side (left or right)
        from_left = random.choice([True, False])

        end_rect = widget.geometry()
        parent_width = widget.parent().width() if widget.parent() else 1920

        # Start position (off-screen)
        if from_left:
            start_x = -end_rect.width()
        else:
            start_x = parent_width

        start_rect = QRect(start_x, end_rect.y(), end_rect.width(), end_rect.height())
        widget.setGeometry(start_rect)

        # Animation group
        anim_group = QSequentialAnimationGroup(widget)

        # Slide in with bounce
        slide_anim = QPropertyAnimation(widget, b"geometry")
        slide_anim.setDuration(duration // 3)
        slide_anim.setStartValue(start_rect)
        slide_anim.setEndValue(end_rect)
        slide_anim.setEasingCurve(QEasingCurve.Type.OutBounce)

        # Fade in opacity
        fade_in = QPropertyAnimation(opacity_effect, b"opacity")
        fade_in.setDuration(duration // 3)
        fade_in.setStartValue(0)
        fade_in.setEndValue(1)

        # Hold
        hold = QPropertyAnimation(widget, b"geometry")
        hold.setDuration(duration // 3)
        hold.setStartValue(end_rect)
        hold.setEndValue(end_rect)

        # Fade out
        fade_out = QPropertyAnimation(opacity_effect, b"opacity")
        fade_out.setDuration(duration // 3)
        fade_out.setStartValue(1)
        fade_out.setEndValue(0)

        # Parallel group for slide + fade in
        parallel_in = QParallelAnimationGroup()
        parallel_in.addAnimation(slide_anim)
        parallel_in.addAnimation(fade_in)

        anim_group.addAnimation(parallel_in)
        anim_group.addAnimation(hold)
        anim_group.addAnimation(fade_out)

        anim_group.finished.connect(widget.deleteLater)
        anim_group.start()

        return anim_group

    @staticmethod
    def float_away(widget, duration=2500):
        """Float upward and fade away - perfect for shares"""
        opacity_effect = QGraphicsOpacityEffect(widget)
        widget.setGraphicsEffect(opacity_effect)

        start_rect = widget.geometry()
        end_rect = QRect(
            start_rect.x() + random.randint(-50, 50),
            -start_rect.height(),  # Float to top of screen
            start_rect.width(),
            start_rect.height()
        )

        anim_group = QParallelAnimationGroup(widget)

        # Float animation
        float_anim = QPropertyAnimation(widget, b"geometry")
        float_anim.setDuration(duration)
        float_anim.setStartValue(start_rect)
        float_anim.setEndValue(end_rect)
        float_anim.setEasingCurve(QEasingCurve.Type.InOutQuad)

        # Fade out
        fade_anim = QPropertyAnimation(opacity_effect, b"opacity")
        fade_anim.setDuration(duration)
        fade_anim.setStartValue(1)
        fade_anim.setEndValue(0)
        fade_anim.setEasingCurve(QEasingCurve.Type.InQuad)

        anim_group.addAnimation(float_anim)
        anim_group.addAnimation(fade_anim)

        anim_group.finished.connect(widget.deleteLater)
        anim_group.start()

        return anim_group

    @staticmethod
    def heart_pulse(widget, duration=3500):
        """Pulsing heart effect - perfect for follows"""
        opacity_effect = QGraphicsOpacityEffect(widget)
        widget.setGraphicsEffect(opacity_effect)

        start_rect = widget.geometry()
        center_x = start_rect.x() + start_rect.width() // 2
        center_y = start_rect.y() + start_rect.height() // 2

        anim_group = QSequentialAnimationGroup(widget)

        # Create pulse effect (3 pulses)
        for i in range(3):
            # Expand
            expand_anim = QPropertyAnimation(widget, b"geometry")
            expand_anim.setDuration(duration // 8)

            large_size = int(start_rect.width() * 1.2)
            large_rect = QRect(
                center_x - large_size // 2,
                center_y - large_size // 2,
                large_size, large_size
            )

            expand_anim.setStartValue(start_rect)
            expand_anim.setEndValue(large_rect)
            expand_anim.setEasingCurve(QEasingCurve.Type.OutQuad)

            # Contract
            contract_anim = QPropertyAnimation(widget, b"geometry")
            contract_anim.setDuration(duration // 8)
            contract_anim.setStartValue(large_rect)
            contract_anim.setEndValue(start_rect)
            contract_anim.setEasingCurve(QEasingCurve.Type.InQuad)

            anim_group.addAnimation(expand_anim)
            anim_group.addAnimation(contract_anim)

        # Final fade out
        fade_out = QPropertyAnimation(opacity_effect, b"opacity")
        fade_out.setDuration(duration // 4)
        fade_out.setStartValue(1)
        fade_out.setEndValue(0)

        anim_group.addAnimation(fade_out)

        anim_group.finished.connect(widget.deleteLater)
        anim_group.start()

        return anim_group

    @staticmethod
    def quick_pop(widget, duration=1500):
        """Quick pop in and out - perfect for likes"""
        opacity_effect = QGraphicsOpacityEffect(widget)
        widget.setGraphicsEffect(opacity_effect)

        start_rect = widget.geometry()
        center_x = start_rect.x() + start_rect.width() // 2
        center_y = start_rect.y() + start_rect.height() // 2

        anim_group = QParallelAnimationGroup(widget)

        # Pop scale animation
        scale_anim = QPropertyAnimation(widget, b"geometry")
        scale_anim.setDuration(duration)

        # Start tiny
        tiny_size = 10
        tiny_rect = QRect(center_x - 5, center_y - 5, tiny_size, tiny_size)

        # Pop to normal then shrink
        scale_anim.setKeyValueAt(0, tiny_rect)
        scale_anim.setKeyValueAt(0.3, start_rect)
        scale_anim.setKeyValueAt(1, tiny_rect)
        scale_anim.setEasingCurve(QEasingCurve.Type.OutBounce)

        # Opacity animation
        opacity_anim = QPropertyAnimation(opacity_effect, b"opacity")
        opacity_anim.setDuration(duration)
        opacity_anim.setKeyValueAt(0, 0)
        opacity_anim.setKeyValueAt(0.2, 1)
        opacity_anim.setKeyValueAt(0.8, 1)
        opacity_anim.setKeyValueAt(1, 0)

        anim_group.addAnimation(scale_anim)
        anim_group.addAnimation(opacity_anim)

        anim_group.finished.connect(widget.deleteLater)
        anim_group.start()

        return anim_group

    @staticmethod
    def firework_explosion(widget, duration=2000):
        """Firework explosion effect"""
        opacity_effect = QGraphicsOpacityEffect(widget)
        widget.setGraphicsEffect(opacity_effect)

        # Create particles
        BubbleEffects._create_explosion_particles(widget, duration)

        # Main bubble fade out
        fade_anim = QPropertyAnimation(opacity_effect, b"opacity")
        fade_anim.setDuration(duration)
        fade_anim.setStartValue(1)
        fade_anim.setEndValue(0)

        fade_anim.finished.connect(widget.deleteLater)
        fade_anim.start()

        return fade_anim

    @staticmethod
    def rainbow_rotate(widget, duration=3000):
        """Rainbow gradient with rotation"""
        opacity_effect = QGraphicsOpacityEffect(widget)
        widget.setGraphicsEffect(opacity_effect)

        # Rotation animation (if widget supports it)
        # Note: This would need custom property for rotation

        # Fade in and out with rotation
        fade_seq = QSequentialAnimationGroup(widget)

        fade_in = QPropertyAnimation(opacity_effect, b"opacity")
        fade_in.setDuration(duration // 3)
        fade_in.setStartValue(0)
        fade_in.setEndValue(1)

        hold = QPropertyAnimation(opacity_effect, b"opacity")
        hold.setDuration(duration // 3)
        hold.setStartValue(1)
        hold.setEndValue(1)

        fade_out = QPropertyAnimation(opacity_effect, b"opacity")
        fade_out.setDuration(duration // 3)
        fade_out.setStartValue(1)
        fade_out.setEndValue(0)

        fade_seq.addAnimation(fade_in)
        fade_seq.addAnimation(hold)
        fade_seq.addAnimation(fade_out)

        fade_seq.finished.connect(widget.deleteLater)
        fade_seq.start()

        return fade_seq

    @staticmethod
    def shake_vibrate(widget, duration=2000):
        """Shake and vibrate effect"""
        original_pos = widget.pos()
        shake_intensity = 10

        anim_group = QSequentialAnimationGroup(widget)

        # Create multiple small movements
        for i in range(10):
            shake_anim = QPropertyAnimation(widget, b"pos")
            shake_anim.setDuration(duration // 20)

            offset_x = random.randint(-shake_intensity, shake_intensity)
            offset_y = random.randint(-shake_intensity, shake_intensity)

            shake_anim.setStartValue(original_pos)
            shake_anim.setEndValue(QPoint(original_pos.x() + offset_x,
                                          original_pos.y() + offset_y))
            anim_group.addAnimation(shake_anim)

        # Return to original
        return_anim = QPropertyAnimation(widget, b"pos")
        return_anim.setDuration(duration // 20)
        return_anim.setStartValue(widget.pos())
        return_anim.setEndValue(original_pos)
        anim_group.addAnimation(return_anim)

        # Fade out
        opacity_effect = QGraphicsOpacityEffect(widget)
        widget.setGraphicsEffect(opacity_effect)

        fade_out = QPropertyAnimation(opacity_effect, b"opacity")
        fade_out.setDuration(duration // 4)
        fade_out.setStartValue(1)
        fade_out.setEndValue(0)
        anim_group.addAnimation(fade_out)

        anim_group.finished.connect(widget.deleteLater)
        anim_group.start()

        return anim_group

    @staticmethod
    def spiral_in(widget, duration=2500):
        """Spiral in from corner"""
        opacity_effect = QGraphicsOpacityEffect(widget)
        widget.setGraphicsEffect(opacity_effect)

        # This would need custom path animation
        # For now, use combined rotation and position

        end_rect = widget.geometry()
        parent = widget.parent()
        parent_width = parent.width() if parent else 1920
        parent_height = parent.height() if parent else 1080

        # Start from corner
        start_rect = QRect(
            parent_width - end_rect.width(),
            0,
            end_rect.width(),
            end_rect.height()
        )

        widget.setGeometry(start_rect)

        # Animate to center position
        geom_anim = QPropertyAnimation(widget, b"geometry")
        geom_anim.setDuration(duration)
        geom_anim.setStartValue(start_rect)
        geom_anim.setEndValue(end_rect)
        geom_anim.setEasingCurve(QEasingCurve.Type.InOutCubic)

        # Fade animation
        fade_seq = QSequentialAnimationGroup(widget)

        fade_in = QPropertyAnimation(opacity_effect, b"opacity")
        fade_in.setDuration(duration // 3)
        fade_in.setStartValue(0)
        fade_in.setEndValue(1)

        hold = QPropertyAnimation(opacity_effect, b"opacity")
        hold.setDuration(duration // 3)
        hold.setStartValue(1)
        hold.setEndValue(1)

        fade_out = QPropertyAnimation(opacity_effect, b"opacity")
        fade_out.setDuration(duration // 3)
        fade_out.setStartValue(1)
        fade_out.setEndValue(0)

        fade_seq.addAnimation(fade_in)
        fade_seq.addAnimation(hold)
        fade_seq.addAnimation(fade_out)

        # Combine
        parallel = QParallelAnimationGroup(widget)
        parallel.addAnimation(geom_anim)
        parallel.addAnimation(fade_seq)

        parallel.finished.connect(widget.deleteLater)
        parallel.start()

        return parallel

    # Helper methods for particle effects
    @staticmethod
    def _add_sparkles(widget, duration):
        """Add sparkle particles around widget"""
        # This would create small particle widgets
        # Implementation would need ParticleWidget class
        pass

    @staticmethod
    def _create_explosion_particles(widget, duration):
        """Create explosion particle effect"""
        # This would create particles flying outward
        pass


    @staticmethod
    def bounce_in(widget, duration=2500):
        """Bounce in from top with physics"""
        opacity_effect = QGraphicsOpacityEffect(widget)
        widget.setGraphicsEffect(opacity_effect)

        start_rect = widget.geometry()

        # Start from top
        top_rect = QRect(
            start_rect.x(),
            -start_rect.height(),
            start_rect.width(),
            start_rect.height()
        )
        widget.setGeometry(top_rect)

        anim_group = QParallelAnimationGroup(widget)

        # Bounce down animation
        bounce_anim = QPropertyAnimation(widget, b"geometry")
        bounce_anim.setDuration(duration)
        bounce_anim.setStartValue(top_rect)
        bounce_anim.setEndValue(start_rect)
        bounce_anim.setEasingCurve(QEasingCurve.Type.OutBounce)

        # Fade in
        fade_anim = QPropertyAnimation(opacity_effect, b"opacity")
        fade_anim.setDuration(duration)
        fade_anim.setKeyValueAt(0, 0)
        fade_anim.setKeyValueAt(0.2, 1)
        fade_anim.setKeyValueAt(0.8, 1)
        fade_anim.setKeyValueAt(1, 0)

        anim_group.addAnimation(bounce_anim)
        anim_group.addAnimation(fade_anim)

        anim_group.finished.connect(widget.deleteLater)
        anim_group.start()

        return anim_group

    @staticmethod
    def rotate_zoom(widget, duration=3000):
        """Rotate while zooming in"""
        opacity_effect = QGraphicsOpacityEffect(widget)
        widget.setGraphicsEffect(opacity_effect)

        start_rect = widget.geometry()
        center_x = start_rect.x() + start_rect.width() // 2
        center_y = start_rect.y() + start_rect.height() // 2

        anim_group = QParallelAnimationGroup(widget)

        # Zoom animation
        geom_anim = QPropertyAnimation(widget, b"geometry")
        geom_anim.setDuration(duration)

        tiny_size = int(start_rect.width() * 0.2)
        tiny_rect = QRect(
            center_x - tiny_size // 2,
            center_y - tiny_size // 2,
            tiny_size, tiny_size
        )

        geom_anim.setKeyValueAt(0, tiny_rect)
        geom_anim.setKeyValueAt(0.5, start_rect)
        geom_anim.setKeyValueAt(1, start_rect)
        geom_anim.setEasingCurve(QEasingCurve.Type.OutBack)

        # Opacity
        opacity_anim = QPropertyAnimation(opacity_effect, b"opacity")
        opacity_anim.setDuration(duration)
        opacity_anim.setKeyValueAt(0, 0)
        opacity_anim.setKeyValueAt(0.3, 1)
        opacity_anim.setKeyValueAt(0.7, 1)
        opacity_anim.setKeyValueAt(1, 0)

        anim_group.addAnimation(geom_anim)
        anim_group.addAnimation(opacity_anim)

        anim_group.finished.connect(widget.deleteLater)
        anim_group.start()

        return anim_group

    @staticmethod
    def wave_slide(widget, duration=3000):
        """Slide in with wave motion"""
        opacity_effect = QGraphicsOpacityEffect(widget)
        widget.setGraphicsEffect(opacity_effect)

        end_rect = widget.geometry()
        parent = widget.parent()
        parent_width = parent.width() if parent else 1920

        # Start from right with wave
        start_rect = QRect(
            parent_width,
            end_rect.y(),
            end_rect.width(),
            end_rect.height()
        )
        widget.setGeometry(start_rect)

        anim_group = QSequentialAnimationGroup(widget)

        # Slide in with wave (up-down motion)
        slide_anim = QPropertyAnimation(widget, b"geometry")
        slide_anim.setDuration(duration // 2)

        # Intermediate position (slightly above final)
        mid_rect = QRect(
            end_rect.x(),
            end_rect.y() - 30,
            end_rect.width(),
            end_rect.height()
        )

        slide_anim.setStartValue(start_rect)
        slide_anim.setEndValue(mid_rect)
        slide_anim.setEasingCurve(QEasingCurve.Type.OutCubic)

        # Settle down
        settle_anim = QPropertyAnimation(widget, b"geometry")
        settle_anim.setDuration(duration // 4)
        settle_anim.setStartValue(mid_rect)
        settle_anim.setEndValue(end_rect)
        settle_anim.setEasingCurve(QEasingCurve.Type.OutBounce)

        # Hold
        hold_anim = QPropertyAnimation(widget, b"geometry")
        hold_anim.setDuration(duration // 4)
        hold_anim.setStartValue(end_rect)
        hold_anim.setEndValue(end_rect)

        anim_group.addAnimation(slide_anim)
        anim_group.addAnimation(settle_anim)
        anim_group.addAnimation(hold_anim)

        # Fade
        fade_seq = QSequentialAnimationGroup(widget)
        fade_in = QPropertyAnimation(opacity_effect, b"opacity")
        fade_in.setDuration(duration // 3)
        fade_in.setStartValue(0)
        fade_in.setEndValue(1)

        hold_opacity = QPropertyAnimation(opacity_effect, b"opacity")
        hold_opacity.setDuration(duration // 3)
        hold_opacity.setStartValue(1)
        hold_opacity.setEndValue(1)

        fade_out = QPropertyAnimation(opacity_effect, b"opacity")
        fade_out.setDuration(duration // 3)
        fade_out.setStartValue(1)
        fade_out.setEndValue(0)

        fade_seq.addAnimation(fade_in)
        fade_seq.addAnimation(hold_opacity)
        fade_seq.addAnimation(fade_out)

        # Run both in parallel
        parallel = QParallelAnimationGroup(widget)
        parallel.addAnimation(anim_group)
        parallel.addAnimation(fade_seq)

        parallel.finished.connect(widget.deleteLater)
        parallel.start()

        return parallel


    @staticmethod
    def bounce_cascade(widget, duration=3000):
        """Professional bounce cascade effect - PREMIUM!"""
        opacity_effect = QGraphicsOpacityEffect(widget)
        widget.setGraphicsEffect(opacity_effect)

        start_rect = widget.geometry()
        center_x = start_rect.x() + start_rect.width() // 2
        center_y = start_rect.y() + start_rect.height() // 2

        # Multiple bounces with decreasing intensity
        anim_group = QSequentialAnimationGroup(widget)

        # Start from tiny
        tiny_size = int(start_rect.width() * 0.15)
        tiny_rect = QRect(
            center_x - tiny_size // 2,
            center_y - tiny_size // 2,
            tiny_size, tiny_size
        )
        widget.setGeometry(tiny_rect)

        # Bounce 1 - Big
        bounce1 = QPropertyAnimation(widget, b"geometry")
        bounce1.setDuration(duration // 4)
        large1 = int(start_rect.width() * 1.4)
        large_rect1 = QRect(
            center_x - large1 // 2,
            center_y - large1 // 2,
            large1, large1
        )
        bounce1.setStartValue(tiny_rect)
        bounce1.setEndValue(large_rect1)
        bounce1.setEasingCurve(QEasingCurve.Type.OutBounce)

        # Bounce 2 - Medium
        bounce2 = QPropertyAnimation(widget, b"geometry")
        bounce2.setDuration(duration // 4)
        medium_size = int(start_rect.width() * 1.2)
        medium_rect = QRect(
            center_x - medium_size // 2,
            center_y - medium_size // 2,
            medium_size, medium_size
        )
        bounce2.setStartValue(large_rect1)
        bounce2.setEndValue(medium_rect)
        bounce2.setEasingCurve(QEasingCurve.Type.OutBounce)

        # Settle to normal
        settle = QPropertyAnimation(widget, b"geometry")
        settle.setDuration(duration // 4)
        settle.setStartValue(medium_rect)
        settle.setEndValue(start_rect)
        settle.setEasingCurve(QEasingCurve.Type.OutElastic)

        # Hold
        hold = QPropertyAnimation(widget, b"geometry")
        hold.setDuration(duration // 4)
        hold.setStartValue(start_rect)
        hold.setEndValue(start_rect)

        anim_group.addAnimation(bounce1)
        anim_group.addAnimation(bounce2)
        anim_group.addAnimation(settle)
        anim_group.addAnimation(hold)

        # Opacity
        opacity_anim = QPropertyAnimation(opacity_effect, b"opacity")
        opacity_anim.setDuration(duration)
        opacity_anim.setKeyValueAt(0, 0)
        opacity_anim.setKeyValueAt(0.1, 1)
        opacity_anim.setKeyValueAt(0.9, 1)
        opacity_anim.setKeyValueAt(1, 0)

        parallel = QParallelAnimationGroup(widget)
        parallel.addAnimation(anim_group)
        parallel.addAnimation(opacity_anim)

        parallel.finished.connect(widget.deleteLater)
        parallel.start()

        return parallel

    @staticmethod
    def explosion_particles(widget, duration=5000):
        """Particle explosion effect - PREMIUM!"""
        opacity_effect = QGraphicsOpacityEffect(widget)
        widget.setGraphicsEffect(opacity_effect)

        start_rect = widget.geometry()

        # Main zoom animation
        anim_group = QSequentialAnimationGroup(widget)

        # Quick zoom in
        zoom_in = QPropertyAnimation(widget, b"geometry")
        zoom_in.setDuration(duration // 5)
        center_x = start_rect.x() + start_rect.width() // 2
        center_y = start_rect.y() + start_rect.height() // 2

        tiny_size = int(start_rect.width() * 0.1)
        tiny_rect = QRect(
            center_x - tiny_size // 2,
            center_y - tiny_size // 2,
            tiny_size, tiny_size
        )

        huge_size = int(start_rect.width() * 1.6)
        huge_rect = QRect(
            center_x - huge_size // 2,
            center_y - huge_size // 2,
            huge_size, huge_size
        )

        zoom_in.setStartValue(tiny_rect)
        zoom_in.setEndValue(huge_rect)
        zoom_in.setEasingCurve(QEasingCurve.Type.OutCubic)

        # Shake at peak
        shake1 = QPropertyAnimation(widget, b"geometry")
        shake1.setDuration(100)
        shake_rect = QRect(
            huge_rect.x() + 10,
            huge_rect.y() + 10,
            huge_rect.width(),
            huge_rect.height()
        )
        shake1.setStartValue(huge_rect)
        shake1.setEndValue(shake_rect)

        shake2 = QPropertyAnimation(widget, b"geometry")
        shake2.setDuration(100)
        shake2.setStartValue(shake_rect)
        shake2.setEndValue(huge_rect)

        # Hold big
        hold = QPropertyAnimation(widget, b"geometry")
        hold.setDuration(duration // 2)
        hold.setStartValue(huge_rect)
        hold.setEndValue(huge_rect)

        # Shrink to normal
        shrink = QPropertyAnimation(widget, b"geometry")
        shrink.setDuration(duration // 4)
        shrink.setStartValue(huge_rect)
        shrink.setEndValue(start_rect)
        shrink.setEasingCurve(QEasingCurve.Type.InOutBack)

        anim_group.addAnimation(zoom_in)
        anim_group.addAnimation(shake1)
        anim_group.addAnimation(shake2)
        anim_group.addAnimation(hold)
        anim_group.addAnimation(shrink)

        # Opacity
        opacity_anim = QPropertyAnimation(opacity_effect, b"opacity")
        opacity_anim.setDuration(duration)
        opacity_anim.setKeyValueAt(0, 0)
        opacity_anim.setKeyValueAt(0.15, 1)
        opacity_anim.setKeyValueAt(0.85, 1)
        opacity_anim.setKeyValueAt(1, 0)

        parallel = QParallelAnimationGroup(widget)
        parallel.addAnimation(anim_group)
        parallel.addAnimation(opacity_anim)

        parallel.finished.connect(widget.deleteLater)
        parallel.start()

        return parallel

    @staticmethod
    def screen_takeover(widget, duration=8000):
        """MEGA effect - takes over screen! PREMIUM!"""
        opacity_effect = QGraphicsOpacityEffect(widget)
        widget.setGraphicsEffect(opacity_effect)

        start_rect = widget.geometry()
        parent = widget.parent()
        parent_width = parent.width() if parent else 1920
        parent_height = parent.height() if parent else 1080

        # Start from center tiny
        center_x = parent_width // 2
        center_y = parent_height // 2

        tiny_size = 20
        tiny_rect = QRect(
            center_x - tiny_size // 2,
            center_y - tiny_size // 2,
            tiny_size, tiny_size
        )
        widget.setGeometry(tiny_rect)

        # Explode to MASSIVE
        massive_size = min(parent_width, parent_height) - 100
        massive_rect = QRect(
            center_x - massive_size // 2,
            center_y - massive_size // 2,
            massive_size, massive_size
        )

        anim_group = QSequentialAnimationGroup(widget)

        # EXPLODE!
        explode = QPropertyAnimation(widget, b"geometry")
        explode.setDuration(duration // 4)
        explode.setStartValue(tiny_rect)
        explode.setEndValue(massive_rect)
        explode.setEasingCurve(QEasingCurve.Type.OutCubic)

        # Pulse 3 times
        for i in range(3):
            pulse_big = QPropertyAnimation(widget, b"geometry")
            pulse_big.setDuration(200)
            pulse_size = massive_size + 50
            pulse_rect = QRect(
                center_x - pulse_size // 2,
                center_y - pulse_size // 2,
                pulse_size, pulse_size
            )
            pulse_big.setStartValue(massive_rect)
            pulse_big.setEndValue(pulse_rect)

            pulse_small = QPropertyAnimation(widget, b"geometry")
            pulse_small.setDuration(200)
            pulse_small.setStartValue(pulse_rect)
            pulse_small.setEndValue(massive_rect)

            anim_group.addAnimation(pulse_big)
            anim_group.addAnimation(pulse_small)

        # Hold massive
        hold = QPropertyAnimation(widget, b"geometry")
        hold.setDuration(duration // 2)
        hold.setStartValue(massive_rect)
        hold.setEndValue(massive_rect)
        anim_group.addAnimation(hold)

        # Shrink to position
        shrink = QPropertyAnimation(widget, b"geometry")
        shrink.setDuration(duration // 4)
        shrink.setStartValue(massive_rect)
        shrink.setEndValue(start_rect)
        shrink.setEasingCurve(QEasingCurve.Type.InBack)
        anim_group.addAnimation(shrink)

        # Opacity
        opacity_anim = QPropertyAnimation(opacity_effect, b"opacity")
        opacity_anim.setDuration(duration)
        opacity_anim.setKeyValueAt(0, 0)
        opacity_anim.setKeyValueAt(0.1, 1)
        opacity_anim.setKeyValueAt(0.9, 1)
        opacity_anim.setKeyValueAt(1, 0)

        parallel = QParallelAnimationGroup(widget)
        parallel.addAnimation(anim_group)
        parallel.addAnimation(opacity_anim)

        parallel.finished.connect(widget.deleteLater)
        parallel.start()

        return parallel

    @staticmethod
    def neon_glow(widget, duration=3500):
        """Neon glow pulse effect - PREMIUM!"""
        opacity_effect = QGraphicsOpacityEffect(widget)
        widget.setGraphicsEffect(opacity_effect)

        # Fade in with glow
        fade_in = QPropertyAnimation(opacity_effect, b"opacity")
        fade_in.setDuration(duration)
        fade_in.setKeyValueAt(0, 0)
        fade_in.setKeyValueAt(0.2, 1)
        fade_in.setKeyValueAt(0.8, 1)
        fade_in.setKeyValueAt(1, 0)

        fade_in.finished.connect(widget.deleteLater)
        fade_in.start()

        return fade_in

    @staticmethod
    def matrix_rain(widget, duration=4000):
        """Matrix-style digital rain effect - PREMIUM!"""
        opacity_effect = QGraphicsOpacityEffect(widget)
        widget.setGraphicsEffect(opacity_effect)

        start_rect = widget.geometry()

        # Fall from top
        top_rect = QRect(
            start_rect.x(),
            -start_rect.height() - 200,
            start_rect.width(),
            start_rect.height()
        )
        widget.setGeometry(top_rect)

        anim_group = QSequentialAnimationGroup(widget)

        # Drop down
        drop = QPropertyAnimation(widget, b"geometry")
        drop.setDuration(duration // 3)
        drop.setStartValue(top_rect)
        drop.setEndValue(start_rect)
        drop.setEasingCurve(QEasingCurve.Type.InCubic)

        # Glitch effect
        glitch1 = QPropertyAnimation(widget, b"geometry")
        glitch1.setDuration(50)
        glitch_rect = QRect(
            start_rect.x() + 20,
            start_rect.y(),
            start_rect.width(),
            start_rect.height()
        )
        glitch1.setStartValue(start_rect)
        glitch1.setEndValue(glitch_rect)

        glitch2 = QPropertyAnimation(widget, b"geometry")
        glitch2.setDuration(50)
        glitch2.setStartValue(glitch_rect)
        glitch2.setEndValue(start_rect)

        # Hold
        hold = QPropertyAnimation(widget, b"geometry")
        hold.setDuration(duration // 2)
        hold.setStartValue(start_rect)
        hold.setEndValue(start_rect)

        anim_group.addAnimation(drop)
        anim_group.addAnimation(glitch1)
        anim_group.addAnimation(glitch2)
        anim_group.addAnimation(hold)

        # Opacity
        opacity_anim = QPropertyAnimation(opacity_effect, b"opacity")
        opacity_anim.setDuration(duration)
        opacity_anim.setKeyValueAt(0, 0)
        opacity_anim.setKeyValueAt(0.2, 1)
        opacity_anim.setKeyValueAt(0.8, 1)
        opacity_anim.setKeyValueAt(1, 0)

        parallel = QParallelAnimationGroup(widget)
        parallel.addAnimation(anim_group)
        parallel.addAnimation(opacity_anim)

        parallel.finished.connect(widget.deleteLater)
        parallel.start()

        return parallel


# Effect registry for easy access
EFFECT_REGISTRY = {
    # Original effects
    'fade_in_out': BubbleEffects.fade_in_out,
    'sparkle_zoom': BubbleEffects.sparkle_zoom,
    'slide_bounce': BubbleEffects.slide_bounce,
    'float_away': BubbleEffects.float_away,
    'heart_pulse': BubbleEffects.heart_pulse,
    'quick_pop': BubbleEffects.quick_pop,
    'firework': BubbleEffects.firework_explosion,
    'rainbow': BubbleEffects.rainbow_rotate,
    'shake': BubbleEffects.shake_vibrate,
    'spiral': BubbleEffects.spiral_in,
    'bounce_in': BubbleEffects.bounce_in,
    'rotate_zoom': BubbleEffects.rotate_zoom,
    'wave_slide': BubbleEffects.wave_slide,
    # NEW PREMIUM EFFECTS
    'bounce_cascade': BubbleEffects.bounce_cascade,
    'explosion_particles': BubbleEffects.explosion_particles,
    'screen_takeover': BubbleEffects.screen_takeover,
    'neon_glow': BubbleEffects.neon_glow,
    'matrix_rain': BubbleEffects.matrix_rain,
}

# Effect descriptions for UI
EFFECT_DESCRIPTIONS = {
    'fade_in_out': 'Simple fade - Minimal',
    'sparkle_zoom': 'Dramatic zoom - Great for gifts!',
    'slide_bounce': 'Bouncy slide - Energetic',
    'float_away': 'Float upward - Gentle',
    'heart_pulse': 'Pulsing heart - Romantic',
    'quick_pop': 'Quick pop - Fast',
    'firework': 'Explosion - Spectacular',
    'rainbow': 'Rainbow colors - Colorful',
    'shake': 'Vibrate - Hype',
    'spiral': 'Spiral path - Elegant',
    'bounce_in': 'Bounce from top - Fun',
    'rotate_zoom': 'Rotate & zoom - Dynamic',
    'wave_slide': 'Wave motion - Smooth',
    'bounce_cascade': '[PREMIUM] Multiple bounces',
    'explosion_particles': '[PREMIUM] Particle explosion',
    'screen_takeover': '[MEGA] Takes over screen!',
    'neon_glow': '[PREMIUM] Neon pulse',
    'matrix_rain': '[PREMIUM] Matrix style',
}
