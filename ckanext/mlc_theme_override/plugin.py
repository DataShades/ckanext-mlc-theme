import ckan.plugins as p
from ckan.common import CKANConfig


class MLCommonsThemeOverridePlugin(p.SingletonPlugin):
    """MLC theme extension override.

    This plugin provides an ovveride for various extension templates
    to be consistent with the MLC theme.

    A theme must be enabled first to work properly, therefore
    it cannot be used to ovveride other extensions templates.
    """

    p.implements(p.IConfigurer)

    def update_config(self, config: CKANConfig):
        p.toolkit.add_template_directory(config, "templates")
