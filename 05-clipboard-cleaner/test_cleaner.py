import unittest

from cleaner import clean_text


class CleanTextTests(unittest.TestCase):
    def test_collapses_spaces_and_newlines(self):
        self.assertEqual(clean_text("  Hello   \n\n world \t again  "), "Hello world again")

    def test_windows_line_endings(self):
        self.assertEqual(clean_text("a\r\nb\r\nc"), "a b c")

    def test_non_breaking_and_zero_width(self):
        self.assertEqual(clean_text("a  b​c"), "a bc")

    def test_keep_paragraphs(self):
        messy = "First   line\nsecond line\n\n\n  Next   para \n"
        self.assertEqual(clean_text(messy, keep_paragraphs=True),
                         "First line second line\n\nNext para")

    def test_empty(self):
        self.assertEqual(clean_text("   \n  "), "")


if __name__ == "__main__":
    unittest.main()
