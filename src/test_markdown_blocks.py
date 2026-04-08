import unittest
from markdown_blocks import ( 
    BlockType,
    markdown_to_blocks, 
    block_to_block_type,
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

    def test_markdown_to_blocks_with_empty_blocks(self):
            md = """This is _italic_ line



Another random `code` line
Unknown text with multiple \n \n newline characters in between."""
            blocks = markdown_to_blocks(md)
            self.assertEqual(
                blocks, 
                [
                    "This is _italic_ line",
                    "",
                    "Another random `code` line\nUnknown text with multiple \n \n newline characters in between."
                ]
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

if __name__ == "__main__":
    unittest.main()
