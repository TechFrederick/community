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

    The provided HTML must have a root element or else ElementTree won't
    parse correctly.
    """
    # The HTML input is trusted from techcity's own build process.
    # There should be no need for defusedxml.
    root = ElementTree.fromstring(html)  # noqa: S314
    tailwindify(root)
    return ElementTree.tostring(root).decode()


def tailwindify(root):
    """Given an XML etree, tranform all applicable nodes to have Tailwind classes."""
    for node in root.iter():
        tag_classes = classes.get(node.tag)
        if tag_classes:
            node.attrib["class"] = tag_classes
