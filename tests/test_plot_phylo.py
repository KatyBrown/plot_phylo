#!/usr/bin/env python3
from matplotlib.testing.compare import compare_images
import matplotlib.pyplot as plt
import plot_phylo
import os
import pytest
from test_data import test_plot_phylo_vars, test_plot_phylo_list, test_plot_phylo_nams
import ete3


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
                           col_dict,
                           label_dict,
                           font_size,
                           line_col,
                           line_width,
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
                          col_dict=col_dict,
                          label_dict=label_dict,
                          font_size=font_size,
                          line_col=line_col,
                          line_width=line_width)
    plt.savefig("test_temp/%s_%s.png" % (ID, tree_stem), bbox_inches='tight')
    plt.close()
    
    exp = expected_figure.replace(".png", "_%s.png" % tree_stem)
    # Compare the Matplotlib figures as images
    result = compare_images("test_temp/%s_%s.png" % (ID, tree_stem),
                            exp, tol=10)

    # Assert that the images are similar
    assert result is None, f"Images differ: {result}"


# Tests all parameters with plot_phylo with three different trees
@pytest.mark.parametrize(test_plot_phylo_vars,
                         test_plot_phylo_list,
                         ids=test_plot_phylo_nams)
@pytest.mark.parametrize("tree, ylim", [["examples/primates.nw", 11],
                                        ["examples/basic_tree.nw", 5],
                                        ['examples/big_tree.nw', 300]])
def test_draw_tree(xpos,
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
                   col_dict,
                   label_dict,
                   font_size,
                   line_col,
                   line_width,
                   expected_figure,
                   ID, tree, ylim):
    
    T = ete3.tree(tree)
    _, _, ps = draw_tree(T, ax,
                         x=xpos,
                         y=-ypos-height,
                         x0=xpos,
                         ps=[],
                         height=height,
                         width=width,
                         depth=maxdist,
                         align_tips=align_tips,
                         rev_align_tips=rev_align_tips,
                         branch_lengths=branch_lengths,
                         reverse=reverse,
                         appearance=appearance)
              appearance={}):
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
                          col_dict=col_dict,
                          label_dict=label_dict,
                          font_size=font_size,
                          line_col=line_col,
                          line_width=line_width)
    plt.savefig("test_temp/%s_%s.png" % (ID, tree_stem), bbox_inches='tight')
    plt.close()
    
    exp = expected_figure.replace(".png", "_%s.png" % tree_stem)
    # Compare the Matplotlib figures as images
    result = compare_images("test_temp/%s_%s.png" % (ID, tree_stem),
                            exp, tol=10)

    # Assert that the images are similar
    assert result is None, f"Images differ: {result}"

def test_get_boxes():
    pass

def test_draw_tree():
    pass

def test_reverse_align():
    pass

def test_draw_scale_bar():
    pass