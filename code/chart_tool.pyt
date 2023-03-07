"""Script tool demonstrating how to include charts in a GP tool output. 
"""

import os
import arcpy

class Toolbox(object):

    def __init__(self):
        self.label = "CreateMovingAverageCharts"
        self.alias = "CreateMovingAverageCharts"

        self.tools = [
            CreateMovingAverageCharts
        ]

class CreateMovingAverageCharts(object):

    def __init__(self):
        self.label = "CreateMovingAverageCharts"
        self.description = "Create moving average charts"
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

        date_field = arcpy.Parameter(
           displayName='Date field',
           name='date_field',
           datatype='Field',
           parameterType='Required',
           direction='Input',
        )
        date_field.filter.list = ['Date']
        date_field.parameterDependencies = ['in_data']

        numeric_field = arcpy.Parameter(
            displayName='Numeric field',
            name='numeric_field',
            datatype='Field',
            parameterType='Required',
            direction='Input',
        )
        numeric_field.filter.list = ['Short', 'Long', 'Double']
        numeric_field.parameterDependencies = ['in_data']

        aggregation = arcpy.Parameter(
            displayName='Aggregation',
            name='aggregation',
            datatype='GPString',
            parameterType='Required',
            direction='Input',
        )
        aggregation.filter.type = 'ValueList'
        aggregation.filter.list = ['None', 'Count', 'Sum', 'Mean', 'Median', 'Min', 'Max']

        day_windows = arcpy.Parameter(
            displayName='Moving Average Windows (Days)',
            name='day_windows',
            datatype='GPString',
            parameterType='Required',
            direction='Input',
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
            date_field,
            numeric_field,
            aggregation,
            day_windows,
            out_data
        ]

    def isLicensed(self):
        return True

    def updateParameters(self, params):
        return 
        
    def updateMessages(self, params):
        return

    def execute(self, params, messages):
        """Create a bar chart for each moving average window specified 
        and add all charts to the output.
        """

        date_field = params[1].valueAsText
        numeric_field = params[2].valueAsText
        aggregation = params[3].valueAsText
        day_windows = params[4].valueAsText
        out_data = params[5]

        # list of charts
        charts = []

        # loop over list of moving average windows
        for window in day_windows.split(','):
            window_int = int(window)

            # create bar chart with window 
            bar = arcpy.charts.Bar(x=date_field, y=numeric_field, aggregation=aggregation,
                                   showMovingAverage=True, movingAveragePeriod=window_int,
                                   title=f"{aggregation.title()} of {numeric_field} By Date ({window_int} day window)",
                                   xTitle='Date', yTitle='New Cases')
            charts.append(bar)

        # add charts to the derived output layer
        out_data.charts = charts