# ***************************************************************************
# *   Copyright (c) 2024 Tim Swait <timswait@gmail.com>              *
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

__title__ = "Code Aster add femelement geometry"
__author__ = "Tim Swait"
__url__ = "https://www.freecad.org"

## \addtogroup FEM
#  @{

def add_femelement_geometry(commtxt, ca_writer):
    commtxt += "# Geometric properties of element\n"
    if ca_writer.member.geos_beamsection:
        FreeCAD.Console.PrintMessage("Beams not yet supported for Code Aster")
    elif ca_writer.member.geos_shellthickness:
        # only use the first shellthickness object
        shellth_obj = ca_writer.member.geos_shellthickness[0]["Object"]
        thickness = shellth_obj.Thickness.getValueAs("mm").Value
        geoms =[]
        for ref in shellth_obj.References: #TODO: work out how to create group of all elements and apply to that in case where len(shellth_obj.References) == 0.
            for geom in ref[1]:
                commtxt += "# Shell elements detected, thickness {}mm on item {}\n".format(thickness, (ref,geom))
                commtxt += "elemprop = AFFE_CARA_ELEM(identifier='2:1',\n"
                commtxt += "                          COQUE=_F(EPAIS={},\n".format(thickness)
                commtxt += "                                   GROUP_MA=('{}', )),\n".format(geom)
                commtxt += "                          MODELE=model)\n\n"
                geoms.append(geom)
        
        ca_writer.tools.group_elements = {g: [g] for g in geoms}

    return commtxt

##  @}
