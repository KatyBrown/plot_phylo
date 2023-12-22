#!/usr/bin/env python3
import ete3

def plot_tree(tree, ax,
              xpos=0,
              ypos=0,
              width=10,
              height=10,
              show_axis=True,
              show_support=False,
              align_tips=False,
              branch_lengths=True,
              col_dict={},
              label_dict={},
              font_size=10,
              line_col='black',
              line_width=2):
    '''

    Parameters
    ----------
    tree : str
        Either the path to a newick formatted tree or a string containing
        a newick formatted tree. Required.
    ax : matplotlib.axes._axes.Axes,
        An open matplotlib ax object where the tree will be plotted. Required.
    x : float
        Desired position of the root node of the tree on the x axis of ax,
        in axis units. Default 0. 
    y : float
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
    branch_lengths : bool
        If True, the branch lengths provided in the tree are used,
        otherwise all branches are fixed to the same length. Default True.
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

    Returns
    -------
    ps : list
        List of lists - ordered as tip labels, tip label x positions,
        tip label y positions. All are in the same order.

    '''
    # Read the tree
    T = ete3.Tree(tree)

    # Define dictionaries for colours and labels if not provided
    for nam in T.get_leaf_names():
        if nam not in label_dict:
            label_dict[nam] = nam
        if nam not in col_dict:
            col_dict[nam] = 'black'
    # Dictionary to pass apperance params to the plotting function
    appearance = {'font_size': font_size,
                  'line_col': line_col,
                  'line_width': line_width,
                  'col_dict': col_dict,
                  'label_dict': label_dict,
                  'show_support': show_support}


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
    # Call the main function. The second and third returns are used
    # internally when the function is called recursively but
    # are not needed by the user
    
    _, _, ps = draw_tree(T, ax,
                         x=xpos,
                         y=-(ypos+len(T)),
                         x0=xpos,
                         ps=[],
                         height=height,
                         width=width,
                         depth=maxdist,
                         align_tips=align_tips,
                         branch_lengths=branch_lengths,
                         appearance=appearance)
    # Hide axis
    if not show_axis:
        ax.set_axis_off()
    return (ps)

def draw_tree(tree, ax,
              x=0,
              y=0,
              x0=0,
              ps=[],
              height=10,
              width=10,
              depth=None,
              align_tips=False,
              branch_lengths=True,
              appearance={}):
    '''
    Plot a phylogenetic tree in matplotlib

    Parameters
    ----------
    tree : ete3.Tree
        ete3 Tree object
    ax : matplotlib.axes._axes.Axes
        An open matplotlib ax object
    x : float
        Current position on x axis.
    y : float
        Current position on y axis.
    ps: list
        Used internally, list of tip labels and x and y positions
    height: float
        Height of the tree in axis units
    width: float
        Width of the tree in axis units
    depth: tuple(float, float, float)
        Total height and width of the original tree in terms of number of
        nodes, total branch length, number of tips
    align_tips: bool
        If True, the tip labels will be aligned rather than positioned at
        the end of the branches. Default False.
    branch_lengths: bool
        If True, use the branch lengths provided in the tree, otherwise fix
        all branches to the same length. Default True.
    appearance: dict
        Dictionary of parameters specifying the appearance of the tree.

    Returns
    -------
    y   float
        Position of previous node on y axis.
    ym  float
        Position of current node on y axis.
    ps  list
        List of lists - tip labels, tip label x positions,
        tip label y positions
    '''
    yint = height / depth[2]

    # td is the branch length - if the branch_lengths parameter is False
    # it is set to 1

    # If the branch lengths are used, the total width of the tree is in
    # the tree branch units, otherwise it's the total number of nodes from
    # the root to the farthest branch

    # textinc stops the tip labels from being immediately next to the tips

    if branch_lengths:
        td = tree.dist
        tot_width = depth[1]
        textinc = tot_width * 0.1

    else:
        td = 1
        tot_width = depth[0]
        textinc = 0.05

    # This interval is used to scale the interval for each node
    # so the total tree width matches the value specified
    xint = width / tot_width

    if tree.is_leaf():
        
        # Position of the node tip
        x_tip_pos = x - (xint * td)
        
        # x_ali_pos is used to align the tips if align_tips is specified
        # x_text_pos is the position of the text - if the tips are aligned
        # the text is also aligned
        if align_tips:
            x_ali_pos = (tot_width * xint) + x0 + 1
            x_text_pos = x_ali_pos + textinc
        else:
            x_ali_pos = None
            x_text_pos = x + textinc

        # Plot the tip label
        ax.text(x_text_pos, -y, appearance['label_dict'][tree.name],
                color=appearance['col_dict'][tree.name],
                fontsize=appearance['font_size'],
                va='center')
        
        # Plot the branch to the tip            
        ax.plot([x, x_tip_pos], [-y, -y],
                color=appearance['line_col'],
                lw=appearance['line_width'])

        # Add an extra line to the aligned tips if align_tips is specified
        if align_tips:
            ax.plot([x, x_ali_pos], [-y, -y],
                     color=appearance['line_col'], alpha=0.2,
                     ls="--",
                     lw=appearance['line_width'])
        # Store the tip label and the position of the tip on the x and y axis
        ps.append([tree.name, x_tip_pos, -y])
        return (y+yint, y, ps)

    else:
        # This section draws the lines for the non-terminal nodes
        # y1 and y2 are the top and bottom positions of the node on the
        # y axis, respectively
        y1 = y
        y2 = y
        # For each tree, all of the children are visited and the function
        # is recursively called
        for c in tree.children:
            # Scale by the branch length if branch_lengths is specified
            if branch_lengths:
                tdc = c.dist
            else:
                tdc = 1

            # The position of the node on the x axis
            x_vert_pos = x + (tdc * xint)
            y, cym, ps = draw_tree(c, ax, x_vert_pos, y,
                                   x0=x0, ps=ps,
                                   height=height,
                                   width=width,
                                   depth=depth, 
                                   align_tips=align_tips,
                                   branch_lengths=branch_lengths,
                                   appearance=appearance)

            # Replace y2 with the current value to increment for the next
            # node - maybe? - forduncs
            y2 = cym
            # This is the bit I don't understand - forduncs
            if c is tree.children[0]:
                y1 = cym

        # midpoint of node on y axis
        ym = (y1 + y2)/2
        
        # Draw the lines
        # Vertical line
        ax.plot([x, x], [-y1, -y2],
                color=appearance['line_col'],
                lw=appearance['line_width'])
        
        # Horizontal line - somehow there are two - forduncs
        ax.plot([x, x-(td*xint)], [-ym, -ym],
                color=appearance['line_col'],
                lw=appearance['line_width'])

        # Add branch support if specified
        # TODO - currently lands on top of the branches if branch_lengths
        # is switched on
        if appearance['show_support']:
            ax.text(x+0.1, -ym, "%.2f" % tree.support,
                    va='center', fontsize=8)

        # TODO scale bar if branch lengths are on
        # TODO sometimes there is no root and sometimes it is giant
        return (y, ym, ps)