#!/usr/bin/env python
#-*- coding: utf-8 -*-
import arcpy, os
from arcpy import env
arcpy.env.overwriteOutput = True



#Define inputs
byggnader = 'D:/projekt_byggarea/data/bygg_area.gdb/by_1286'
fastigheter = 'D:/projekt_byggarea/data/bygg_area.gdb/ay_1286'



arcpy.env.outputCoordinateSystem = arcpy.Describe(fastigheter).spatialReference

#Define field names
Bebyggd = "Bebyggd"
fast_objID = "OBJECTID"
fast_area = "Shape_Area"
bygg_area = "Shape_Area"
bygg_objID = "OBJECTID"

count = 0



# Set local variables
byggnad_clip = "in_memory/byygnad_clip"
properties = "AREA"
length_unit = ""
area_unit = "SQUARE_METERS"
coordinate_system = ""

#Make feature layer of byggnader
arcpy.MakeFeatureLayer_management(byggnader, "byggnad_Layer")

arcpy.AddField_management(fastigheter, Bebyggd, "FLOAT")

with arcpy.da.UpdateCursor(fastigheter, (fast_objID,fast_area,Bebyggd)) as cursor:
    
    for row in cursor:
        area_list = []
        fastID = row[0]
        if fastID in range(0,6959):
            continue
        else:
            f_area = row[1]
            print fastID
            print f_area

            #Create expression to fastighet
            expression = '"' + (fast_objID) + '" =' + str(fastID)
            #print expression

            
            #Create feature layer of current fastighet
            arcpy.MakeFeatureLayer_management(fastigheter, "fast_Layer", expression)

            arcpy.Clip_analysis(byggnader,"fast_Layer",byggnad_clip)

            arcpy.AddGeometryAttributes_management(byggnad_clip, properties, length_unit,
                                                                  area_unit,
                                                                  coordinate_system)

            #fields = arcpy.ListFields(byggnad_clip)
            #for field in fields:
                #print("{0} is a type of {1} with a length of {2}"
                    #.format(field.name, field.type, field.length))
       
            byggnad_count = int(arcpy.GetCount_management(byggnad_clip).getOutput(0))
            print "byggnad count", byggnad_count


            
                
            with arcpy.da.SearchCursor(byggnad_clip, (bygg_objID, "POLY_AREA")) as cursor1:
                for row1 in cursor1:
                    if byggnad_count >= 1:
                        byggnadID = row1[0]
                        #print byggnadID
                        byggnad_area = row1[1]
                        area_list.append(byggnad_area)

                    elif byggnad_count<1:
                        byggnad_area = 0
                        area_list.append(byggnad_area)
                        row.bebyggd= perc
                        count = count +1

            total_area = sum(area_list)
            print "Total", total_area
            perc = (total_area/f_area)*100
            print perc, "%"
            row[2]= perc
            cursor.updateRow(row)
            count = count +1

      
            
            
                    
                    
            arcpy.Delete_management(byggnad_clip)
            arcpy.Delete_management("fast_Layer")

print count

