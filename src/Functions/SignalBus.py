from ModuleLogger import logger
from PySide6.QtCore import QObject, Signal


class SignalBus(QObject):
    """Signal bus"""

    switch_page_signal = Signal(str)

    # message signal
    info_signal = Signal(str)
    warning_signal = Signal(str)
    error_signal = Signal(str)
    status_signal = Signal(str, str)

    # setting signal
    mica_enable_change_signal = Signal(bool)


signalBus = SignalBus()
logger.debug(signalBus)
