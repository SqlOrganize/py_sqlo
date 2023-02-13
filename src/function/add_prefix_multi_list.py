def add_prefix_multi_list(l:list, prefix:str=""):
    ll = l.copy()
    if (ll):
        if (isinstance(ll[0],list)):
            for i, v in enumerate(l):
                v = add_prefix_multi_list(v, prefix)
                ll[i] = v

        else:
            ll[0] = prefix + ll[0]

    return ll
