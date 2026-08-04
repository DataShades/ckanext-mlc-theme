import ckan.plugins.toolkit as tk


def get_homepage_counts() -> dict[str, int]:
    packages = tk.get_action("package_search")({}, {"rows": 0})["count"]
    orgs = tk.h.organizations_available("read")
    groups = tk.h.groups_available("read")

    return {
        "packages": packages,
        "orgs": len(orgs),
        "groups": len(groups),
    }
