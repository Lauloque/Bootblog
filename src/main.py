from textnode import TextNode, TextType

print("hello world")


def main():
    my_node = TextNode(
        "This is some anchor text", TextType.LINK, "https://www.boot.dev"
    )

    print(my_node)


if __name__ == "__main__":
    main()
