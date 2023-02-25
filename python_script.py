lyr = arcpy.mp.ArcGISProject('current').activeMap.listLayers('bigfoot')[0]
fields = arcpy.ListFields(lyr, field_type='Double')
for f in fields:
    histogram = arcpy.charts.Histogram(x=f.name, showMean=True, showMedian=True, 
        showStandardDeviation=True)
    histogram.addToLayer(lyr)