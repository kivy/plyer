from plyer.facades import Systray
from os.path import dirname, join
from Foundation import (NSUserNotification, NSUserNotificationCenter, NSDate, NSTimer, NSRunLoop, NSDefaultRunLoopMode,
                        NSSearchPathForDirectoriesInDomains, NSMakeRect, NSLog, NSObject)
from AppKit import NSApplication, NSStatusBar, NSMenu, NSMenuItem, NSAlert, NSTextField, NSImage
from PyObjCTools import AppHelper


def _nsimage_from_file(filename, dimensions=None):
    """
    Takes a path to an image file and returns an NSImage object.
    """
    try:
        with open(filename):
            pass
    except IOError:  # literal file path didn't work -- try to locate image based on main script path
        try:
            from __main__ import __file__ as main_script_path
            main_script_path = dirname(main_script_path)
            filename = join(main_script_path, filename)
        except ImportError:
            pass
        with open(filename):
            pass
    image = NSImage.alloc().initByReferencingFile_(filename)
    image.setScalesWhenResized_(True)
    image.setSize_((20, 20) if dimensions is None else dimensions)
    return image


class NSApp(NSObject):

    def build_statusbar(self):
        if not hasattr(self, 'nsstatusitem'):
            self.nsstatusitem = NSStatusBar.systemStatusBar().statusItemWithLength_(-1)
            self.nsstatusitem.setHighlightMode_(True)

            if self._app._icon is not None:
                self.set_statusbar_icon()
                if self._app._title is not None:
                    self.set_statusbar_title()
            else:
                self.set_statusbar_title()

        self._holders = []
        menu = self._build_menu(None, self._app._menu_options)
        #mainmenu.add('Quit')
        #mainmenu['Quit']._menuitem.setAction_('terminate:') 
        self.nsstatusitem.setMenu_(menu)

    def set_statusbar_title(self):
        self.nsstatusitem.setTitle_(self._app._title or '')

    def set_statusbar_icon(self):
        self.nsstatusitem.setImage_(_nsimage_from_file(self._app._icon))

    def _build_menu(self, menu, options):

        if menu is None:
            menu = NSMenu.alloc().init()

        for text, icon, action in options:

            menuitem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
                    text, None, '')
            if icon:
                menuitem.setImage_(_nsimage_from_file(icon, None))

            if isinstance(action, (list, tuple)):
                submenu = self._build_menu(None, action)
                menuitem.setSubmenu_(submenu)
            else:
                holder = MenuItemCallback.alloc().init()
                holder._action = action
                self._holders.append(holder)
                menuitem.setAction_('callback:')
                menuitem.setTarget_(holder)

            menu.addItem_(menuitem)

        return menu


class MenuItemCallback(NSObject):
    def callback_(self, _):
        return self._action()


class OSXSystray(Systray):

    def _run(self):
        # initialize unused component (but might be useful to integrate them
        # later)
        self._title = None
        self._nsapplication = nsapplication = NSApplication.sharedApplication()
        nsapplication.activateIgnoringOtherApps_(True)  # NSAlerts in front
        self._nsapp = NSApp.alloc().init()
        self._nsapp._app = self
        self._nsapp.build_statusbar()
        nsapplication.setDelegate_(self._nsapp)
        NSUserNotificationCenter.defaultUserNotificationCenter().setDelegate_(self._nsapp)

        AppHelper.runEventLoop()

    def _configure(self):
        if hasattr(self, '_nsapp'):
            self._nsapp.build_statusbar()

    def _quit(self):
        self._nsapplication.terminate_(self._nsapp)


def instance():
    return OSXSystray()
