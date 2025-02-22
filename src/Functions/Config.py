import re
import sys
from enum import Enum

from ModuleLogger import logger
from PySide6.QtCore import QLocale
from qfluentwidgets import (
    BoolValidator,
    ConfigItem,
    ConfigSerializer,
    ConfigValidator,
    FolderValidator,
    OptionsConfigItem,
    OptionsValidator,
    QConfig,
    RangeConfigItem,
    RangeValidator,
    Theme,
    qconfig,
)


class Language(Enum):
    """Language enumeration"""

    CHINESE_SIMPLIFIED = QLocale(QLocale.Chinese, QLocale.China)
    # CHINESE_TRADITIONAL = QLocale(QLocale.Chinese, QLocale.HongKong)
    ENGLISH = QLocale(QLocale.English)
    AUTO = QLocale()


class LanguageSerializer(ConfigSerializer):
    """Language serializer"""

    def serialize(self, language):
        return language.value.name() if language != Language.AUTO else "Auto"

    def deserialize(self, value: str):
        return Language(QLocale(value)) if value != "Auto" else Language.AUTO


class ProviderUrlValidator(ConfigValidator):
    """Config validator"""

    url_pattern = r"^((http|https)://)([a-zA-Z0-9\-\.]+)(:[0-9]+)?(/[\w \.-]*)?$"

    def validate(self, url: str):
        """Verify whether the value is legal"""
        if re.match(self.url_pattern, url):
            return True
        return False

    def correct(self, url: str):
        """correct illegal value"""
        if url == "Default" or url == "":
            return "Default"
        return url


def isWin11():
    return sys.platform == "win32" and sys.getwindowsversion().build >= 22000


class Config(QConfig):
    """Config of application"""

    # main window
    mica_enabled = ConfigItem("MainWindow", "MicaEnabled", isWin11(), BoolValidator())
    dpiScale = OptionsConfigItem(
        "MainWindow",
        "DpiScale",
        "Auto",
        OptionsValidator([1, 1.25, 1.5, 1.75, 2, "Auto"]),
        restart=True,
    )
    language = OptionsConfigItem(
        "MainWindow",
        "Language",
        Language.AUTO,
        OptionsValidator(Language),
        LanguageSerializer(),
        restart=True,
    )

    # Material
    blurRadius = RangeConfigItem(
        "Material", "AcrylicBlurRadius", 15, RangeValidator(0, 40)
    )

    # software update
    checkUpdateAtStartUp = ConfigItem(
        "Update", "CheckUpdateAtStartUp", True, BoolValidator()
    )


YEAR = 2024
AUTHOR = "Layton"
VERSION = "0.1"
HELP_URL = "https://github.com/HATTER-LONG/Verbiverse"
REPO_URL = "https://github.com/HATTER-LONG/Verbiverse"
FEEDBACK_URL = "https://github.com/HATTER-LONG/Verbiverse/issues"
RELEASE_URL = "https://github.com/HATTER-LONG/Verbiverse/releases/latest"
CONFIG_PATH = "./app/config/"


cfg = Config()
cfg.themeMode.value = Theme.AUTO
qconfig.load("app/config/config.json", cfg)
logger.debug(cfg)
