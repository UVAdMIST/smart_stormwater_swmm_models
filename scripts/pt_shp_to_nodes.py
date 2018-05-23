from swmmio import swmmio
from swmmio.utils.modify_model import replace_inp_section
from swmmio.utils.dataframes import create_dataframeINP
from get_contributing_area import get_upstream_nodes
import pandas as pd
from shutil import copyfile

# read in template model
template_inp = "../brambleton/template.inp"
template_model = swmmio.Model(template_inp)

# copy template model
target_inp = "../brambleton/brambleton.inp"
copyfile(template_inp, target_inp)

# read in node input data
node_data = "../brambleton/spatial/nodes_attr.txt"
ndf = pd.read_csv(node_data)

# get just the nodes in our area

# convert the data into the format of the inp file table

# create a dataframe of the template model's junctions
jxns = create_dataframeINP(template_inp, '[JUNCTIONS]')

# replace the template model junctions with info from the node shapfile

