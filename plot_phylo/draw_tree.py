#!/usr/bin/env python3
import numpy as np


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
              appearance={},
              collapse=[],
              collapseD=dict()):
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
    collapse: list
        Collapse nodes where possible based on strings in the list.

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
        if tree.name in appearance['bold']:
            bold = 'bold'
        else:
            bold = 'normal'

        if 'COLLAPSE|' not in tree.name:
            for c in collapse:
                tree.name = tree.name.strip(c)
            texti = appearance['label_dict'][tree.name]
            # Plot the branch to the tip
            ax.plot([x, x_tip_pos], [-y, -y],
                    color=appearance['line_col'],
                    lw=appearance['line_width'])

        else:
            texti = collapseD[tree.name]
            yyy = (yint / 2) * 0.8
            if branch_lengths:
                xxx = xint * 0.4
            else:
                xxx = xint * 0.2
            if not branch_lengths:
                ax.plot([x, x_tip_pos+xxx], [-y+yyy, -y],
                        color=appearance['line_col'],
                        lw=appearance['line_width'],
                        solid_capstyle='butt')
                ax.plot([x, x_tip_pos+xxx], [-y-yyy, -y],
                        color=appearance['line_col'],
                        lw=appearance['line_width'],
                        solid_capstyle='butt')
                ax.plot([x_tip_pos, x_tip_pos+xxx], [-y, -y],
                        color=appearance['line_col'],
                        lw=appearance['line_width'],
                        solid_capstyle='butt')
                ax.plot([x, x], [-y+yyy, -y-yyy],
                        color=appearance['line_col'],
                        lw=appearance['line_width'],
                        solid_capstyle='butt')
            else:
                ax.plot([x, x_tip_pos], [-y+yyy, -y],
                        color=appearance['line_col'],
                        lw=appearance['line_width'],
                        solid_capstyle='butt')
                ax.plot([x, x_tip_pos], [-y-yyy, -y],
                        color=appearance['line_col'],
                        lw=appearance['line_width'],
                        solid_capstyle='butt')
                ax.plot([x_tip_pos, x_tip_pos], [-y, -y],
                        color=appearance['line_col'],
                        lw=appearance['line_width'],
                        solid_capstyle='butt')
                ax.plot([x, x], [-y+yyy, -y-yyy],
                        color=appearance['line_col'],
                        lw=appearance['line_width'],
                        solid_capstyle='butt')

        textpos = ax.text(x_text_pos, -y,
                          "  %s  " % texti,
                          color=appearance['col_dict'][tree.name],
                          fontsize=appearance['font_size'],
                          va='center', ha=hali, fontweight=bold)
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
                                   appearance=appearance,
                                   collapse=collapse,
                                   collapseD=collapseD)

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
                if tree.support == 1:
                    ax.text(x, -ym, " %i" % tree.support, ha='left',
                            va='center', fontsize=appearance['font_size']-2,
                            color='#7c7c7c')
                else:
                    ax.text(x, -ym, " %.2f" % tree.support, ha='left',
                            va='center', fontsize=appearance['font_size']-2,
                            color='#7c7c7c')
            else:
                ax.text(x, -ym, "%.2f " % tree.support, ha='right',
                        va='center', fontsize=appearance['font_size']-2)

        return (y, ym, ps)


def collapse_nodes(tree, collapse_list, collapse_names):
    cD = dict(zip(collapse_list, collapse_names))
    collapseD = dict()
    for string in collapse_list:
        keeps = set()
        collapsed = set()
        done = set()
        ddD = dict()
        for node in tree.traverse():
            x = 0
            L = list(node.get_leaves())
            dd = []
            for leaf in L:
                if leaf.name.endswith(string) and leaf not in done:
                    dd.append(leaf.dist)
                    x += 1
            if x == len(L) or (len(L) == 1 and leaf not in done):
                keeps.add(L[0].name)
                done = done | set(L)
                if x > 1:
                    collapsed.add(L[0])
                    ddD[L[0]] = np.mean(dd)
        tree.prune(keeps)
        for leaf in tree.get_leaves():
            if leaf in collapsed:
                leaf.dist = ddD[leaf]
                leaf.name = 'COLLAPSE|%s' % (leaf.name)
                collapseD[leaf.name] = cD[string]
    return (tree, collapseD)