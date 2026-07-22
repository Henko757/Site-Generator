import os

from markdown_to_html import markdown_to_html_node


def extract_title(markdown):
    lines = markdown.split("\n")

    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()

    raise Exception("No h1 header found")


def generate_page(
    from_path,
    template_path,
    dest_path,
    basepath,
):

    print(
        f"Generating page from {from_path} "
        f"to {dest_path} "
        f"using {template_path}"
    )

    with open(from_path, "r") as file:
        markdown = file.read()

    with open(template_path, "r") as file:
        template = file.read()

    html_node = markdown_to_html_node(markdown)
    html = html_node.to_html()

    title = extract_title(markdown)

    template = template.replace(
        "{{ Title }}",
        title,
    )

    template = template.replace(
        "{{ Content }}",
        html,
    )

    template = template.replace(
        'href="/',
        f'href="{basepath}',
    )

    template = template.replace(
        'src="/',
        f'src="{basepath}',
    )

    os.makedirs(
        os.path.dirname(dest_path),
        exist_ok=True,
    )

    with open(dest_path, "w") as file:
        file.write(template)

def generate_pages_recursive(
    dir_path_content,
    template_path,
    dest_dir_path,
    basepath,
):
    for item in os.listdir(dir_path_content):

        source_path = os.path.join(
            dir_path_content,
            item,
        )

        destination_path = os.path.join(
            dest_dir_path,
            item,
        )

        if os.path.isdir(source_path):
            os.makedirs(
                destination_path,
                exist_ok=True,
            )

            generate_pages_recursive(
                source_path,
                template_path,
                destination_path,
                basepath,
            )

        else:
            if source_path.endswith(".md"):

                html_destination = (
                    os.path.splitext(
                        destination_path,
                    )[0]
                    + ".html"
                )

                generate_page(
                    source_path,
                    template_path,
                    html_destination,
                    basepath,
                )