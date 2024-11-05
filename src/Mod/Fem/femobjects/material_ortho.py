# ***************************************************************************
# *   Copyright (c) 2024 Tim Swait <timswait@gmail.com                      *
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

__title__ = "FreeCAD FEM orthotropic material"
__author__ = "Tim Swait"
__url__ = "https://www.freecad.org"

## @package material_ortho
#  \ingroup FEM
#  \brief orthotropic object

from . import material_common


class MaterialOrtho(material_common.MaterialCommon):
    """
    The MaterialOrtho object
    """

    Type = "Fem::MaterialOrtho"

    def __init__(self, obj):
        super().__init__(obj)

        obj.addProperty(
            type = 'App::PropertyStiffness', name = 'EL', group = 'Orthotropic properties', doc = 'Longitudinal Modulus'
        )
        obj.addProperty(
            type = 'App::PropertyStiffness', name = 'ET', group = 'Orthotropic properties', doc = 'Transverse Modulus'
        )

        obj.Category = ["Solid"]
