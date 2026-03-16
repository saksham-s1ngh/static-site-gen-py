import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_no_prop(self):
        node = HTMLNode("a", "random url", None, None)
        self.assertEqual(node.props_to_html(), "")

    def test_single_prop(self):
        node = HTMLNode("a", "random url", None, {"href":"https://www.boot.dev"})
        self.assertEqual(node.props_to_html(), ' href="https://www.boot.dev"')

    def test_multi_prop(self):
        node = HTMLNode("a", "random url", None, {"href":"https://www.boot.dev", "target":"_blank"})
        self.assertEqual(node.props_to_html(), ' href="https://www.boot.dev" target="_blank"')


