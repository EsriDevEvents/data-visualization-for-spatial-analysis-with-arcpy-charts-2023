"""Script demonstrating how to automate the creation and export of pie charts 
showing 2020 election vote breakdowns for each state.
"""

import arcpy

lyr = arcpy.mp.ArcGISProject('current').activeMap.listTables('election2020')[0]
# get list of unique state names
state_names = set([row[0] for row in arcpy.da.SearchCursor(lyr, 'state')])

# iterate over each state
for state in state_names:
    # set definition query to only show current state
    lyr.definitionQuery = f"state = '{state}'"
    # create pie chart showing vote proportions
    pie = arcpy.charts.Pie(numberFields=['REPUBLICAN', 'DEMOCRAT', 'OTHER'], 
                           title=state, groupingPercent=0, displaySize=(700, 700), 
                           dataSource=lyr)
    # export as svg
    pie.exportToSVG(f'c:/temp/{state}.svg')
    # reset definition query
    lyr.definitionQuery = None