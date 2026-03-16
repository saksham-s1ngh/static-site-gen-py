import unittest

from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    """
    def test_noteq(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        node2 = TextNode("this is an italic node", TextType.ITALIC)
        self.assertNotEqual(node, node2)
    """
    def test_eq_false(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_eq_false2(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node2", TextType.BOLD)
        self.assertNotEqual(node, node2)

    """
    def test_urleq(self):
        node = TextNode("This is url 1", TextType.LINK, "#url1")
        node2 = TextNode("This is url 1", TextType.LINK, "#url1")
        self.assertEqual(node, node2)
    """
    def test_eq_url(self):
        node = TextNode("This is a text node", TextType.ITALIC, "https://www.boot.dev")
        node2 = TextNode("This is a text node", TextType.ITALIC, "https://www.boot.dev")
        self.assertEqual(node, node2)

    def test_eq_url_false(self):
        node = TextNode("This is url a", TextType.LINK, "#urla")
        node2 = TextNode("This is url b", TextType.LINK, "#urlb")
        self.assertNotEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", TextType.TEXT, "https://www.boot.dev")
        self.assertEqual(
            "TextNode(This is a text node, TextType.TEXT, https://www.boot.dev)", repr(node)
        )

if __name__ == "__main__":
    unittest.main()
