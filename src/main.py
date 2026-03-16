from textnode import TextNode, TextType

def main():
    dummy_node = TextNode("This is img alt text", TextType.BOLD, "#dummy_url")
    print(dummy_node)

main()

