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
noll = 0

#Add attribute to property feature class
arcpy.AddField_management(fastigheter, Bebyggd, "FLOAT")


#Make feature layer of buildings and properties
arcpy.MakeFeatureLayer_management(byggnader, "byggnad_Layer")
arcpy.MakeFeatureLayer_management(fastigheter, "fast_Layer")


#Select properties with buildning polygons, reverse selection to find properties that contain no buildings
fast_bygg_Layer = arcpy.SelectLayerByLocation_management("fast_Layer", 'intersect', "byggnad_Layer", "", "", "INVERT")

#Count number of properties that don't contain buiildings
fast_count = int(arcpy.GetCount_management("fast_Layer").getOutput(0))
print "fastighet count", fast_count

#Fill all properties with no buildings with 0 (%)
arcpy.CalculateField_management("fast_Layer",Bebyggd,int(noll))

#Delete feature layers
arcpy.Delete_management("byggnad_Layer")
arcpy.Delete_management("fast_Layer")

#Iterate through properties
with arcpy.da.UpdateCursor(fastigheter, (fast_objID,fast_area,Bebyggd)) as cursor:
    
    for row in cursor:
        area_list = []
        fastID = row[0]
        byggnad = row[2]

        #For restart
        if fastID in range(0,10093):
            continue

        #Skip properties with no buildings
        elif byggnad == 0:
            continue
        else:
            f_area = row[1]
            print fastID
            print f_area

            #Create expression for property
            expression = '"' + (fast_objID) + '" =' + str(fastID)
            #print expression

            
            #Create feature layer of current property
            arcpy.MakeFeatureLayer_management(fastigheter, "fast_Layer1", expression)

            #Ckip buildings with property
            arcpy.Clip_analysis(byggnader,"fast_Layer1",byggnad_clip)

            #Add geometry attribute to clipped building
            arcpy.AddGeometryAttributes_management(byggnad_clip, properties, length_unit,
                                                                  area_unit,
                                                                  coordinate_system)

         
           #Count number of buildings
            byggnad_count = int(arcpy.GetCount_management(byggnad_clip).getOutput(0))
            print "byggnad count", byggnad_count


            
            #Iterate through clipped buildings     
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

            #Calculate total building area
            total_area = sum(area_list)
            print "Total", total_area

            #calculate building area as percentage of property
            perc = (total_area/f_area)*100
            print perc, "%"
            row[2]= perc
            cursor.updateRow(row)
            count = count +1
                    
            #Delete clipped fc and property layer   
            arcpy.Delete_management(byggnad_clip)
            arcpy.Delete_management("fast_Layer1")

print count

