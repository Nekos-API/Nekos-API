import tomllib


def get_project_version():
    pyproject_path = "pyproject.toml"

    with open(pyproject_path, "rb") as f:
        data = tomllib.load(f)

    # Standard location for project metadata under PEP 621
    return data.get("project", {}).get("version")
