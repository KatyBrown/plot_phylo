#!/usr/bin/env python3
import ete3


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
               col_dict={},
               label_dict={},
               font_size=10,
               line_col='black',
               line_width=1):
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
        List of lists - ordered as tip labels, tip label text objects,
        alignment lines (if aligned). All are in the same order.
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

    if reverse:
        xpos = -xpos
    # Call the main function. The second and third returns are used
    # internally when the function is called recursively but
    # are not needed by the user

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

    if rev_align_tips:
        ps = reverse_align(ax, ps, reverse)
    # Hide axis
    if not show_axis:
        ax.set_axis_off()
    if scale_bar and branch_lengths:
        if not reverse:
            draw_scale_bar(ax, width, height, maxdist, xpos, ypos,
                           scale_bar_width=scale_bar_width,
                           appearance=appearance)
        else:
            draw_scale_bar(ax, width, height, maxdist, -xpos, ypos,
                           scale_bar_width=scale_bar_width,
                           appearance=appearance)
    textobj = [p[1] for p in ps]
    return (get_boxes(ax, textobj))


def get_boxes(ax, texts):
    '''
    Converts a list of text objects to their co-ordinates on the axis in
    axis units.

    Parameters
    ----------
    ax : matplotlib.axes._axes.Axes,
        An open matplotlib ax object where the tree will be plotted.
    texts : list
        A list of matplotlib.pyplot.text objects representing the tip
        labels from the tree and their metadata.

    Returns
    -------
    boxpos : dict
        A dictionary of dictionaries where the top level keys are the tip
        labels. Within each subdictionary the key value pairs are
        index (position in the tree starting from the top) and the minimum,
        maximum and central position of the text box on the x and y axis,
        as index, xmin, xmid, xmax and ymin, ymid and ymax.

    '''
    boxpos = dict()
    # Iterate through the tip labels
    for i, txt in enumerate(texts):
        # Get the position of the boxes containing the labels, convert to axis
        # units
        box = ax.transData.inverted().transform(txt.get_window_extent())
        nam = txt.get_text().strip()
        # Build the dictionary
        boxpos[nam] = dict()
        boxpos[nam]['index'] = i
        boxpos[nam]['xmin'] = box[0][0].round(3)
        boxpos[nam]['xmax'] = box[1][0].round(3)
        boxpos[nam]['ymin'] = box[0][1].round(3)
        boxpos[nam]['ymax'] = box[1][1].round(3)
        boxpos[nam]['ymid'] = (box[0][1] + ((
            box[1][1] - box[0][1]) / 2)).round(3)
        boxpos[nam]['xmid'] = (
            box[0][0] + ((box[1][0] - box[0][1]) / 2)).round(3)

    return (boxpos)


def draw_tree(tree, ax,
              x=0,
              y=0,
              x0=0,
              ps=[],
              height=10,
              width=10,
              depth=None,
              align_tips=False,
              rev_align_tips=False,
              branch_lengths=True,
              reverse=False,
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
    rev_align_tips: bool
        If True  the tip labels are right aligned
        if reverse=False and left aligned if reverse=True.
    branch_lengths: bool
        If True, use the branch lengths provided in the tree, otherwise fix
        all branches to the same length. Default True.
    reverse: bool
        If True, reverse the tree on the y-axis, showing the root on the right
        hand side. Default False.
    appearance: dict
        Dictionary of parameters specifying the appearance of the tree.

    Returns
    -------
    y   float
        Position of previous node on y axis.
    ym  float
        Position of current node on y axis.
    ps  list
        List of lists - ordered as tip labels, tip label text objects,
        alignment lines (if aligned). All are in the same order.
    '''
    # This is the increment for the position of each terminal node on
    # the y axis.
    # The number of nodes - 1 is used because one branch will be at position 0
    yint = height / (depth[2] - 1)

    # td is the branch length - if the branch_lengths parameter is False
    # it is set to 1

    # If the branch lengths are used, the total width of the tree is in
    # the tree branch units, otherwise it's the total number of nodes from
    # the root to the farthest branch

    # textinc stops the tip labels from being immediately next to the tips

    if branch_lengths:
        td = tree.dist
        tot_width = depth[1]

    else:
        td = 1
        tot_width = depth[0] + 1

    # This interval is used to scale the interval for each node
    # so the total tree width matches the value specified
    xint = width / tot_width

    if tree.is_leaf():

        # Position of the node tip
        x_tip_pos = x - (xint * td)

        # x_ali_pos is used to align the tips if align_tips is specified
        # x_text_pos is the position of the text - if the tips are aligned
        # the text is also aligned
        if align_tips or rev_align_tips:
            x_ali_pos = (tot_width * xint) + x0 + 1
            x_text_pos = x_ali_pos
        else:
            x_ali_pos = None
            x_text_pos = x
        xmax = (tot_width * xint)
        if reverse:
            x_tip_pos = xmax - x_tip_pos
            x_text_pos = xmax - x_text_pos
            if x_ali_pos is not None:
                x_ali_pos = xmax - x_ali_pos
            x = xmax - x
            hali = 'right'
        else:
            hali = 'left'
        # Plot the tip label
        textpos = ax.text(x_text_pos, -y,
                          "  %s  " % appearance['label_dict'][tree.name],
                          color=appearance['col_dict'][tree.name],
                          fontsize=appearance['font_size'],
                          va='center', ha=hali)

        # Plot the branch to the tip
        ax.plot([x, x_tip_pos], [-y, -y],
                color=appearance['line_col'],
                lw=appearance['line_width'])

        # Add an extra line to the aligned tips if align_tips is specified
        if align_tips or rev_align_tips:
            line = ax.plot([x, x_ali_pos], [-y, -y],
                           color=appearance['line_col'], alpha=0.2,
                           ls="--",
                           lw=appearance['line_width'])
            ps.append([tree.name, textpos, line])
        else:
            ps.append([tree.name, textpos])

        # Store the tip label and the position of the tip on the x and y axis

        return (y+yint, y, ps)

    else:
        # This section draws the lines for the non-terminal nodes

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

            # returns y - the bottom position of all the labels so far
            # cym - the middle of the previous node on the y axis

            y, cym, ps = draw_tree(c, ax, x_vert_pos, y,
                                   x0=x0, ps=ps,
                                   height=height,
                                   width=width,
                                   depth=depth,
                                   align_tips=align_tips,
                                   rev_align_tips=rev_align_tips,
                                   branch_lengths=branch_lengths,
                                   reverse=reverse,
                                   appearance=appearance)

            # y1 and y2 are the top and bottom positions of the current
            # child node on the y axis, respectively
            # Gives the extent of the vertical line for this segment

            if c is tree.children[0]:
                y1 = cym
            elif c is tree.children[-1]:
                y2 = cym

        # midpoint of node on y axis
        ym = (y1 + y2)/2

        if reverse:
            xmax = (tot_width * xint)
            x = xmax - x

        # Draw the lines
        # Vertical line
        ax.plot([x, x], [-y1, -y2],
                color=appearance['line_col'],
                lw=appearance['line_width'])

        # Horizontal line - each node draws the one line that
        # projects towards its parent so x is the position of the
        # vertical line and x-(td*xint) is one increment back
        # towards the root

        if not reverse:
            ax.plot([x, x-(td*xint)], [-ym, -ym],
                    color=appearance['line_col'],
                    lw=appearance['line_width'])
        else:
            ax.plot([x, x+(td*xint)], [-ym, -ym],
                    color=appearance['line_col'],
                    lw=appearance['line_width'])

        # Add branch support if specified
        # TODO - currently lands on top of the branches if branch_lengths
        # is switched on
        if appearance['show_support']:
            if not reverse:
                ax.text(x, -ym, " %.2f" % tree.support, ha='left',
                        va='center', fontsize=appearance['font_size']-2)
            else:
                ax.text(x, -ym, "%.2f " % tree.support, ha='right',
                        va='center', fontsize=appearance['font_size']-2)

        return (y, ym, ps)


def reverse_align(ax, ps, reverse):
    '''
    Realigns the text in the tip labels so that for a standard tree, the
    text is right aligned, for a mirrored tree (root on the right), the
    text is left aligned. Only used when tip labels are set to be aligned.

    This has to happen once the whole plot is drawn as the limits
    of the text only exist once the text exists.

    Parameters
    ----------
    ax : matplotlib.axes._axes.Axes
        An open matplotlib ax object
    ps : list
        List of lists - ordered as tip labels, tip label text objects,
        alignment lines (if aligned). All are in the same order.
    reverse: bool
        If True, reverse the tree on the y-axis, showing the root on the right
        hand side. Default False.

    Returns
    -------
    ps_new : list
        List of lists - ordered as tip labels, tip label text objects,
        alignment lines (if aligned). All are in the same order. Updated
        based on new alignment.
    '''

    x_extremes = []
    ys = []
    # Used to determine which x co-ordinates to take depending on the
    # tree orientation
    if reverse:
        indi = 0
    else:
        indi = 1
    for pnam, ptext, pline in ps:
        # Get the data units of the box which encloses the text
        box = ax.transData.inverted().transform(
            ptext.get_window_extent())
        # Get the rightmost point of the text box (regular tree)
        # or the leftmost (reversed tree)
        x_extreme = box[indi][0]
        x_extremes.append(x_extreme)

        # Store the y axis positions
        ys.append(box[1][1])

    if not reverse:
        # For right alignment, take the rightmost x point
        maxi = max(x_extremes)
    else:
        # For left alignment, take the leftmost x point
        maxi = min(x_extremes)
    alis = ['left', 'right']

    ps_new = []
    for i, p in enumerate(ps):
        # Move the text to the right position
        p[1].set_position([maxi, ys[i]])

        # Get the current left end of the dotted alignment line
        oldline = p[2][0].get_xdata()[0]

        # Left or right align the text
        p[1].set_horizontalalignment(alis[indi])

        # Get the updated text position limits
        pbox = ax.transData.inverted().transform(p[1].get_window_extent())

        # Move the dotted line to hit the new text position
        # int(not indi) swaps 0 for 1
        p[2][0].set_xdata([pbox[int(not indi)][0], oldline])

        # Set the y axis position
        p[1].set_verticalalignment('center')

        # Store the new values
        ps_new.append(p)
    return (ps_new)


def draw_scale_bar(ax, width, height, depth, left, bottom,
                   scale_bar_width=None,
                   appearance={'font_size': 10}):
    '''
    Adds a scale bar to the tree - only when branch lengths are specified.

    The default length is 0.25 * total tree width, or it can be specified
    using scale_bar_width.

    Parameters
    ----------
    ax : matplotlib.axes._axes.Axes
        An open matplotlib ax object

    height : float
        Height of the tree, in axis units.
    width : float
        Width of the tree, in axis units.
    depth: tuple(float, float, float)
        Total height and width of the original tree in terms of number of
        nodes, total branch length, number of tips
    bottom: float
        The bottom position of the tree on the y axis
    scale_bar_width: float
        The desired width of the scale bar, if not specified
        tree width * 0.25 is used
    appearance: dict
        Dictionary of parameters specifying the appearance of the tree.
    '''
    # depth[1] - total width of the tree in tree units
    # width - total width of tree in axis units
    # xint - width of one tree unit in axis units
    xint = width / depth[1]

    # Distance from x axis to start the scale bar
    # 10% of total tree width
    interx = width * 0.1

    # Distance on y axis to extend the bracket ends on the scale bar
    # 10% of the height of one node
    intery = (height / depth[2]) * 0.1
    bottom -= (height / depth[2])
    # scale_bar_width = total width of scale bar in axis units
    if not scale_bar_width:
        scale_bar_width = width * 0.25

    # Convert the scale bar width to tree units
    scale = scale_bar_width / xint

    # Draw the horizontal line
    ax.plot([left+interx, left+interx+scale_bar_width],
            [bottom, bottom], color='black')

    # Bracket the ends of the scale bar with small vertical lines
    ax.plot([left+interx, left+interx],
            [bottom-intery, bottom+intery], color='black')
    ax.plot([left+interx+scale_bar_width, left+interx+scale_bar_width],
            [bottom-intery, bottom+intery], color='black')

    # Add the scale text
    ax.text(left+interx+(scale_bar_width/2), bottom+intery, "%.3f" % scale,
            va='bottom', ha='center', fontsize=appearance['font_size']-2)
