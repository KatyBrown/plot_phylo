#!/usr/bin/env python3
import plot_phylo
import copy
import matplotlib.pyplot as plt


# Default parameters values
defaults = plot_phylo.plot_phylo.__defaults__
# Number of parameters
ac = plot_phylo.plot_phylo.__code__.co_argcount
# Argument names, excluding variables defined within the function and
# arguments with no default values
varis = list(plot_phylo.plot_phylo.__code__.co_varnames[
             ac-len(defaults):ac-len(defaults)+len(defaults)])

variD = dict(zip(varis, defaults))

varis.remove('height')
variD.pop('height')


tests = [{},
         {'xpos': 1, 'ypos': 1},
         {'show_axis': False},
         {'show_support': False},
         {'align_tips': True},
         {'rev_align_tips': True},
         {'branch_lengths': False},
         {'scale_bar': False},
         {'scale_bar_width': 6},
         {'reverse': True},
         {'rev_align_tips': True, 'reverse': True},
         {'col_dict': {'Homo sapiens': 'blue'}},
         {'label_dict': {'Homo sapiens': 'human'}},
         {'font_size': 20},
         {'line_col': 'orange'},
         {'line_width': 5}]


test_plot_phylo_list = []
test_plot_phylo_nams = []
for test in tests:
    testnam = "_".join(test.keys())
    if len(testnam) == 0:
        testnam = "basic"
    curr_dict = copy.deepcopy(variD)
    curr_dict.update(test)
    pass_vals = [curr_dict[v] for v in varis]
    pass_vals.append('tests/test_images/%s.png' % testnam)
    pass_vals.append(testnam)
    test_plot_phylo_list.append(pass_vals)
    test_plot_phylo_nams.append(testnam)
test_plot_phylo_vars = ",".join(varis + ['expected_figure', 'ID'])

