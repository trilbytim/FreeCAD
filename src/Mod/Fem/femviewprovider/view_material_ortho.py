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

__title__ = "FreeCAD FEM material orthotropic ViewProvider for the document object"
__author__ = "Tim Swait"
__url__ = "https://www.freecad.org"

## @package view_material_reinforced
#  \ingroup FEM
#  \brief view provider for orthotropic material object

from femtaskpanels import task_material_ortho
from . import view_base_femmaterial


class VPMaterialOrtho(view_base_femmaterial.VPBaseFemMaterial):
    """
    A View Provider for the MaterialOrtho object
    """

    def setEdit(self, vobj, mode=0):
        super().setEdit(vobj, mode, task_material_ortho._TaskPanel)
