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

__title__ = "Code Aster add force constraint"
__author__ = "Tim Swait"
__url__ = "https://www.freecad.org"

## \addtogroup FEM
#  @{
import FreeCAD
import Part

def add_con_force(commtxt, ca_writer):
    commtxt += "# Adding force loads\n"
    geoms = []
    for i, femobj in enumerate(ca_writer.member.cons_force):
        force_obj = femobj["Object"]
        dirvec = femobj["Object"].DirectionVector
        F = force_obj.Force.getValueAs('N')
        dirvec.normalize()
        #Need to divide force across length, number of points or area as appropriate
        force_entities = []
        for ref in force_obj.References:
	        for r in ref[1]:
		        o = getattr(ref[0].Shape, r)
		        force_entities.append(o)
        tot = 0
        for o in force_entities:
	        if type(o) == Part.Vertex:
		        tot += 1
	        elif type(o) == Part.Edge:
		        tot += o.Length
	        elif type(o) == Part.Face:
		        tot += o.Area
        
        txt = "Force load: {} on: {} of: {} at: {} spread across: {} Vertices, length or area\n".format(i,force_obj.Name, F,dirvec,tot)
        FreeCAD.Console.PrintMessage(txt)
        commtxt += '#'+txt
        
        F /= tot
        for ref in force_obj.References:
            for geom in ref[1]:
                geoms.append(geom)
            ca_writer.forces.append("force{}".format(len(ca_writer.forces)))
            commtxt += "{} = AFFE_CHAR_MECA(FORCE_ARETE=_F(FX={},\n".format(ca_writer.forces[0],F * dirvec.x)
            commtxt += "                                     FY={},\n".format(F * dirvec.y)
            commtxt += "                                     FZ={},\n".format(F * dirvec.z)
            commtxt += "                                     GROUP_MA=('{}', )),\n".format(force_obj.Name)
            commtxt += "                      MODELE=model)\n\n"
        
        ca_writer.tools.group_elements[force_obj.Name] = [g for g in geoms]
    return commtxt

##  @}
