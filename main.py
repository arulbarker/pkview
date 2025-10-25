"""
TikTok Live PK Battle Application
Main entry point for the desktop application
"""

import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt


def main():
    """Main application entry point"""

    try:
        # Create application
        app = QApplication(sys.argv)

        # Import after QApplication created to avoid warnings
        from pk_main_window import PKMainWindow
        app.setApplicationName("TikTok Live PK Battle")
        app.setOrganizationName("TikTokPKApp")

        # Set application style
        app.setStyle('Fusion')

        # Create and show main window
        print("Creating main window...")
        window = PKMainWindow()
        print("Main window created successfully!")

        window.show()
        print("Window shown!")

        # Run application
        sys.exit(app.exec())

    except Exception as e:
        print(f"\nFATAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        input("Press Enter to exit...")
        sys.exit(1)


if __name__ == '__main__':
    main()
