import unittest
from unittest import mock

import logen2


class LogenOverlayTests(unittest.TestCase):
    def test_merge_spreadsheets_replaces_matching_rows_and_appends_new_rows(self):
        base = [
            ["Identifier", "en", "sk"],
            ["hello", "Hello", "Ahoj"],
            ["goodbye", "Goodbye", "Dovidenia"],
        ]
        overlay = [
            ["Identifier", "en", "sk"],
            ["goodbye", "Bye", "Cau"],
            ["welcome", "Welcome", "Vitaj"],
        ]

        merged = logen2.merge_spreadsheets(base, overlay)

        self.assertEqual(
            merged,
            [
                ["Identifier", "en", "sk"],
                ["hello", "Hello", "Ahoj"],
                ["goodbye", "Bye", "Cau"],
                ["welcome", "Welcome", "Vitaj"],
            ],
        )

    def test_generate_strings_accepts_identifier_header(self):
        spreadsheet = [
            ["Identifier", "en", "sk"],
            ["hello", "Hello", "Ahoj"],
        ]

        strings, pluralized_strings = logen2.generate_strings(spreadsheet, "en")

        self.assertEqual(strings, ['"hello" = "Hello";'])
        self.assertEqual(pluralized_strings, [])

    def test_generate_special_strings_accepts_identifier_header(self):
        spreadsheet = [
            ["Identifier", "en", "sk"],
            ["NSCameraUsageDescription(InfoPlist)", "Camera text", "Camera sk"],
        ]

        special = logen2.generate_special_strings(spreadsheet, "en")

        self.assertEqual(
            special,
            {"InfoPlist": ['NSCameraUsageDescription = "Camera text";']},
        )

    def test_get_languages_and_lproj_support_region_codes(self):
        spreadsheet = [
            ["Identifier", "en", "sk_SK", "cs-CZ", "Notes"],
            ["hello", "Hello", "Ahoj", "Ahoj", ""],
        ]

        languages = logen2.get_languages(spreadsheet)

        self.assertEqual(languages, ["en", "sk_SK", "cs-CZ"])
        self.assertEqual(logen2.lproj_language_code("en"), "en")
        self.assertEqual(logen2.lproj_language_code("sk_SK"), "sk_SK")
        self.assertEqual(logen2.lproj_language_code("cs-CZ"), "cs_CZ")

    def test_pip_install_google_apis_uses_pinned_versions_without_upgrade(self):
        with mock.patch("logen2.subprocess.call") as subprocess_call:
            logen2.pip_install_google_apis()

        subprocess_call.assert_called_once_with(
            [
                logen2.sys.executable,
                "-m",
                "pip",
                "install",
                "google-api-python-client==2.128.0",
                "google-auth==2.29.0",
                "google-auth-httplib2==0.2.0",
            ]
        )


if __name__ == "__main__":
    unittest.main()
