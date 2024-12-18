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

__title__ = "Code Aster add femelement geometry"
__author__ = "Tim Swait"
__url__ = "https://www.freecad.org"

## \addtogroup FEM
#  @{

import FreeCAD

def add_femelement_geometry(commtxt, ca_writer):
    matname = ca_writer.mat_objs[0].Name # Set default material name for cases where no layup is specified
    commtxt += "# Geometric properties of element\n"
    if ca_writer.member.geos_beamsection:
        FreeCAD.Console.PrintError("Beams not yet supported for Code Aster\n")
        
    elif ca_writer.member.geos_shelllaminate:
        # only use the first shelllaminate object
        shelllam_obj = ca_writer.member.geos_shelllaminate[0]["Object"]
        mat_objs = ca_writer.mat_objs
        thicknesses = shelllam_obj.Thicknesses
        orientations = shelllam_obj.Orientations
        assert len(thicknesses) == len(orientations), "{} ply thicknesses given, {} orientation angles given, these should match (i.e provide one thickness and one angle for every ply".format(len(thicknesses), len(orientations))
        materials = shelllam_obj.Materials
        if len(materials) != len(thicknesses):
            FreeCAD.Console.PrintWarning("Overwriting materials list\n")
            materials = []
            matnames = [] # TODO work out better way of naming materials without needing to reference the object, i.e. use a version of the Card Name condensed to remove spaces
            if len(ca_writer.mat_objs) == 1:
                FreeCAD.Console.PrintMessage("Single material, {}, applied to all plies\n".format(mat_objs[0].Material['CardName']))
                for i in range(len(thicknesses)):
                    materials.append(mat_objs[0].Material)
                    matnames.append(mat_objs[0].Name)
            elif len(ca_writer.mat_objs) == len(shelllam_obj.Thicknesses):
                FreeCAD.Console.PrintMessage("Multiple materials applied to each ply\n")
                for i in range(len(thicknesses)):
                    materials.append(ca_writer.mat_objs[i].Material)
                    matnames.append(mat_objs[i].Name)
            else:
                FreeCAD.Console.PrintWarning("Number of materials in analysis more than 1 but not equal to number of plies\n")
                for i in range(len(thicknesses)):
                    if i < len(ca_writer.mat_objs)-1:
                        materials.append(ca_writer.mat_objs[i].Material)
                        matnames.append(mat_objs[i].Name)
                    else:
                        materials.append(ca_writer.mat_objs[-1].Material)
                        matnames.append(mat_objs[-1].Name)

        geoms =[]
        i=0
        if len(shelllam_obj.Windall['elements']) > 0:
            print('*********************OI**********************')
            print('TODO WINDING STUFF')
            commtxt += "# WindAll object detected"
            for ref in shelllam_obj.References:
                #set default layup
                layup = {"group":ref[0].Name, "matnames":matnames, 'thicknesses':thicknesses, "orientations":orientations}
                layups = [layup]
                for e,t,o in zip(shelllam_obj.Windall['elements'],shelllam_obj.Windall['thicknesslists'],shelllam_obj.Windall['orientationlists']):
                    layup = {"group":"E"+str(e), "thicknesses":t, "orientations":o}
                    layups.append(layup)
                    commtxt += add_layup(layup["group"], layup)
                commtxt += add_grps(layups)
                commtxt += add_laminate(layups)
        else:
            for ref in shelllam_obj.References: 
            #TODO: work out how to create group of all elements and apply to that in case where len(shelllam_obj.References) == 0.
                for geom in ref[1]:
                    geoms.append(geom)
                matname = "LAYUP"+str(i)
                layup = {"group":ref[0].Name, "matnames":matnames, 'thicknesses':thicknesses, "orientations":orientations}
                i+=1
                commtxt += add_layup(matname, layup)
                commtxt += add_laminate([layup])
                ca_writer.tools.group_elements[ref[0].Name] = [g for g in geoms]
        
    elif ca_writer.member.geos_shellthickness:
        # only use the first shellthickness object
        shellth_obj = ca_writer.member.geos_shellthickness[0]["Object"]
        thickness = shellth_obj.Thickness.getValueAs("mm").Value
        geoms =[]
        i=0
        for ref in shellth_obj.References: #TODO: work out how to create group of all elements and apply to that in case where len(shellth_obj.References) == 0.
            for geom in ref[1]:
                geoms.append(geom)

            if 'YoungsModulusX' in ca_writer.mat_objs[0].Material.keys():
                matname = ca_writer.mat_objs[0].Name + "LAYUP"+str(i)
                i+=1
                commtxt += "# Orthotropic material detected, added to shell at default angle\n"
                commtxt += "{} = DEFI_COMPOSITE(COUCHE=(_F(EPAIS={},\n".format(matname, thickness)
                commtxt += "                               MATER={},\n".format(ca_writer.mat_objs[0].Name)
                commtxt += "                               ORIENTATION = 0)))\n\n"
                
            commtxt += "# Shell elements detected, thickness {}mm on item {}\n".format(thickness, (ref[0].Name,geom))
            commtxt += "elemprop = AFFE_CARA_ELEM(COQUE=_F(EPAIS={},\n".format(thickness)
            commtxt += "                                   GROUP_MA=('{}', )),\n".format(ref[0].Name)
            commtxt += "                          MODELE=model)\n\n"
                
        
            ca_writer.tools.group_elements[ref[0].Name] = [g for g in geoms]
        FreeCAD.Console.PrintMessage("Shell of thickness {}mm added.\n".format(thickness))
        
    return commtxt, matname
    
def add_grps(layups):
    commtxt = "# Adding WindAll groups"
    commtxt += "grps = DEFI_GROUP(MAILLAGE=mesh, CREA_GROUP_MA = (\n"
    for layup in layups[1:]:
        commtxt += "                                                  _F(GROUP_MA = ({},),\n".format(layups[0]["group"])
        commtxt += "                                                     NUME_INIT = {},\n".format(layup["group"][1:])
        commtxt += "                                                     NUME_FIN = {}\n,".format(layup["group"][1:])
        commtxt += "                                                     NOM = '{}'),\n".format(layup["group"])
    commtxt += "                                                     ))"

def add_layup(LUname, layup):
    thicknesses, orientations, matnames = layup["thicknesses"], layup["orientations"], layup["matnames"]
    commtxt = "# Composite layup detected, added to shell\n"
    commtxt += "{} = DEFI_COMPOSITE(COUCHE=(\n".format(LUname)
    for j in range(len(thicknesses)):
        commtxt += "                               _F(EPAIS={},\n".format(thicknesses[j])
        commtxt += "                                MATER={},\n".format(matnames[j])
        commtxt += "                                ORIENTATION = {}),\n".format(orientations[j])
    commtxt += "                                ))\n\n"
    return commtxt
    
def add_laminate(layups):
    commtxt = "# Shell elements detected, applying composite laminate definition\n"
    commtxt += "elemprop = AFFE_CARA_ELEM(COQUE="
    for layup in layups:
        thicknesses, group = layup["thicknesses"], layup["group"]
        thicktot = sum(thicknesses)
        commtxt += "                                _F(COQUE_NCOU = {},\n".format(len(thicknesses))
        commtxt += "                                   EPAIS={},\n".format(thicktot)
        commtxt += "                                   GROUP_MA=('{}', ),\n".format(group)
        commtxt += "                                   VECTEUR=(1.0, 0.0, 0.0)),\n"
    commtxt += "                          MODELE=model)\n\n"
    return commtxt
##  @}
