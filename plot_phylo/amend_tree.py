#!/usr/bin/env python3
try:
    from plot_phylo import get_boxes
except ImportError:
    import get_boxes


def auto_axis(ax, textobj, xpos, ypos, width, height, depth, scale_bar,
              branch_lengths, reverse):
    """
    Adjust the axis limits around the tree automatically (rather than
    using user definted values).

    Parameters
    ----------
    ax : matplotlib.axes._axes.Axes
        An open matplotlib ax object
    textobj: list of matplotlib.text.Text
        List of text objects containing tip labels, used to ensure the
        labels are within the limits of the plot
    xpos : float
        User defined desired position of the root node of the tree on the x
        axis of ax, in axis units.
    ypos : float
        User defined desired position of the bottom of the tree on the y
        axis of ax, in axis units.
    height : float
        User defined desired height of the tree, in axis units. Default 10.
    width : float
        User defined desired width of the tree, in axis units. Default 10.
    depth: tuple(float, float, float)
        Total height and width of the original tree in terms of number of
        nodes, total branch length, number of tips
    scale_bar: bool
        User defined - True to draw a scale bar, else False
    branch_lengths: bool
        User defined - True to use true branch lengths, False to use
        fixed branch lengths
    reverse: bool
        If True, the tree is reversed on the y-axis,
        showing the root on the right
        hand side. Default False.
    """
    xint = width * 0.01
    yint = (height / depth[2])

    nboxes = 0
    cboxes = 1

    while nboxes != cboxes:
        nboxes = get_boxes.get_boxes(ax, textobj)
        if not reverse:
            xmin = xpos - xint
            xmaxes = [nboxes[x]['xmax'] for x in nboxes]
            xmax = max(xmaxes) + xint
        else:
            xmins = [nboxes[x]['xmin'] for x in nboxes]
            xmin = min(xmins)
            xmax = -xpos + width + xint
        ymaxes = [nboxes[y]['ymax'] for y in nboxes]
        ymax = max(ymaxes)
        ymins = [nboxes[y]['ymin'] for y in nboxes]
        ymin = min(ymins)

        if scale_bar:
            ymin -= yint
        ax.set_xlim(min(xmin, xmax)-xint, max(xmin, xmax)+xint)
        ax.set_ylim(min(ymin, ymax), max(ymin, ymax))
        cboxes = get_boxes.get_boxes(ax, textobj)
    return (textobj, ax)


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
            ptext.get_window_extent(renderer=ax.figure.canvas.get_renderer()))
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
        pbox = ax.transData.inverted().transform(p[1].get_window_extent(
            renderer=ax.figure.canvas.get_renderer()))

        # Move the dotted line to hit the new text position
        # int(not indi) swaps 0 for 1
        p[2][0].set_xdata([pbox[int(not indi)][0], oldline])

        # Set the y axis position
        p[1].set_verticalalignment('center')

        # Store the new values
        ps_new.append(p)
    return (ps_new)
