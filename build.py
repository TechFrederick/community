from jinja2 import Environment, FileSystemLoader


def main():
    environment = Environment(loader=FileSystemLoader("templates"))
    print("Generating content to `out` directory")
    template = environment.get_template("group.html")


if __name__ == "__main__":
    main()
