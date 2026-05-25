import unittest

from markdown_blocks import (
    BlockType,
    block_to_block_type,
    heading_to_html_node,
    markdown_to_blocks,
    markdown_to_html_node,
    olist_to_html_node,
    paragraph_to_html_node,
)


class TestMarkdownToHTML(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_filters_empty_blocks(self):
        md = """This is _italic_ line



Another random `code` line
Unknown text with multiple \n \n newline characters in between."""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is _italic_ line",
                "Another random `code` line\nUnknown text with multiple \n \n newline characters in between.",
            ],
        )

    def test_block_to_blocktype_headings(self):
        block = "# heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
        block = "```\ncode\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
        block = "> quote\n> more quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
        block = "- list\n- items"
        self.assertEqual(block_to_block_type(block), BlockType.ULIST)
        block = "1. list\n2. items"
        self.assertEqual(block_to_block_type(block), BlockType.OLIST)
        block = "paragraph"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_heading_h2(self):
        node = heading_to_html_node("## Hello **world**")
        self.assertEqual(node.to_html(), "<h2>Hello <b>world</b></h2>")

    def test_ordered_list(self):
        md = """1. Item 1\n2. Item 2\n3. Item 3"""
        node = olist_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<ol><li>Item 1</li><li>Item 2</li><li>Item 3</li></ol>",
        )

    def test_blockquote(self):
        md = """
> This is a 
> blockquote block

this is a paragraph text


"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote block</blockquote><p>this is a paragraph text</p></div>",
        )


if __name__ == "__main__":
    unittest.main()
