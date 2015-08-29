__all__ = [
    'xbmc',
    'xbmcplugin',
    'xbmcgui',
    'xbmcaddon',
    'xbmcvfs'
]


class Dummy(object):
    """Literally just pretends it has
       any property/method but doesn't do anything"""
    def __getattr__(self, name):
        return Dummy()

    def __call__(self, *args, **kwargs):
        # print args, kwargs
        return Dummy()

    def __add__(self, other):
        return other


class xbmc(Dummy):
    pass


class xbmcplugin(Dummy):
    pass


class xbmcgui(Dummy):
    pass


class xbmcaddon(Dummy):
    class Addon(Dummy):
        def getSetting(self, id):
            import xml.etree.ElementTree as ET
            tree = ET.parse('../resources/settings.xml')
            root = tree.getroot()
            for setting in root.iter('setting'):
                if setting.attrib.get("id", None) == id:
                    return setting.attrib.get("default", Dummy())
            return Dummy()


class xbmcvfs(Dummy):
    pass


xbmc = xbmc()
xbmcplugin = xbmcplugin()
xbmcgui = xbmcgui()
xbmcvfs = xbmcvfs()
xbmcaddon = xbmcaddon()
