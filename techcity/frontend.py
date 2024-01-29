from xml.etree import ElementTree

classes = {
    "a": "underline text-tflightblue hover:text-tfdarkblue",
    "p": "pb-4 text-normal",
    # TODO: Fix the heading styles when a group uses that in the description.
    "h1": "text-lg",
    "h2": "text-lg",
}


def tailwindify_html(html: str) -> str:
    """Given HTML, tranform all applicable nodes to have Tailwind classes.

    The provided HTML must have a root element or else ElementTree won't parse correctly.
    """
    root = ElementTree.fromstring(html)
    tailwindify(root)
    return ElementTree.tostring(root).decode()


def tailwindify(root):
    """Given an XML element tree, tranform all applicable nodes to have Tailwind classes."""
    for node in root.iter():
        tag_classes = classes.get(node.tag)
        if tag_classes:
            node.attrib["class"] = tag_classes
