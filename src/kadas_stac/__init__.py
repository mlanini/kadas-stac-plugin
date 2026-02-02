# -*- coding: utf-8 -*-
"""
/***************************************************************************
 KadasStac

 A KADAS plugin that provides support for accessing STAC APIs inside KADAS
 Albireo 2. Also compatible with QGIS 3.x applications.
 
 Adapted for KADAS from the original QGIS STAC Plugin by Kartoza.
 Original work: https://github.com/stac-utils/qgis-stac-plugin
                             -------------------
        begin                : 2021-11-15
        original copyright   : (C) 2021-2024 by Kartoza
        kadas adaptation     : (C) 2026 by Michael Lanini
        email                : mlanini@proton.me
        git sha              : $Format:%H$
 ***************************************************************************/
/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to KADAS and QGIS.
"""
import os
import sys

LIB_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), 'lib'))
if LIB_DIR not in sys.path:
    sys.path.append(LIB_DIR)


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load KadasStac class from file main.
    
    :param iface: A KADAS/QGIS interface instance.
    :type iface: QgsInterface or KadasPluginInterface
    """
    #
    from .main import KadasStac

    return KadasStac(iface)
