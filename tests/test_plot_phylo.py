#!/usr/bin/env python3
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import plot_phylo
import pytest
from test_plot_phylo_data import (test_plot_phylo_vars,
                                  test_plot_phylo_list,
                                  test_plot_phylo_nams,
                                  test_draw_tree_vars,
                                  test_draw_tree_list,
                                  test_draw_tree_nams,
                                  test_rev_align_vars,
                                  test_rev_align_list,
                                  test_rev_align_nams)
from test_get_boxes_data import (test_get_boxes_axes,
                                 test_get_boxes_texts,
                                 test_get_boxes_results)
import ete3
import pickle
import os
import shutil
import numpy as np


def compare_images(f1, f2, tol):
    f1arr = matplotlib.image.imread(f1)
    f2arr = matplotlib.image.imread(f2)

    f1arr_sub = f1arr[500:1500, 500:1500, :]
    f2arr_sub = f2arr[500:1500, 500:1500, :]
    return np.allclose(f1arr_sub, f2arr_sub, atol=tol)


def compare_floats(float1, float2, tolerance=0.05):
    abs_diff = abs(float1 - float2)
    print (float1, float2, abs_diff, (tolerance * abs(float2)), abs_diff <= (tolerance * abs(float2)))
    return abs_diff <= (tolerance * abs(float2))

# Tests all parameters with plot_phylo with three different trees
@pytest.mark.parametrize(test_plot_phylo_vars,
                         test_plot_phylo_list,
                         ids=test_plot_phylo_nams)
@pytest.mark.parametrize("tree, ylim", [["examples/primates.nw", 11],
                                        ["examples/basic_tree.nw", 5],
                                        ['examples/big_tree.nw', 300]])
def test_plot_phylo_params(xpos,
                           ypos,
                           width,
                           show_axis,
                           show_support,
                           align_tips,
                           rev_align_tips,
                           branch_lengths,
                           scale_bar,
                           scale_bar_width,
                           reverse,
                           outgroup,
                           col_dict,
                           label_dict,
                           font_size,
                           line_col,
                           line_width,
                           bold,
                           expected_figure,
                           ID, tree, ylim):
    
    tree_stem = tree.split("/")[-1].split(".")[0]

    f = plt.figure(figsize=(10, 20))
    a = f.add_subplot(111)
    a.set_xlim(-10, 20)
    a.set_ylim(-1, ylim)
    plot_phylo.plot_phylo(tree=tree, ax=a,
                          xpos=xpos,
                          ypos=ypos,
                          width=width,
                          height=ylim-1,
                          show_axis=show_axis,
                          show_support=show_support,
                          align_tips=align_tips,
                          rev_align_tips=rev_align_tips,
                          branch_lengths=branch_lengths,
                          scale_bar=scale_bar,
                          scale_bar_width=scale_bar_width,
                          reverse=reverse,
                          outgroup=outgroup,
                          col_dict=col_dict,
                          label_dict=label_dict,
                          font_size=font_size,
                          line_col=line_col,
                          line_width=line_width,
                          bold=bold)
    try:
        os.mkdir("test_temp")
    except FileExistsError:
        pass
    plt.savefig("test_temp/%s_%s.png" % (ID, tree_stem), bbox_inches='tight',
                dpi=200)
    plt.close()
    
    exp = expected_figure.replace(".png", "_%s.png" % tree_stem)
    # Compare the Matplotlib figures as images
    result = compare_images("test_temp/%s_%s.png" % (ID, tree_stem),
                            exp, tol=10)
    shutil.rmtree("test_temp")
    # Assert that the images are similar
    assert result


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
                          width,
                          depth,
                          align_tips,
                          rev_align_tips,
                          branch_lengths,
                          reverse,
                          appearance,
                          expected,
                          ID,
                          tree,
                          ylim):
    
    T = ete3.Tree(tree)
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

    test_obj = plot_phylo.draw_tree(tree=T, ax=a,
                                    x=x,
                                    y=y,
                                    x0=x0,
                                    ps=ps,
                                    height=ylim-1,
                                    width=width,
                                    depth=depth,
                                    align_tips=align_tips,
                                    rev_align_tips=rev_align_tips,
                                    branch_lengths=branch_lengths,
                                    reverse=reverse,
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
            if compare_floats(z1, z2):
                ll += 1
    assert ll == len(expected_obj)


@pytest.mark.parametrize(test_rev_align_vars,
                         test_rev_align_list,
                         ids=test_rev_align_nams)
@pytest.mark.parametrize("tree, ylim", [["examples/primates.nw", 11],
                                        ["examples/basic_tree.nw", 5],
                                        ['examples/big_tree.nw', 300]])
def test_reverse_align_params(x,
                              y,
                              x0,
                              width,
                              depth,
                              branch_lengths,
                              reverse,
                              appearance,
                              expected,
                              ID,
                              tree,
                              ylim):
    
    T = ete3.Tree(tree)
    tree_stem = tree.split("/")[-1].split(".")[0]

    f = plt.figure(figsize=(10, 20))
    a = f.add_subplot(111)
    a.set_xlim(-10, 19)
    a.set_ylim(-1, ylim)
    for nam in T.get_leaf_names():
        if nam not in appearance['label_dict']:
            appearance['label_dict'][nam] = nam
        if nam not in appearance['col_dict']:
            appearance['col_dict'][nam] = 'black'

    _, _, ps = plot_phylo.draw_tree(tree=T, ax=a,
                                    x=x,
                                    y=y,
                                    x0=x0,
                                    ps=[],
                                    height=ylim-1,
                                    width=width,
                                    depth=depth,
                                    align_tips=True,
                                    rev_align_tips=True,
                                    branch_lengths=branch_lengths,
                                    reverse=reverse,
                                    appearance=appearance)
    plt.close()
    reverse = plot_phylo.reverse_align(a, ps, True)

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
            if compare_floats(z1, z2):
                ll += 1
    assert ll == len(expected_obj)


@pytest.mark.parametrize("ax, texts, expected_result",
                         list(zip(test_get_boxes_axes,
                                  test_get_boxes_texts,
                                  test_get_boxes_results)))
def test_get_boxes(ax, texts, expected_result):
    boxes = plot_phylo.get_boxes(ax, texts)
    bclean = dict()
    for b, vals in boxes.items():
        bclean[b] = dict()
        for v in vals:
            bclean[b][v] = round(vals[v], 0)
    assert bclean == expected_result
