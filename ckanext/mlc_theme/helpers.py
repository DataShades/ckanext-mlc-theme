from cachetools import TTLCache, cached

import ckan.plugins.toolkit as tk
from ckan import model


@cached(cache=TTLCache(maxsize=256, ttl=600))
def get_homepage_counts(user: str) -> dict[str, int]:
    packages = tk.get_action("package_search")(
        {"user": user}, {"rows": 0, "include_private": True}
    )["count"]

    return {
        "packages": packages,
        "orgs": _get_groups_count(is_org=True),
        "groups": _get_groups_count(),
    }


def _get_groups_count(is_org: bool = False) -> int:
    return (
        model.Session.query(model.Group.id)
        .filter_by(is_organization=is_org, state=model.State.ACTIVE)
        .count()
    )
