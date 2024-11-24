from xml.etree import ElementTree

classes = {
    "a": "underline text-tclightblue hover:text-tcdarkblue",
    "p": "pb-4 text-normal",
    "h2": "text-2xl pb-2",
    "ul": "list-disc px-4",
}


def tailwindify_html(html: str) -> str:
    """Given HTML, tranform all applicable nodes to have Tailwind classes.

    The provided HTML must have a root element or else ElementTree won't
    parse correctly.
    """
    # The HTML input is trusted from techcity's own build process.
    # There should be no need for defusedxml.
    try:
        root = ElementTree.fromstring(html)  # noqa: S314
        tailwindify(root)
        return ElementTree.tostring(root).decode()
    except ElementTree.ParseError:
        # TODO: This solution is not great. This is needed because the XML parser
        # is too strict for the HTML that might come in. A better solution would
        # be to use BeautifulSoup to parser the HTML better.
        return "<div>No description available.</div>"


def tailwindify(root):
    """Given an XML etree, tranform all applicable nodes to have Tailwind classes."""
    for node in root.iter():
        tag_classes = classes.get(node.tag)
        if tag_classes:
            node.attrib["class"] = tag_classes
