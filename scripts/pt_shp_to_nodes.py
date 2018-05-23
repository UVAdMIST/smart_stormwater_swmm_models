from swmmio import swmmio
from swmmio.utils.modify_model import replace_inp_section
from get_contributing_area import get_upstream_nodes
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
us_node_ids = get_upstream_nodes('F15531', pdf, "Upstream_S", "Downstream")
us_node_data = ndf[ndf["Structure_"].isin(us_node_ids)]
us_node_data.set_index("Structure_", inplace=True)
us_node_data.sort_index(inplace=True)

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

# replace the template model junctions with info from the node shapefile
replace_inp_section(target_inp, '[JUNCTIONS]', jxns_nw)
replace_inp_section(target_inp, '[COORDINATES]', coord_nw)
