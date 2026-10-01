import unittest

from generate_page import extract_title


class TestGeneratePage(unittest.TestCase):
    def test_extract_title_without_title(self):
        markdown = "this markdown has no title, this is just a subheading"
        with self.assertRaises(Exception):
            extract_title(markdown)

    def test_extract_title_with_incorrect_markdown(self):
        markdown = "#this markdown has a title but incorrect markdown"
        with self.assertRaises(Exception):
            extract_title(markdown)

    def test_extract_title_correctly(self):
        markdown = "# example title \n ## subheading"
        self.assertEqual(extract_title(markdown), "example title")

    def test_extract_title_with_extra_spaced_title(self):
        markdown = "#   too many spaces before and after     "
        self.assertEqual(extract_title(markdown), "too many spaces before and after")

    def test_extract_title_when_title_appears_after(self):
        markdown = "## subheading first \n# title later"
        self.assertEqual(extract_title(markdown), "title later")

    def test_extract_title_when_multiple_headings(self):
        # this should return the first title encountered
        markdown = "# first title \n# second title\n# third title"
        self.assertEqual(extract_title(markdown), "first title")

    def test_extract_title_when_title_appears_later(self):
        markdown = """
## subheading here

- random item 1
- random item 2
- random item 3

#### some text here

# markdown title in the middle

some paragraph text
some paragraph text

> block quote
        """
        self.assertEqual(extract_title(markdown), "markdown title in the middle")


#    def test_extract_title_when_line_has_whitespaces_before_tags(self):
#    commented this test since I'm keeping my parser strict, and so this test test something that I explicitly decided to keep out
#        markdown = "  # sample title"
#        self.assertEqual(extract_title(markdown), "sample title")
