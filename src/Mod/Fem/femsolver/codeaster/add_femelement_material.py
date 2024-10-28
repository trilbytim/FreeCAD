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

__title__ = "Code Aster add femelement materials"
__author__ = "Tim Swait"
__url__ = "https://www.freecad.org"

## \addtogroup FEM
#  @{


from FreeCAD import Units


def add_femelement_material(commtxt, ca_writer):

    # only use the first material object TODO allow setting multi materials
    commtxt += "# Defining materials\n"
    mat_obj = ca_writer.member.mats_linear[0]["Object"]
    YM = Units.Quantity(mat_obj.Material["YoungsModulus"])
    YM_in_MPa = YM.getValueAs("MPa").Value
    PR = float(mat_obj.Material["PoissonRatio"])
    commtxt += "{} = DEFI_MATERIAU(ELAS=_F(E={},\n".format(mat_obj.Name, YM_in_MPa)
    commtxt += "                            NU={}))\n\n".format(PR)
    
    ca_writer.fieldmats.append("fieldmat{}".format(len(ca_writer.fieldmats)))
    commtxt += "{} = AFFE_MATERIAU(identifier='4:1',\n".format(ca_writer.fieldmats[-1])
    commtxt += "                         AFFE=_F(MATER=({}, ),\n".format(mat_obj.Name)
    commtxt += "                                 TOUT='OUI'),\n"
    commtxt += "                         MAILLAGE=mesh)\n\n"

    return commtxt


##  @}
