import ckan.plugins as p

from ckanext.theming.interfaces import ITheme
from ckanext.theming.lib import Theme

from .themes.mlcommons_theming.theme import make_theme


class MLCommonsThemePlugin(p.SingletonPlugin, ITheme):
    def register_themes(self) -> list[Theme]:
        return [make_theme()]
