import orchid

orchid_training_data_path = orchid.training_data_path()
# note that you'll need to map the fiber db based on your local paths for this project
project = orchid.load_project(str(orchid_training_data_path.joinpath("HFTS2_10132022_NAD27TexasCentral_UTC_CWCinterp_wMSgrouped.ifrac")))
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
