from markdown.extensions import Extension
from markdown.treeprocessors import Treeprocessor


class TailwindExtension(Extension):
    """An extension to add classes to tags to achieve the desired styling"""

    def extendMarkdown(self, md):
        md.treeprocessors.register(TailwindTreeProcessor(md), "tailwind", 20)


class TailwindTreeProcessor(Treeprocessor):
    """Walk the root node and modify any discovered tag with the desired CSS classes"""

    classes = {
        "a": "underline text-tflightblue hover:text-tfdarkblue",
        "p": "pb-4 text-normal",
        # TODO: Fix the heading styles when a group uses that in the description.
        "h1": "text-lg",
        "h2": "text-lg",
    }

    def run(self, root):
        for node in root.iter():
            tag_classes = self.classes.get(node.tag)
            if tag_classes:
                node.attrib["class"] = tag_classes
