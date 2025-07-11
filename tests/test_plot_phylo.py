#!/usr/bin/env python3
import matplotlib.pyplot as plt
import plot_phylo
import pytest
from test_plot_phylo_data import (test_plot_phylo_vars,
                                  test_plot_phylo_list,
                                  test_plot_phylo_nams)
import os
import shutil
import matplotlib
from matplotlib.testing.compare import compare_images
matplotlib.use('Agg')


plt.rcParams.update({
    'font.family': 'DejaVu Sans',
    'figure.dpi': 100 # Set a fixed DPI
})


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
                           ID, tree, ylim,
                           collapse,
                           collapse_names,
                           auto_ax):

    tree_stem = tree.split("/")[-1].split(".")[0]

    f = plt.figure(figsize=(10, 20))
    a = f.add_subplot(111)
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
                          bold=bold,
                          collapse=collapse,
                          collapse_names=collapse_names,
                          auto_ax=auto_ax)
    try:
        os.mkdir("test_temp")
    except FileExistsError:
        pass
    plt.savefig("test_temp/%s_%s.png" % (ID, tree_stem), bbox_inches='tight',
                dpi=200)
    plt.close('all')

    exp = expected_figure.replace(".png", "_%s.png" % tree_stem)
    # Compare the Matplotlib figures as images
    result = compare_images("test_temp/%s_%s.png" % (ID, tree_stem),
                            exp, tol=30)

    shutil.rmtree("test_temp")
    # Assert that the images are similar
    assert result is None


@pytest.mark.parametrize(test_plot_phylo_vars,
                         test_plot_phylo_list,
                         ids=test_plot_phylo_nams)
@pytest.mark.parametrize("tree, ylim", [["examples/bad_tree.nw", 1]])
def test_bad_tree(xpos,
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
                  ID, tree, ylim,
                  collapse,
                  collapse_names,
                  auto_ax):
    f = plt.figure(figsize=(10, 20))
    a = f.add_subplot(111)
    with pytest.raises(RuntimeError,
                       match="Error in parsing Newick"):
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
    plt.close()
