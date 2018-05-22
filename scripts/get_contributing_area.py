def get_upstream_conduits(node_id, con_df, in_col_name="InletNode", out_col_name="OutletNode"):
    us_nodes = get_upstream_nodes(node_id, con_df)
    us_cons = con_df[(con_df[in_col_name].isin(us_nodes)) | (con_df[out_col_name].isin(us_nodes))] 
    return us_cons.index

def get_upstream_nodes_one(node_id, con_df, in_col_name, out_col_name):
    conids = con_df[con_df[out_col_name] == node_id].index
    if len(conids)>0:
        us_node_ids = con_df[in_col_name].loc[conids].tolist()
        return us_node_ids
    else:
        return []

def get_upstream_nodes(node_id, con_df, in_col_name="InletNode", out_col_name="OutletNode"):
    l = get_upstream_nodes_one(node_id, con_df, in_col_name, out_col_name)
    for n in l:
        l.extend(get_upstream_nodes_one(n, con_df, in_col_name, out_col_name))
    return l

def get_contributing_subs(node_id, con_df, subs_df, **kwargs):
    us_nodes = get_upstream_nodes(node_id, con_df, **kwargs)
    us_subs = subs_df[subs["Outlet"].isin(us_nodes)]
    return us_subs

def get_contributing_area(node_id, con_df, subs_df, **kwargs):
    cont_subs = get_contributing_subs(node_id, con_df, subs_df, **kwargs)
    return cont_subs["Area"].sum()

