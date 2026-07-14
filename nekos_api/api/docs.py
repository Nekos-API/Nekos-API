import os


OPENAPI_TAGS = []

OPENAPI_DESCRIPTION = ""


for doc_file in os.listdir("./docs"):
    if not doc_file.endswith(".md"):
        continue

    with open(f"./docs/{doc_file}", "r", encoding="utf-8") as f:
        content = f.read()

        name = doc_file.split(".")[0]

        if name == "_Project":
            OPENAPI_DESCRIPTION = content

        else:
            OPENAPI_TAGS.append(
                {
                    "name": name,
                    "description": content,
                }
            )
