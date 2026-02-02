"""
/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import re
import os.path
import subprocess
import sys

from qgis.core import QgsSettings
from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication, Qt
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction, QDockWidget, QMenu, QMessageBox

# Try to import Kadas-specific interface
try:
    from kadas.kadasgui import KadasPluginInterface
    KADAS_AVAILABLE = True
except ImportError:
    KADAS_AVAILABLE = False

# Initialize Qt resources from file resources.py
# Note: resources.py must be generated from resources.qrc using pyrcc5
try:
    from .resources import *
except ImportError:
    pass  # resources.py not yet compiled, will be generated during plugin build

from .gui.kadas_stac_widget import KadasStacWidget
from .conf import settings_manager
from .utils import config_defaults_catalogs, open_documentation
from .logger import get_logger


class KadasStacDockWidget(QDockWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("STAC API Browser")
        self.widget = KadasStacWidget(self)
        self.setWidget(self.widget)
        
        # Set allowed dock areas (left and right only)
        self.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        
        # Set minimum and default size for the dock widget
        self.setMinimumSize(400, 500)
        self.resize(450, 700)


class KadasStac:
    """KADAS STAC API Plugin Implementation."""

    def __init__(self, iface):
        # Cast to KadasPluginInterface if available (Kadas Albireo 2)
        if KADAS_AVAILABLE:
            self.iface = KadasPluginInterface.cast(iface)
        else:
            self.iface = iface
            
        self.plugin_dir = os.path.dirname(__file__)
        
        # Initialize logger - set desired log level: "STANDARD", "DEBUG", "ERRORS"
        self.log = get_logger(level="STANDARD")
        self.log.info("KADAS STAC Plugin - Logger initialized (level: STANDARD)")
        
        locale = QgsSettings().value("locale/userLocale")[0:2]
        locale_path = os.path.join(
            self.plugin_dir, "i18n", "KadasStac_{}.qm".format(locale)
        )

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)
            self.log.debug(f"Loaded translation: {locale_path}")

        # Declare instance attributes
        self.actions = []
        self.menu = QMenu(self.tr(u"STAC API Browser"))
        self.pluginIsActive = False
        self.dock_widget = None
        
        # Create toolbar (may be None in Kadas)
        self.toolbar = self.iface.addToolBar("KADAS STAC API Browser")
        if self.toolbar is not None:
            self.toolbar.setObjectName("KadasStac")

        # Add default catalogs (will only add new ones if they don't exist)
        config_defaults_catalogs()

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.
        We implement this ourselves since we do not inherit QObject.
        :param message: String for translation.
        :type message: str, QString
        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate("KadasStac", message)

    def add_action(
            self,
            icon_path,
            text,
            callback,
            enabled_flag=True,
            add_to_menu=True,
            add_to_web_menu=True,
            add_to_toolbar=True,
            status_tip=None,
            whats_this=None,
            parent=None,
            checkable=False,
    ):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_web_menu: Flag indicating whether the action
            should also be added to the web menu. Defaults to True.
        :type add_to_web_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :param checkable: Whether the action should be checkable.
        :type checkable: bool

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path) if icon_path else QIcon()
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)
        action.setCheckable(checkable)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_menu:
            self.menu.addAction(action)

        if add_to_toolbar and self.toolbar is not None:
            self.toolbar.addAction(action)

        self.actions.append(action)

        return action
    
    def open_log_window(self):
        """Open the log file with system's default text editor."""
        log_path = os.environ.get('KADAS_STAC_LOG', os.path.expanduser('~/.kadas/stac.log'))
        try:
            if sys.platform.startswith('win'):
                os.startfile(log_path)
            elif sys.platform.startswith('darwin'):
                subprocess.Popen(['open', log_path])
            else:
                subprocess.Popen(['xdg-open', log_path])
            self.log.info(f"Opening log file: {log_path}")
        except Exception as e:
            self.log.error(f"Failed to open log file: {e}", exc_info=True)
            QMessageBox.warning(
                self.iface.mainWindow(),
                "Error Opening Log",
                f"Could not open log file:\n{e}\n\nLog location: {log_path}"
            )

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""
        self.log.info("Initializing GUI")
        icon_path = ":/plugins/kadas_stac/icon.png"
        
        # Main action to open STAC browser (checkable for dock widget)
        self.main_action = self.add_action(
            icon_path,
            text=self.tr(u"STAC API Browser"),
            callback=self.run,
            status_tip=self.tr(u"Toggle STAC API Browser Panel"),
            parent=self.iface.mainWindow(),
            checkable=True,
        )

        # Documentation action
        self.add_action(
            None,
            text=self.tr(u"Documentation"),
            callback=open_documentation,
            parent=self.iface.mainWindow(),
            add_to_toolbar=False,
        )
        
        # Log window opener
        self.add_action(
            None,
            text=self.tr(u"Open Log File"),
            callback=self.open_log_window,
            parent=self.iface.mainWindow(),
            add_to_toolbar=False,
            status_tip=self.tr(u"View plugin log file"),
        )

        # Register menu with Kadas interface or fallback to QGIS standard
        if KADAS_AVAILABLE:
            # Create custom "STAC" ribbon tab in Kadas
            self.log.info("Registering menu in Kadas custom ribbon tab 'STAC'")
            self.iface.addActionMenu(
                self.tr(u"STAC API Browser"),
                QIcon(icon_path),
                self.menu,
                self.iface.PLUGIN_MENU,
                self.iface.CUSTOM_TAB,
                "STAC"
            )
        else:
            # Fallback: use standard QGIS plugin menu
            self.log.info("Registering menu in standard QGIS plugin menu")
            for action in self.actions:
                self.iface.addPluginToMenu(
                    self.tr(u"&STAC API Browser"),
                    action
                )
                self.iface.addPluginToWebMenu(
                    self.tr(u"&STAC API Browser"),
                    action
                )
        
        self.log.info("GUI initialized successfully")

    def onClosePlugin(self):
        """Cleanup necessary items here when plugin widget is closed"""
        self.log.debug("Closing plugin panel")
        if self.dock_widget is not None:
            self.iface.mainWindow().removeDockWidget(self.dock_widget)
            self.dock_widget = None
        if hasattr(self, 'main_action') and self.main_action:
            self.main_action.setChecked(False)
        self.pluginIsActive = False

    def unload(self):
        """Removes the plugin menu item, icon, and dock widget from QGIS GUI."""
        self.log.info("Unloading plugin")
        if self.dock_widget is not None:
            self.iface.mainWindow().removeDockWidget(self.dock_widget)
            self.dock_widget = None
            
        # Remove menu based on which interface is used
        if KADAS_AVAILABLE:
            # Remove custom ribbon tab menu
            if self.menu:
                self.iface.removeActionMenu(
                    self.menu,
                    self.iface.PLUGIN_MENU,
                    self.iface.CUSTOM_TAB,
                    "STAC"
                )
                self.menu = None
        else:
            # Remove standard QGIS plugin menu entries
            for action in self.actions:
                self.iface.removePluginMenu(
                    self.tr(u"&STAC API Browser"),
                    action
                )
                self.iface.removePluginWebMenu(
                    self.tr(u"&STAC API Browser"),
                    action
                )
                self.iface.removeToolBarIcon(action)
        
        # Clear actions
        for action in self.actions:
            if action:
                action.triggered.disconnect()
        self.actions.clear()
        
        self.log.info("Plugin unloaded successfully")

    def run(self):
        """Run method that creates and shows the dock widget"""
        self.log.debug("Run method called")
        
        # Note: Proxy/SSL configuration is now handled automatically by QgisStacApiIO
        # which uses QGIS QgsNetworkAccessManager (respects QGIS proxy settings)
        
        if self.dock_widget is None:
            # First time: create dock widget, add it to right side, and show it
            try:
                self.log.info("Creating dock widget for first time")
                self.dock_widget = KadasStacDockWidget(self.iface.mainWindow())
                self.dock_widget.setObjectName("KadasStacDock")
                self.dock_widget.visibilityChanged.connect(self._on_visibility_changed)
                # Add as dock widget to main window (ensures proper docking)
                self.iface.mainWindow().addDockWidget(Qt.RightDockWidgetArea, self.dock_widget)
                self.dock_widget.show()
                self.dock_widget.raise_()
                self.pluginIsActive = True
                self.log.info("Dock widget created and shown successfully")
                return  # Exit after first creation
            except Exception as e:
                self.log.critical(f"Failed to create dock widget: {e}", exc_info=True)
                QMessageBox.critical(
                    self.iface.mainWindow(),
                    "Error",
                    f"Failed to create STAC API Browser panel:\n{str(e)}"
                )
                if hasattr(self, 'main_action') and self.main_action:
                    self.main_action.setChecked(False)
                return
        
        # Toggle visibility on subsequent calls
        if self.dock_widget.isVisible():
            self.log.debug("Hiding dock widget")
            self.dock_widget.hide()
        else:
            self.log.debug("Showing dock widget")
            self.dock_widget.show()
            self.dock_widget.raise_()

    def _on_visibility_changed(self, visible):
        """Sync main action checked state with dock widget visibility"""
        if hasattr(self, 'main_action') and self.main_action:
            self.main_action.setChecked(visible)
