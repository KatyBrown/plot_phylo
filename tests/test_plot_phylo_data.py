#!/usr/bin/env python3
import plot_phylo
import copy

# Default parameters values
defaults = plot_phylo.plot_phylo.__defaults__
# Number of parameters
ac = plot_phylo.plot_phylo.__code__.co_argcount
# Argument names, excluding variables defined within the function and
# arguments with no default values
varis = list(plot_phylo.plot_phylo.__code__.co_varnames[
             ac-len(defaults):ac])

variD = dict(zip(varis, defaults))

varis.remove('height')
variD.pop('height')

defaults_draw_tree = plot_phylo.draw_tree.__defaults__
ac_draw_tree = plot_phylo.draw_tree.__code__.co_argcount
varis_draw_tree = list(plot_phylo.draw_tree.__code__.co_varnames[
    ac_draw_tree-len(defaults_draw_tree):ac_draw_tree])
varis_draw_tree.remove('height')

varis_rev_align = copy.deepcopy(varis_draw_tree)
varis_rev_align.remove('align_tips')
varis_rev_align.remove('rev_align_tips')
varis_rev_align.remove('ps')

tests_plot_phylo = [{},
                    {'xpos': 1, 'ypos': 1},
                    {'show_axis': False},
                    {'show_support': False},
                    {'align_tips': True},
                    {'rev_align_tips': True},
                    {'branch_lengths': False},
                    {'scale_bar': False},
                    {'scale_bar_width': 6},
                    {'reverse': True},
                    {'outgroup': 'Homo sapiens'},
                    {'rev_align_tips': True, 'reverse': True},
                    {'col_dict': {'Homo sapiens': 'blue'}},
                    {'label_dict': {'Homo sapiens': 'human'}},
                    {'font_size': 20},
                    {'line_col': 'orange'},
                    {'line_width': 5},
                    {'bold': ['Homo sapiens']}]

tests_draw_tree = [{},
                  {'xpos': 1, 'ypos': 1},
                  {'show_axis': False},
                  {'align_tips': True},
                  {'rev_align_tips': True},
                  {'branch_lengths': False},
                  {'scale_bar': False},
                  {'scale_bar_width': 6},
                  {'reverse': True},
                  {'rev_align_tips': True, 'reverse': True},
                  {'appearance': {'col_dict': {'Homo sapiens': 'blue'},
                                  'label_dict': {'Homo sapiens': 'human'},
                                  'font_size': 20,
                                  'line_col': 'orange',
                                  'line_width': 5,
                                  'show_support': True,
                                  'bold': ['Homo sapiens']}},
                  {'depth': [2, 2, 2]}]

test_plot_phylo_list = []
test_plot_phylo_nams = []
for test in tests_plot_phylo:
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

test_draw_tree_list = []
test_draw_tree_nams = []
for test in tests_draw_tree:
    testnam = "draw_tree_%s" % "_".join(test.keys())
    curr_dict = copy.deepcopy(variD)
    curr_dict['x'] = curr_dict['xpos']
    curr_dict['x0'] = curr_dict['xpos']
    curr_dict['y'] = curr_dict['ypos']
    curr_dict['ps'] = []
    curr_dict['appearance'] = dict()
    for var in ['col_dict', 'label_dict', 'font_size',
                'line_col', 'line_width', 'show_support', 'bold']:
        curr_dict['appearance'][var] = curr_dict[var]
    curr_dict['depth'] = [5, 5, 5]
    curr_dict.update(test)
    pass_vals = [curr_dict[v] for v in varis_draw_tree]
    pass_vals.append('tests/test_objects/%s.pickle' % testnam)
    pass_vals.append(testnam)
    test_draw_tree_list.append(pass_vals)
    test_draw_tree_nams.append(testnam)
test_draw_tree_vars = ",".join(varis_draw_tree + ['expected', 'ID'])


test_rev_align_list = []
test_rev_align_nams = []
for test in tests_draw_tree:
    testnam = "rev_align_%s" % "_".join(test.keys())
    if 'align_tips' not in testnam:
        curr_dict = copy.deepcopy(variD)
        curr_dict['x'] = curr_dict['xpos']
        curr_dict['x0'] = curr_dict['xpos']
        curr_dict['y'] = curr_dict['ypos']
        curr_dict['appearance'] = dict()
        for var in ['col_dict', 'label_dict', 'font_size',
                    'line_col', 'line_width', 'show_support', 'bold']:
            curr_dict['appearance'][var] = curr_dict[var]
        curr_dict.update(test)
        curr_dict['depth'] = [5, 5, 5]
        curr_dict.pop('rev_align_tips')
        curr_dict.pop('align_tips')
        pass_vals = [curr_dict[v] for v in varis_rev_align]
        pass_vals.append('tests/test_objects/%s.pickle' % testnam)
        pass_vals.append(testnam)
        test_rev_align_list.append(pass_vals)
        test_rev_align_nams.append(testnam)
test_rev_align_vars = ",".join(varis_rev_align + ['expected', 'ID'])