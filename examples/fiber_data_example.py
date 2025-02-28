import orchid
from orchid.project_store import as_python_time_series_arrays

project = orchid.load_project("/example/HFTS2_10132022_NAD27TexasCentral_UTC_CWCinterp_wMSgrouped.ifrac")
all_well_names = list(project.wells().all_names())

fiber_data = project.fiber_data()[3]
data_set = fiber_data.get_data_set()
# Reconstructing the data table from the data_set, dates and depths
data_set.columns = fiber_data.dates
data_set.insert(0, "Depths", fiber_data.depths)
# Getting the data table which takes few minutes if you don't specify start and/or end indexes
data_table = fiber_data.get_data_table()

name = fiber_data.name
depth_unit = fiber_data.depth_unit
