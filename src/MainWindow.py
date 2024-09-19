from Functions.LogBase import get_logger

from qfluentwidgets import setTheme


def main():
    """Main function for the application."""
    logger = get_logger("main")
    logger.info("start application...")

    setTheme(cfg.get(cfg.themeMode))
