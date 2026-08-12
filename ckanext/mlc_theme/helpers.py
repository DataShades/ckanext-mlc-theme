from typing import Any

from cachetools import TTLCache, cached

import ckan.plugins.toolkit as tk
from ckan import model, types


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


@cached(cache=TTLCache(maxsize=256, ttl=600))
def mlc_get_featured_groups(user: str, count: int = 1) -> list[dict[str, Any]]:
    """Return a list of featured groups with dataset counter."""
    config_groups = tk.config.get("ckan.featured_groups")
    return _featured_group_org(
        user=user,
        count=count,
        items=config_groups,
    )


def _featured_group_org(
    items: list[str], user: str, count: int
) -> list[dict[str, Any]]:
    groups_data = []

    extras = tk.get_action("group_list")({}, {"limit": count})

    found = []

    for group_name in items + extras:
        group = _get_group(group_name, user=user)

        if not group:
            continue

        if group["id"] in found:
            continue

        found.append(group["id"])
        groups_data.append(group)

    return groups_data


def _get_group(group_id: str, user: str) -> dict[str, Any] | None:
    try:
        out = tk.get_action("group_show")(
            types.Context(
                ignore_auth=True,
                for_view=True,
            ),
            {
                "id": group_id,
                "include_datasets": False,
                "include_dataset_count": True,
                "include_extras": False,
                "include_users": False,
                "include_groups": False,
                "include_followers": False,
            },
        )
    except tk.ObjectNotFound:
        return None

    if not out.get("is_organization"):
        out["package_count"] = tk.get_action("package_search")(
            types.Context(user=user),
            {
                "fq": f'+groups:"{out["name"]}"',
                "include_private": True,
                "rows": 0,
            },
        )["count"]

    return out
