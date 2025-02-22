import asyncio
import sys

from PySide6.QtCore import Qt, QTranslator, Slot
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QFrame, QHBoxLayout
from qasync import QApplication, QEventLoop
from qfluentwidgets import (
    FluentBackgroundTheme,
    FluentTranslator,
    FluentWindow,
    InfoBar,
    InfoBarPosition,
    NavigationItemPosition,
    StateToolTip,
    SubtitleLabel,
    setFont,
    setTheme,
)
from qfluentwidgets import FluentIcon as FIF

from Functions.Config import cfg
from Functions.LogBase import get_logger
from Functions.SignalBus import signalBus
from resources import resources_rc  # noqa: F401


class Widget(QFrame):
    """
    A custom widget that displays a centered subtitle label.

    Args:
        text (str): The text to display in the label.
        parent (QWidget, optional): The parent widget. Defaults to None.
    """

    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.label = SubtitleLabel(text, self)
        self.hBoxLayout = QHBoxLayout(self)

        setFont(self.label, 24)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.hBoxLayout.addWidget(self.label, 1, Qt.AlignmentFlag.AlignCenter)
        self.setObjectName(text.replace(" ", "-"))

        self.hBoxLayout.setContentsMargins(0, 32, 0, 0)


class MainWindow(FluentWindow):
    """
    The main window of the application, containing multiple interfaces and navigation.

    Methods:
        initNavigation(): Initializes the navigation items.
        initWindow(): Sets up the main window properties.
        connectSignalToSlot(): Connects signals to their respective slots.
        switchPage(page_name: str): Switches to the specified page.
        showStatusMessage(title: str, content: str): Displays a status message.
        showInfoMessage(info_message: str): Displays an info message.
        showWarningMessage(warning_message: str): Displays a warning message.
        showErrorMessage(error_message: str): Displays an error message.
    """

    def __init__(self):
        super().__init__()

        from UI.SettingInterface import (
            SettingInterface,
        )

        # Initialize interface pages
        self.interfaceList = []
        self.home_page = Widget("Home", self)
        self.test_page = Widget("Test", self)

        self.setting_page = SettingInterface(self)

        # Add pages to the interface list
        self.interfaceList.append(self.home_page)
        self.interfaceList.append(self.test_page)
        self.interfaceList.append(self.setting_page)

        # Initialize navigation and window settings
        self.initNavigation()
        self.initWindow()
        self.connectSignalToSlot()

    def initNavigation(self):
        """Adds navigation items to the main window."""
        self.addSubInterface(self.home_page, FIF.HOME, self.tr("Home"))
        self.addSubInterface(self.test_page, FIF.CHAT, self.tr("Test Page"))

        self.addSubInterface(
            self.setting_page,
            FIF.SETTING,
            self.tr("Settings"),
            NavigationItemPosition.BOTTOM,
        )

    def initWindow(self):
        """Sets up the main window properties."""
        self.resize(1300, 800)
        self.setWindowIcon(QIcon(":/images/logo.png"))
        self.setWindowTitle("PySide6 Fluent Template")
        self.setCustomBackgroundColor(*FluentBackgroundTheme.DEFAULT_BLUE)
        self.setMicaEffectEnabled(cfg.get(cfg.mica_enabled))

    def connectSignalToSlot(self):
        """Connects signals to their respective slots."""
        signalBus.switch_page_signal.connect(self.switchPage)
        signalBus.info_signal.connect(self.showInfoMessage)
        signalBus.warning_signal.connect(self.showWarningMessage)
        signalBus.error_signal.connect(self.showErrorMessage)
        signalBus.status_signal.connect(self.showStatusMessage)
        self.stateTooltip = None
        signalBus.mica_enable_change_signal.connect(self.setMicaEffectEnabled)

    @Slot(str)
    def switchPage(self, page_name: str):
        """
        Switches to the specified page.

        Args:
            page_name (str): The name of the page to switch to.
        """
        for w in self.interfaceList:
            if w.objectName() == page_name:
                self.stackedWidget.setCurrentWidget(w, False)

    @Slot(str, str)
    def showStatusMessage(self, title: str, content: str):
        """
        Displays a status message.

        Args:
            title (str): The title of the status message.
            content (str): The content of the status message.
        """
        if self.stateTooltip:
            if len(title) > 0:
                self.stateTooltip.setTitle(title)
            self.stateTooltip.setContent(content)
            self.stateTooltip.setState(True)
            self.stateTooltip = None
        else:
            self.stateTooltip = StateToolTip(title, content, self)
            # self.stateTooltip.move(510, 30)
            self.stateTooltip.show()

    @Slot(str)
    def showInfoMessage(self, info_message: str):
        """
        Displays an info message.

        Args:
            info_message (str): The info message to display.
        """
        InfoBar.info(
            title="INFO",
            content=info_message,
            orient=Qt.Orientation.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP_RIGHT,
            duration=-1,
            parent=self,
        )

    @Slot(str)
    def showWarningMessage(self, warning_message: str):
        """
        Displays a warning message.

        Args:
            warning_message (str): The warning message to display.
        """
        InfoBar.warning(
            title="WARN",
            content=warning_message,
            orient=Qt.Orientation.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP_RIGHT,
            duration=-1,
            parent=self,
        )

    @Slot(str)
    def showErrorMessage(self, error_message: str):
        """
        Displays an error message.

        Args:
            error_message (str): The error message to display.
        """
        print("test: ", error_message)
        InfoBar.error(
            title="Error",
            content=error_message,
            orient=Qt.Orientation.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP_RIGHT,
            duration=-1,
            parent=self,
        )


def main():
    """Main function for the application."""
    logger = get_logger("main")
    logger.info("start application...")
    print(cfg.get(cfg.themeMode))
    setTheme(cfg.get(cfg.themeMode))

    app = QApplication(sys.argv)
    event_loop = QEventLoop(app)
    asyncio.set_event_loop(event_loop)

    app_close_event = asyncio.Event()
    app.aboutToQuit.connect(app_close_event.set)
    app.setAttribute(Qt.ApplicationAttribute.AA_DontCreateNativeWidgetSiblings)

    # Internationalization
    locale = cfg.get(cfg.language).value
    translator = FluentTranslator(locale)
    appTranslator = QTranslator()
    appTranslator.load(locale, "app_language", ".", ":/i18n")
    app.installTranslator(translator)
    app.installTranslator(appTranslator)
    window = MainWindow()
    window.show()

    logger.info("start finish...")
    with event_loop:
        event_loop.run_until_complete(app_close_event.wait())
