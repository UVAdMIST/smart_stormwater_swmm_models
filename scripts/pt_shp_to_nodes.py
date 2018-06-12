import numpy as np
from swmmio import swmmio
from swmmio.utils.modify_model import replace_inp_section
from get_contributing_area import get_upstream_nodes, get_upstream_conduits
import pandas as pd
from shutil import copyfile

def make_new_df(index, cols, data):
    df = pd.DataFrame(index=index, data=dict(zip(cols, data)))
    return df[cols]

# read in template model
template_inp = "../brambleton/template.inp"
template_model = swmmio.Model(template_inp)

# copy template model
target_inp = "../brambleton/brambleton.inp"
copyfile(template_inp, target_inp)

# read in node and pipe input data
node_data_file = "../brambleton/spatial/nodes_attr.csv"
ndf = pd.read_csv(node_data_file)
ndf.set_index("Structure_", inplace=True)
ndf.sort_index(inplace=True)
pipe_data_file = "../brambleton/spatial/pipes_attr.csv"
pdf = pd.read_csv(pipe_data_file)

# get just the nodes in our area
# todo: needs to take a list of outlet nodes
outlet_id = 'F15531'
us_node_col_name = "Upstream_S"
ds_node_col_name = "Downstream" 
us_node_ids = get_upstream_nodes(outlet_id, pdf, us_node_col_name, 
                                 ds_node_col_name)
us_node_data = ndf.loc[us_node_ids]

# get just the conduits in our area
us_cons_ids = get_upstream_conduits(outlet_id, pdf, 
                                    in_col_name=us_node_col_name, 
                                    out_col_name=ds_node_col_name)
us_cons = pdf.loc[us_cons_ids]

# convert the data into the format of the inp file tables
# make JUNCTIONS dataframe
# columns list so that we can have the columns in a specific order
jxns_cols = ['InvertElev', 'MaxDepth', 'SurchargedDepth', 'PondedArea'] 
# data for the columns
jxns_data = [us_node_data['Invert_Ele'], us_node_data['Rim_Elevat'], 0, 0]
jxns_nw = make_new_df(us_node_data.index, jxns_cols, jxns_data)

# make OUTFALLS dataframe
outlet_info = ndf.loc[outlet_id]
of_cols = ['InvertElev', 'OutfallType', 'StageOrTimeseries', 'TideGate']
of_data = [outlet_info['Invert_Ele'], 'FREE', '', 'NO']
of_nw = make_new_df([outlet_id], of_cols, of_data)

# make COORDINATES dataframe
coord_cols = ['X-Coord', 'Y-Coord']
coord_data = [us_node_data['Easting'], us_node_data['Northing']]
coord_nw = make_new_df(us_node_data.index, coord_cols, coord_data)

# make CONDUITS dataframe
conduits_cols = ['InletNode', 'OutletNode', 'Length', 'ManningN', 'InletOffset',
                 'OutletOffset', 'InitFlow', 'MaxFlow'] 
conduits_data = [us_cons[us_node_col_name], us_cons[ds_node_col_name],
                 us_cons['Pipe_Lengt'], 0.015, 0, 0, 0, 0 ]
conduits_nw = make_new_df(us_cons.index, conduits_cols, conduits_data)

# make XSECTION dataframe
xsec_cols = ['Shape', 'Geom1', 'Geom2', 'Geom3', 'Geom4', 'Barrels', 'Culvert']
# translate pipe geom
xsec_geom_sel = [us_cons['Pipe_Geome']=='CR', us_cons['Pipe_Geome']=='BX', 
                 us_cons['Pipe_Geome']=='AR', us_cons['Pipe_Geome']=='EL']
xsec_geom_vals = ['CIRCULAR', 'RECT_CLOSED', 'ARCH', 'HORIZ_ELLIPSE']
xsec_data = [np.select(xsec_geom_sel, xsec_geom_vals), 
             us_cons['Horizontal']/12., us_cons['Vertical_D']/12., 0, 0, 1, ''] 
             
xsec_nw = make_new_df(us_cons.index, xsec_cols, xsec_data)

# make SUBCATCHMENTS dataframe
sub_catch_cols = ['Name, Rain Gage, Outlet, Area, %Imperv, Width, %Slope, CurbLen, SnowPack''gt']


# replace the template model junctions with info from the node shapefile
replace_inp_section(target_inp, '[JUNCTIONS]', jxns_nw)
replace_inp_section(target_inp, '[COORDINATES]', coord_nw)
replace_inp_section(target_inp, '[CONDUITS]', conduits_nw)
replace_inp_section(target_inp, '[XSECTIONS]', xsec_nw)
replace_inp_section(target_inp, '[OUTFALLS]', of_nw)
