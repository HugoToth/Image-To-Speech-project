import sys
from PyQt6.QtWidgets import QApplication
from gui.main_window import MainWindow

def main():
    """
    Main entry point for the application.
    Initializes the QApplication and displays the main window.
    """
    # Create the application instance. sys.argv allows command-line arguments.
    app = QApplication(sys.argv)

    # Create an instance of our main window
    window = MainWindow()

    # Show the window
    window.show()

    # Start the application's event loop and wait for it to be closed.
    # sys.exit ensures a clean exit.
    sys.exit(app.exec())

# Check if this script is being run directly (not imported)
if __name__ == "__main__":
    main()