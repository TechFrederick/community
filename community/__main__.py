import sys

from .build import build
from .events import fetch

operation = "build"
if len(sys.argv) > 1:
    operation = sys.argv[1]

if operation == "build":
    build()
elif operation == "events":
    fetch()
else:
    sys.exit(f"{operation} is an invalid option.")
