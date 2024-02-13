#!/usr/bin/env python3
from matplotlib.testing.compare import compare_images
import matplotlib.pyplot as plt
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
    plt.savefig("test_temp/%s_%s.png" % (ID, tree_stem), bbox_inches='tight')
    plt.close()
    
    exp = expected_figure.replace(".png", "_%s.png" % tree_stem)
    # Compare the Matplotlib figures as images
    result = compare_images("test_temp/%s_%s.png" % (ID, tree_stem),
                            exp, tol=10)
    #shutil.rmtree("test_temp")
    # Assert that the images are similar
    assert result is None


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
    ytest = test_obj[0]
    y2test = test_obj[1]
    ps = test_obj[2]
    v0 = [v[0] for v in ps]
    v1 = [str(v[1]) for v in ps]
    plt.close()

    test_dat = [ytest, y2test, v0, v1]

    e0 = expected.replace(".pickle", "_%s.pickle" % tree_stem)
    expected_obj = pickle.load(open(e0, "rb"))
    assert expected_obj == test_dat


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
    a.set_xlim(-10, 20)
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
    
    v0 = [v[0] for v in reverse]
    v1 = [str(v[1]) for v in reverse]
    v2 = [[str(w.get_xdata()) + str(w.get_ydata())
           for w in v[2]] for v in reverse]
    e0 = expected.replace(".pickle", "_%s.pickle" % tree_stem)
    test_dat = [v0, v1, v2]

    expected_obj = pickle.load(open(e0, "rb"))
    assert expected_obj == test_dat


@pytest.mark.parametrize("ax, texts, expected_result",
                         list(zip(test_get_boxes_axes,
                                  test_get_boxes_texts,
                                  test_get_boxes_results)))
def test_get_boxes(ax, texts, expected_result):
    boxes = plot_phylo.get_boxes(ax, texts)
    assert boxes == expected_result


def test_draw_scale_bar():
    pass