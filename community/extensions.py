from markdown.extensions import Extension
from markdown.treeprocessors import Treeprocessor

from .frontend import tailwindify


class TailwindExtension(Extension):
    """An extension to add classes to tags to achieve the desired styling"""

    def extendMarkdown(self, md):
        md.treeprocessors.register(TailwindTreeProcessor(md), "tailwind", 20)


class TailwindTreeProcessor(Treeprocessor):
    """Walk the root node and modify any discovered tag with the desired CSS classes"""

    def run(self, root):
        tailwindify(root)
