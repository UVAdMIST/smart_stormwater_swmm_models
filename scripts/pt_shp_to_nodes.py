from swmmio import swmmio
from swmmio.utils.modify_model import replace_inp_section
from get_contributing_area import get_upstream_nodes, get_upstream_conduits
import pandas as pd
from shutil import copyfile

# read in template model
template_inp = "../brambleton/template.inp"
template_model = swmmio.Model(template_inp)

# copy template model
target_inp = "../brambleton/brambleton.inp"
copyfile(template_inp, target_inp)

# read in node and pipe input data
node_data_file = "../brambleton/spatial/nodes_attr.txt"
ndf = pd.read_csv(node_data_file)
pipe_data_file = "../brambleton/spatial/pipes_attr.txt"
pdf = pd.read_csv(pipe_data_file)

# get just the nodes in our area
outlet_id = 'F15531'
us_node_col_name = "Upstream_S"
ds_node_col_name = "Downstream" 
us_node_ids = get_upstream_nodes(outlet_id, pdf, us_node_col_name, ds_node_col_name)
us_node_data = ndf[ndf["Structure_"].isin(us_node_ids)]
us_node_data.set_index("Structure_", inplace=True)
us_node_data.sort_index(inplace=True)

# get just the conduits in our area
us_cons_ids = get_upstream_conduits(outlet_id, pdf, in_col_name=us_node_col_name, out_col_name=ds_node_col_name)
us_cons = pdf.loc[us_cons_ids]

# convert the data into the format of the inp file tables
jxns_nw = pd.DataFrame(index=us_node_data.index,
                       data={
                           'InvertElev':us_node_data['Invert_Ele'],
                           'MaxDepth':us_node_data['Rim_Elevat'],
                           'SurchargedDepth':0,
                           'PondedArea':0
                           }
                      )

coord_nw = pd.DataFrame(index=us_node_data.index,
                        data={
                            'X-Coord':us_node_data['Easting'],
                            'Y-Coord':us_node_data['Northing']
                            }
                       )

conduits_columns = ['InletNode', 'OutletNode', 'Length', 'ManningN', 'InletOffset', 'OutletOffset',
                   'InitFlow', 'MaxFlow'] 
conduits_data = [us_cons[us_node_col_name], us_cons[ds_node_col_name], us_cons['Pipe_Lengt'], 
                 0.015, 0, 0, 0, 0 ]
conduits_nw = pd.DataFrame(index=us_cons.index,
                           data=dict(zip(conduits_columns, conduits_data))
                          )
conduits_nw = conduits_nw[conduits_columns]


# replace the template model junctions with info from the node shapefile
replace_inp_section(target_inp, '[JUNCTIONS]', jxns_nw)
replace_inp_section(target_inp, '[COORDINATES]', coord_nw)
replace_inp_section(target_inp, '[CONDUITS]', conduits_nw)
