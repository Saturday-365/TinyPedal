#  TinyPedal is an open-source overlay application for racing simulation.
#  Copyright (C) 2022-2026 TinyPedal developers, see contributors.md file
#
#  This file is part of TinyPedal.
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""Application translations and localized display names."""

import logging

from PySide2.QtCore import QCoreApplication, QTranslator

from ..constant import APP, FILE
from ..formatter import format_module_name, format_option_name

logger = logging.getLogger(__name__)


def install_translations(root: QCoreApplication, language: str):
    """Install translations for the lifetime of the application."""
    if language == APP.DEFAULT_LANGUAGE or language not in APP.LANGUAGES:
        return
    # 分开维护界面文案与动态标签，Qt 提取文本时不会覆盖动态标签。
    for catalog in ("ui", "labels"):
        translator = QTranslator(root)
        filename = f"{catalog}_{language}.qm"
        if translator.load(filename, FILE.PATH_TRANSLATIONS):
            root.installTranslator(translator)
        else:
            logger.warning("Translation file unavailable: %s", filename)
            translator.deleteLater()


def option_label(name: str) -> str:
    """Translate a configuration key for display."""
    translated = QCoreApplication.translate("ConfigOption", name)
    return format_option_name(name) if translated == name else translated


def module_label(name: str) -> str:
    """Translate a widget or module key for display."""
    translated = QCoreApplication.translate("ModuleName", name)
    return format_module_name(name) if translated == name else translated
