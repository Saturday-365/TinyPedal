import unittest

from tinypedal.constant import APP
from tinypedal.setting.validator import PresetValidator
from tinypedal.version import __version__


class LanguageConfigTest(unittest.TestCase):
    def test_existing_config_defaults_to_english(self):
        self.assertEqual(self.validate_application({}), "en")

    def test_chinese_survives_validation(self):
        self.assertEqual(self.validate_application({"ui_language": "zh_CN"}), "zh_CN")

    def test_invalid_language_defaults_to_english(self):
        for value in ("unknown", 1, None, {"locale": "zh_CN"}):
            with self.subTest(value=value):
                self.assertEqual(self.validate_application({"ui_language": value}), "en")

    @staticmethod
    def validate_application(application):
        # 模拟同版本旧配置，验证语言字段的补全和校验。
        defaults = {
            "preset": {"version": __version__},
            "application": {"ui_language": APP.DEFAULT_LANGUAGE},
        }
        user_config = {
            "preset": {"version": __version__},
            "application": application,
        }
        return PresetValidator.global_preset(user_config, defaults)["application"]["ui_language"]
