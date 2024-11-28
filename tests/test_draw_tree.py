#!/usr/bin/env python3
import matplotlib.pyplot as plt
from plot_phylo import draw_tree
import pytest
from test_draw_tree_data import (test_draw_tree_vars,
                                 test_draw_tree_list,
                                 test_draw_tree_nams)

import ete3
import pickle
import helper_functions


@pytest.mark.parametrize(test_draw_tree_vars,
                         test_draw_tree_list,
                         ids=test_draw_tree_nams)
@pytest.mark.parametrize("tree, ylim", [["examples/primates.nw", 11],
                                        ["examples/basic_tree.nw", 5],
                                        ['examples/big_tree.nw', 300]])
def test_draw_tree_params(x,
                          y,
                          x0,
                          ps,
                          dims,
                          structure,
                          appearance,
                          collapse,
                          collapseD,
                          expected,
                          ID,
                          tree,
                          ylim):
    try:
        T = ete3.Tree(tree)
    except ete3.parser.newick.NewickError:
        try:
            # Allows for trees with named internal nodes
            T = ete3.Tree(tree, format=1)
        except ete3.parser.newick.NewickError as e:
            raise RuntimeError(f"Error in parsing Newick format: {e}")
    tree_stem = tree.split("/")[-1].split(".")[0]

    f = plt.figure(figsize=(10, 20))
    a = f.add_subplot(111)
    a.set_xlim(-10, 20)
    a.set_ylim(-1, ylim)
    for nam in T.get_leaf_names():
        if nam not in appearance['label_dict']:
            appearance['label_dict'][nam] = nam
        if nam not in appearance['col_dict']:
            appearance['col_dict'][nam] = 'black'

    test_obj = draw_tree.draw_tree(tree=T, ax=a,
                                   x=x,
                                   y=y,
                                   x0=x0,
                                   ps=ps,
                                   dims=dims,
                                   structure=structure,
                                   appearance=appearance)
    plt.close()
    ytest = round(test_obj[0], 2)
    y2test = round(test_obj[1], 2)
    test_dat = [ytest, y2test]
    for v in test_obj[2]:
        row = [v[0]]
        x, y = v[1].get_position()
        row += [round(x, 2), round(y, 2)]
        row += [v[1].get_text()]
        test_dat += row
    e0 = expected.replace(".pickle", "_%s.pickle" % tree_stem)
    expected_obj = pickle.load(open(e0, "rb"))
    ll = 0
    for z1, z2 in zip(expected_obj, test_dat):
        if isinstance(z1, str):
            if z1 == z2:
                ll += 1
        else:
            if helper_functions.compare_floats(z1, z2):
                ll += 1
    assert ll == len(expected_obj)
