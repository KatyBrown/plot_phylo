#!/usr/bin/env python3
import ete3
from plot_phylo import draw_tree, amend_tree, get_boxes


def plot_phylo(tree, ax,
               xpos=0,
               ypos=0,
               width=10,
               height=10,
               show_axis=False,
               show_support=True,
               align_tips=False,
               rev_align_tips=False,
               branch_lengths=True,
               scale_bar=True,
               scale_bar_width=None,
               reverse=False,
               outgroup=None,
               col_dict={},
               label_dict={},
               font_size=10,
               line_col='black',
               line_width=1,
               bold=[],
               collapse=[],
               collapse_names=[],
               auto_ax=True,
               dots=False):
    '''
    Parameters
    ----------
    tree : str
        Either the path to a newick formatted tree or a string containing
        a newick formatted tree. Required.
    ax : matplotlib.axes._axes.Axes,
        An open matplotlib ax object where the tree will be plotted. Required.
    xpos : float
        Desired position of the root node of the tree on the x axis of ax,
        in axis units. Default 0.
    ypos : float
        Desired position of the bottom of the tree on the y axis of ax,
        in axis units. Default 0.
    height : float
        Desired height of the tree, in axis units. Default 10.
    width : float
        Desired width of the tree, in axis units. Default 10.
    show_axis : bool
        Show the axis on the output tree. Default True. This can be toggled
        later directly on the matplotlib ax.
    show_support : bool
        Display branch support on the internal nodes of the tree. Default
        False.
    align_tips : bool
        If True, the tip labels will be aligned rather than positioned at
        the end of the branches. Default False.
    rev_align_tips: bool
        If True  the tip labels are right aligned
        if reverse=False and left aligned if reverse=True.
    branch_lengths : bool
        If True, the branch lengths provided in the tree are used,
        otherwise all branches are fixed to the same length. Default True.
    scale_bar: bool
        If True and branch_lengths is True, draw a scale bar.
    scale_bar_width: float
        Width of scale bar in axis units. If not specified, the scale bar
        will be 1/4 of the width of the tree.
    reverse: bool
        If True, reverse the tree on the y-axis, showing the root on the right
        hand side. Default False.
    outgroup: str
        Leaf to use as an outgroup, must be identical to the     print (tree)
name of the
        leaf in the tree file.
    col_dict : dict
        User provided dictionary with tip labels as keys and colours
        (in any format accepted by matplotlib
         https://matplotlib.org/stable/users/explain/colors/colors.html
        as values. If this is not
        specified all labels will be black, if only some labels are specified
        all others will be black.
    label_dict : TYPE, optional
        User provided dictionary with current tip labels as keys and desired
        tip labels as values. If this is not specified all labels
        will be as specified in the newick, if some labels are specified
        all others will match the newick.
    font_size : int
        Font size for tip labels. Default 10.
    line_col : str or tuple
        Line colour, in any format allowed by matplotlib
        https://matplotlib.org/stable/users/explain/colors/colors.html.
        Default is black.
    line_width : float
        Line width. Default 2.
    bold: list
        List of tip labels to show in bold.


    Returns
    -------
    ps : list
        List of lists - ordered as tip labels, tip label text objects,
        alignment lines (if aligned). All are in the same order.
    '''
    # Read the tree
    try:
        T = ete3.Tree(tree)
    except ete3.parser.newick.NewickError:
        try:
            # Allows for trees with named internal nodes
            T = ete3.Tree(tree, format=1)
        except ete3.parser.newick.NewickError as e:
            raise RuntimeError(f"Error in parsing Newick format: {e}")

    if outgroup and outgroup in set(T.get_leaf_names()):
        T.set_outgroup(outgroup)

    if len(collapse) != 0:
        assert len(collapse) == len(collapse_names), "To collapse nodes the \
            collapse_strings and collapse_names parameters must be lists \
            of equal length"
        T, collapseD, countD = draw_tree.collapse_nodes(T, collapse,
                                                        collapse_names)
    else:
        collapseD = dict()
        countD = dict()

    # Define dictionaries for colours and labels if not provided
    for nam in T.get_leaf_names():
        if nam not in label_dict:
            label_dict[nam] = nam
        if len(collapse) != 0:
            for string in collapse:
                if nam in label_dict:
                    label_dict[nam.strip(string)] = label_dict[nam]
                else:
                    label_dict[nam.strip(string)] = nam.strip(string)

        if len(collapse) != 0:
            for string in collapse:
                if nam.endswith(string):
                    stripped = nam.removesuffix(string)
                    cc = stripped.replace("COLLAPSE|", "")
                    if nam in col_dict or \
                            stripped in col_dict or cc in col_dict:
                        if nam in col_dict:
                            col_dict[stripped] = col_dict[nam]
                            col_dict[f'COLLAPSE|{stripped}'] = col_dict[nam]
                        elif stripped in col_dict:
                            col_dict[nam] = col_dict[stripped]
                            col_dict[f'COLLAPSE|{stripped}'] = \
                                col_dict[stripped]
                        else:
                            col_dict[nam] = col_dict[cc]
                            col_dict[stripped] = col_dict[cc]
                            col_dict[f'COLLAPSE|{stripped}'] = col_dict[cc]
                    else:
                        col_dict[stripped] = 'black'
                        col_dict[f'COLLAPSE|{stripped}'] = 'black'
                        col_dict[nam] = 'black'
        if nam not in col_dict:
            col_dict[nam] = 'black'
    # Dictionary to pass apperance params to the plotting function
    appearance = {'font_size': font_size,
                  'line_col': line_col,
                  'line_width': line_width,
                  'col_dict': col_dict,
                  'label_dict': label_dict,
                  'show_support': show_support,
                  'bold': bold}

    structure = {'align_tips': align_tips,
                 'rev_align_tips': rev_align_tips,
                 'branch_lengths': branch_lengths,
                 'reverse': reverse}

    if auto_ax:
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)

    # Calculate the total height and width of the original tree
    # in terms of number of nodes, total branch length, number of tips
    maxdist = ((T.get_farthest_leaf(topology_only=True)[1],
                T.get_farthest_leaf(topology_only=False)[1],
                len(T)))

    # Without branch lengths the tree has a root which appears at position -1,
    # so shift the tree over by one unit
    if not branch_lengths:
        xpos += 1
        width -= 2
    elif align_tips:
        width -= 1

    if reverse:
        xpos = -xpos

    dims = {'height': height,
            'width': width,
            'depth': maxdist}
    # Call the main function. The second and third returns are used
    # internally when the function is called recursively but
    # are not needed by the user

    _, _, ps = draw_tree.draw_tree(T, ax,
                                   x=xpos,
                                   y=-ypos-height,
                                   x0=xpos,
                                   ps=[],
                                   dims=dims,
                                   structure=structure,
                                   appearance=appearance,
                                   collapse=collapse,
                                   collapseD=collapseD,
                                   countD=countD,
                                   dots=dots)

    if rev_align_tips:
        ps = amend_tree.reverse_align(ax, ps, reverse)
    # Hide axis
    if not show_axis:
        ax.set_axis_off()
    if scale_bar and branch_lengths:
        if not reverse:
            amend_tree.draw_scale_bar(ax, width, height, maxdist, xpos, ypos,
                                      scale_bar_width=scale_bar_width,
                                      appearance=appearance)
        else:
            amend_tree.draw_scale_bar(ax, width, height, maxdist, -xpos,
                                      ypos,
                                      scale_bar_width=scale_bar_width,
                                      appearance=appearance)

    textobj = [p[1] for p in ps]
    boxes = get_boxes.get_boxes(ax, textobj)
    if auto_ax:
        textobj, ax = amend_tree.auto_axis(ax, textobj,
                                           xpos, ypos,
                                           width, height, maxdist,
                                           scale_bar, branch_lengths,
                                           reverse=reverse)

    return (boxes)
