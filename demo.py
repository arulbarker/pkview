"""
Demo/Test Script for TikTok Live Bubble Application
Run this to see all effects in action without TikTok connection
"""

import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer


def main():
    """Run demo with auto-simulation"""

    # Create application
    app = QApplication(sys.argv)

    # Import after QApplication created
    from main_window import MainWindow

    app.setApplicationName("TikTok Live Bubble - Demo Mode")
    app.setStyle('Fusion')

    # Create and show main window
    window = MainWindow()
    window.show()

    # Auto-run demo after 2 seconds
    def run_demo():
        window._add_log("\n🎬 DEMO MODE: Auto-running all effects...")
        window._add_log("Watch the left panel for bubble animations!\n")

        # Simulate different events with delays
        events = [
            (0, "join", "Join Event - Fade In/Out"),
            (800, "gift", "Gift Event - Sparkle Zoom ⭐"),
            (1600, "comment", "Comment Event - Slide Bounce"),
            (2400, "share", "Share Event - Float Away"),
            (3200, "follow", "Follow Event - Heart Pulse ❤️"),
            (4000, "like", "Like Event - Quick Pop"),
            (5000, "gift", "Another Gift - See the sparkle!"),
            (6000, "comment", "Another Comment - Watch it slide!"),
            (7000, "join", "Another User Joined"),
            (8000, "follow", "Another Follow - Hearts!"),
        ]

        for delay, event_type, description in events:
            QTimer.singleShot(
                delay,
                lambda et=event_type, desc=description: (
                    window._simulate_event(et),
                    window._add_log(f"   ▶ {desc}")
                )
            )

        # Final message
        QTimer.singleShot(9000, lambda: window._add_log(
            "\n✅ Demo complete! Try clicking simulation buttons yourself!"
        ))

    # Start demo after 2 seconds
    QTimer.singleShot(2000, run_demo)

    # Run application
    sys.exit(app.exec())


if __name__ == '__main__':
    print("=" * 60)
    print("TikTok Live Bubble - DEMO MODE")
    print("=" * 60)
    print("This will automatically show all bubble animations!")
    print("Watch the application window for bubble effects.")
    print("=" * 60)
    print()

    main()
