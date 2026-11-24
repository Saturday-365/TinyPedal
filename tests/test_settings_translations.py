import ast
import unittest
from pathlib import Path
from xml.etree import ElementTree

from tinypedal.constant import APP
from tinypedal.regex_pattern import CHOICE_COMMON, CHOICE_UNITS
from tinypedal.setting.default_heatmap import HEATMAP_DEFAULT
from tinypedal.setting.default_shortcuts import SHORTCUTS_GENERAL, SHORTCUTS_PRESET


ROOT = Path(__file__).resolve().parents[1]
DEFAULTS = {
    "default_api": "API_DEFAULT",
    "default_common": "COMMON_DEFAULT",
    "default_global": "GLOBAL_DEFAULT",
    "default_module": "MODULE_DEFAULT",
    "default_widget": "WIDGET_DEFAULT",
}


class SettingsTranslationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        catalog = ROOT / "tinypedal" / "translations" / "labels_zh_CN.ts"
        cls.labels = {
            context.findtext("name"): {
                message.findtext("source")
                for message in context.findall("message")
                if any("\u4e00" <= char <= "\u9fff" for char in message.findtext("translation", ""))
                and message.find("translation").get("type") not in {"unfinished", "vanished", "obsolete"}
            }
            for context in ElementTree.parse(catalog).findall("context")
        }

    def test_default_settings_have_chinese_labels(self):
        for module, constant in DEFAULTS.items():
            with self.subTest(module=module):
                # 静态读取全局默认项，避免检查时创建用户配置目录。
                path = ROOT / "tinypedal" / "setting" / f"{module}.py"
                source = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
                settings = next(
                    node.value for node in source.body
                    if isinstance(node, ast.Assign) and any(
                        isinstance(target, ast.Name) and target.id == constant for target in node.targets
                    )
                )
                keys = {ast.literal_eval(key) for section in settings.values for key in section.keys}
                self.assertEqual(keys - self.labels["ConfigOption"], set())
                order_names = {key[len("display_order_"):] for key in keys if key.startswith("display_order_")}
                self.assertEqual(order_names - self.labels["ConfigOption"], set())

    def test_default_choices_have_chinese_labels(self):
        values = {
            value for choices in (*CHOICE_COMMON.values(), *CHOICE_UNITS.values()) for value in choices
        }
        values.update(HEATMAP_DEFAULT, APP.LANGUAGES.values(), ("no change", "enable", "disable"))
        self.assertEqual(values - self.labels["ConfigValue"], set())

    def test_shortcuts_have_chinese_labels(self):
        keys = set(SHORTCUTS_GENERAL) | SHORTCUTS_PRESET.keys()
        self.assertEqual(keys - self.labels["ConfigOption"], set())
