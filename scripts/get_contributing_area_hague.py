from swmmio import swmmio
from get_contributing_area import get_contributing_area

mymodel = swmmio.Model("../hague_model/v2014_Hague_EX_10yr_MHHW_mod2.inp")
nodes = mymodel.nodes()
cons = mymodel.conduits()
subs = mymodel.subcatchments()

a0 = get_contributing_area("St1", cons, subs)
a1 = get_contributing_area("E143351", cons, subs)
a2 = get_contributing_area("E144050", cons, subs)
a3 = get_contributing_area("E146004", cons, subs)
