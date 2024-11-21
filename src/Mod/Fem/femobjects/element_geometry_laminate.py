# ***************************************************************************
# *   Copyright (c) 2024 Tim Swait <timswait@gmail.com>                     *
# *                                                                         *
# *   This file is part of the FreeCAD CAx development system.              *
# *                                                                         *
# *   This program is free software; you can redistribute it and/or modify  *
# *   it under the terms of the GNU Lesser General Public License (LGPL)    *
# *   as published by the Free Software Foundation; either version 2 of     *
# *   the License, or (at your option) any later version.                   *
# *   for detail see the LICENCE text file.                                 *
# *                                                                         *
# *   This program is distributed in the hope that it will be useful,       *
# *   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
# *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
# *   GNU Library General Public License for more details.                  *
# *                                                                         *
# *   You should have received a copy of the GNU Library General Public     *
# *   License along with this program; if not, write to the Free Software   *
# *   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  *
# *   USA                                                                   *
# *                                                                         *
# ***************************************************************************

__title__ = "FreeCAD FEM element geometry laminate document object"
__author__ = "Tim Swait"
__url__ = "https://www.freecad.org"

## @package element_geometry_laminate
#  \ingroup FEM
#  \brief element geometry laminate object

from . import base_femelement


class ElementGeometryLaminate(base_femelement.BaseFemElement):
    """
    The ElementGeometryLaminate object
    """

    Type = "Fem::ElementGeometryLaminate"

    def __init__(self, obj):
        super().__init__(obj)

        obj.addProperty(
            "App::PropertyFloatList", 
            "Thicknesses", 
            "Layup",
            "List of ply thicknesses"
        )
        obj.addProperty(
            "App::PropertyFloatList", 
            "Orientations", 
            "Layup",
            "List of ply orientations (in-plane angles)"
        )
        #obj.setPropertyStatus("Layup", "LockDynamic")
