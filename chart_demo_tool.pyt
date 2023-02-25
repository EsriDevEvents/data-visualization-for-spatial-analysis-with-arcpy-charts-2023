# -*- coding: utf-8 -*-

import os
import arcpy

class Toolbox(object):

    def __init__(self):
        self.label = "Histogramify"
        self.alias = "Histogramify"

        self.tools = [
            Histogramify
        ]

class Histogramify(object):

    def __init__(self):
        self.label = "Histogramify"
        self.description = "Bulk generate histograms"
        self.canRunInBackground = False 

    def getParameterInfo(self):
        """Define parameter definitions"""

        in_data = arcpy.Parameter(
            displayName='Input Table',
            name='in_data',
            datatype=['GPFeatureLayer', 'GPTableView'],
            parameterType='Required',
            direction='Input'
        )

        double_fields = arcpy.Parameter(
           displayName='Double fields',
           name='double_fields',
           datatype='Field',
           parameterType='Required',
           direction='Input',
           multiValue=True
        )
        double_fields.filter.list = ["Double"]
        double_fields.parameterDependencies = ['in_data']

        show_mean = arcpy.Parameter(
            displayName='Show mean',
            name='show_mean',
            datatype='Boolean',
            parameterType='Optional',
            direction='Input',
            category='Overlays'  
        )

        show_median = arcpy.Parameter(
            displayName='Show median',
            name='show_median',
            datatype='Boolean',
            parameterType='Optional',
            direction='Input',
            category='Overlays'  
        )
        
        show_stdev = arcpy.Parameter(
            displayName='Show standard deviation',
            name='show_stdev',
            datatype='Boolean',
            parameterType='Optional',
            direction='Input',
            category='Overlays'  
        )

        out_data = arcpy.Parameter(
            displayName='Output Layer or Table',
            name='out_data',
            datatype=['GPFeatureLayer', 'GPTableView'],
            parameterType='Derived',
            direction="Output"
        )
        out_data.parameterDependencies = ['in_data']
        out_data.schema.clone = True

        return [
            in_data,
            double_fields,
            show_mean,
            show_median,
            show_stdev,
            out_data
        ]

    def isLicensed(self):
        return True

    def updateParameters(self, params):
        return 
        
    def updateMessages(self, params):
        return

    def execute(self, params, messages):
        """The source code of the tool."""

        # get list of selected fields
        fields = params[1].valueAsText.split(';')
        show_mean = params[2].value
        show_median = params[3].value
        show_stdev = params[4].value
        out_data = params[5]

        # list of charts
        charts = []

        # loop over fields
        for f in fields:
            histogram = arcpy.charts.Histogram(x=f, showMean=show_mean, 
                                                showMedian=show_median, showStandardDeviation=show_stdev, 
                                                title=f"{f} histogram from tool")
            charts.append(histogram)

        # add charts to the derived output layer
        out_data.charts = charts
