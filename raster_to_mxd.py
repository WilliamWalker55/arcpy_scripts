#!/usr/bin/env python
#-*- coding: utf-8 -*-
import glob
import os
import arcpy

#Count number of files added to mxd
count = 0

#Define paths
path = r"/folder"
MXD = r"/mymap.mxd"
sourceLayer = arcpy.mapping.Layer(r"/rgb.lyr")

#Define mxd and dataframe
mxd = arcpy.mapping.MapDocument(MXD)
df = arcpy.mapping.ListDataFrames(mxd)[0]

#Iterate through folder
for file in os.listdir(path):
    if file.endswith(".tif"):
        name = file.split('.')[0]
        print name

        rasterPath =os.path.join(path, file)
        
        updatelyr = arcpy.mapping.Layer(rasterPath)
        arcpy.mapping.UpdateLayer(df, updatelyr, sourceLayer, True)
        arcpy.mapping.AddLayer(df, updatelyr, "BOTTOM")
        
        count = count + 1
           


print count
mxd.save()
