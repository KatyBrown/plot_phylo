#!/usr/bin/env python3
import numpy as np
import matplotlib


def compare_images(f1, f2, tol):
    f1arr = matplotlib.image.imread(f1)
    f2arr = matplotlib.image.imread(f2)

    f1arr_sub = f1arr[500:1500, 500:1500, :]
    f2arr_sub = f2arr[500:1500, 500:1500, :]
    return np.allclose(f1arr_sub, f2arr_sub, atol=tol)


def compare_floats(float1, float2, tolerance=0.05):
    abs_diff = abs(float1 - float2)
    return abs_diff <= (tolerance * abs(float2))


def get_plot_phylo_metadata():
    variD = {'xpos': 0,
             'ypos': 0,
             'width': 10,
             'show_axis': False,
             'show_support': True,
             'align_tips': False,
             'rev_align_tips': False,
             'branch_lengths': True,
             'scale_bar': True,
             'scale_bar_width': None,
             'reverse': False,
             'outgroup': None,
             'col_dict': {},
             'label_dict': {},
             'font_size': 10,
             'line_col': 'black',
             'line_width': 1,
             'bold': [],
             'collapse': [],
             'collapse_names': [],
             'auto_ax': True}
    varis = ['xpos',
             'ypos',
             'width',
             'show_axis',
             'show_support',
             'align_tips',
             'rev_align_tips',
             'branch_lengths',
             'scale_bar',
             'scale_bar_width',
             'reverse',
             'outgroup',
             'col_dict',
             'label_dict',
             'font_size',
             'line_col',
             'line_width',
             'bold',
             'collapse',
             'collapse_names',
             'auto_ax']
    return (variD, varis)


def get_draw_tree_metadata():
    variD = {'x': 0,
             'y': 0,
             'x0': 0,
             'ps': [],
             'dims': {'width': 10,
                      'height': 10,
                      'depth': [5, 5, 5]},
             'structure': {'align_tips': False,
                           'rev_align_tips': False,
                           'branch_lengths': True,
                           'reverse': False},
             'appearance': {'col_dict': {},
                            'label_dict': {},
                            'font_size': 10,
                            'line_col': 'black',
                            'line_width': 1,
                            'show_support': True,
                            'bold': []},
             'collapse': [],
             'collapseD': dict()}
    varis_draw_tree = ['x',
                       'y',
                       'x0',
                       'ps',
                       'dims',
                       'structure',
                       'appearance',
                       'collapse',
                       'collapseD']
    return (variD, varis_draw_tree)

