from test_amend_tree_data import (test_rev_align_vars,
                                  test_rev_align_list,
                                  test_rev_align_nams)
import matplotlib.pyplot as plt
from plot_phylo import draw_tree
from plot_phylo import amend_tree
import pytest
import ete3
import pickle
import helper_functions
import matplotlib
matplotlib.use('Agg')


plt.rcParams.update({
    'font.family': 'DejaVu Sans',
    'figure.dpi': 100              # Set a fixed DPI
})


@pytest.mark.parametrize(test_rev_align_vars,
                         test_rev_align_list,
                         ids=test_rev_align_nams)
@pytest.mark.parametrize("tree, ylim", [["examples/primates.nw", 11],
                                        ["examples/basic_tree.nw", 5],
                                        ['examples/big_tree.nw', 300]])
def test_reverse_align_params(x,
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

    _, _, ps = draw_tree.draw_tree(tree=T, ax=a,
                                   x=x,
                                   y=y,
                                   x0=x0,
                                   ps=[],
                                   dims=dims,
                                   structure=structure,
                                   appearance=appearance)
    reverse = amend_tree.reverse_align(a, ps, True)
    plt.close()
    e0 = expected.replace(".pickle", "_%s.pickle" % tree_stem)

    test_dat = []
    for v0, v1, v2 in reverse:
        row = [v0]
        x, y = v1.get_position()
        row += [round(x, 2), round(y, 2)]
        row += [v1.get_text()]
        for w in v2:
            x2 = [round(z, 2) for z in w.get_xdata()]
            y2 = [round(z, 2) for z in w.get_ydata()]
            row += x2
            row += y2
        test_dat += row
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
