#!/usr/bin/env python3
import ete3

def plot_tree(tree, ax,
              xpos=0,
              ypos=0,
              height=10,
              width=10,
              show_axis=True,
              show_support=False,
              align_tips=False,
              branch_lengths=True,
              colour_dict={},
              label_dict={},
              font_size=10,
              line_col='black',
              line_width=5):
    
    # Read the tree
    T = ete3.Tree(tree)

    # Define dictionaries for colours and labels if not provided
    if len(colour_dict) == 0:
        colour_dict = {x: 'black' for x in tree.get_leaf_names()}
    if len(label_dict) == 0:
        label_dict = {x: x for x in T.get_leaf_names()}

    # Dictionary to pass apperance params to the plotting function
    appearance = {'font_size': font_size,
                  'line_col': line_col,
                  'line_width': line_width,
                  'colour_dict': colour_dict,
                  'label_dict': label_dict,
                  'show_support': show_support}


    # Calculate the total height and width of the original tree
    # in terms of number of nodes, total branch length, number of tips
    maxdist = ((T.get_farthest_leaf(topology_only=True)[1],
                T.get_farthest_leaf(topology_only=False)[1],
                len(T)))

    
    # Call the main function. The second and third returns are used
    # internally when the function is called recursively but
    # are not needed by the user
    
    # subtract one from width as the root adds one unit
    # y is subtracted from the total height to order tip names correctly
    ax, _, _, ps = draw_tree(T, ax,
                             x=xpos+1,
                             y=-(ypos+len(T)),
                             x0=xpos,
                             ps=[],
                             height=height,
                             width=width-1,
                             depth=maxdist,
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
    x : int
        Current position on x axis.
    y : TYPE, optional
        Current position on y axis.

    Returns
    -------
    y   int
        Position of previous node on y axis.
    ym  int
        Position of current node on y axis.

    '''
    yint = height / depth[2]
    if tree.is_leaf():
        td = tree.dist
        if not align_tips:
            if branch_lengths:
                totbl = depth[1]
                xint = width / totbl
                ax.text(x+(depth[1] * 0.01), -y,
                        tree.name,
                        color=appearance['colour_dict'][tree.name],
                        va='center')
                ax.plot([x, x-(xint*td)], [-y, -y],
                        color='black')
                ps.append([tree.name, x-(xint*td), -y])
            else:
                totbl = depth[0]
                xint = (width - 2) / totbl
                ax.text(x+0.1, -y, tree.name,
                        color=appearance['colour_dict'][tree.name],
                        va='center')
                ax.plot([x, x-xint], [-y, -y],
                        color='black')
                ps.append([tree.name, x-xint, -y])
        else:
            if branch_lengths:
                totbl = depth[1]
                xint = width / totbl
                ax.text(((depth[1])*xint)+0.1+x0+1, -y, tree.name,
                        color=appearance['colour_dict'][tree.name],
                        va='center')
                ax.plot([x, x-(xint * td)], [-y, -y],
                        color='black')
                ax.plot([x, ((depth[1])*xint)+x0+1], [-y, -y],
                        color='lightgrey',
                        ls="-")
                ps.append([tree.name, ((depth[1])*xint)+x0+1, -y])
            else:
                totbl = depth[0]
                xint = width / totbl
                ax.text((depth[0]*xint)+x0+1.1, -y, tree.name,
                        color=appearance['colour_dict'][tree.name],
                        va='center')
                ax.plot([x-xint , ((depth[0])*xint)+x0+1], [-y, -y], 
                        color='black')
                ps.append([tree.name, ((depth[0])*xint)+x0+1, -y])
        return (ax, y+yint, y, ps)
    else:
        y1 = y
        y2 = y
        for c in tree.children:
            td = c.dist
            if branch_lengths:
                totbl = depth[1]
                xint = width / totbl
                ax, y, cym, ps = draw_tree(c, ax, x+(td*xint), y,
                                           x0=x0, ps=ps,
                                           height=height,
                                           width=width,
                                           depth=depth, 
                                           align_tips=align_tips,
                                           branch_lengths=branch_lengths,
                                           appearance=appearance)

            else:
                totbl = depth[0]
                if align_tips:
                    xint = width / totbl
                else:
                    xint = (width - 2) / totbl
                ax, y, cym, ps = draw_tree(c, ax, x+xint, y,
                                           x0=x0, ps=ps,
                                           height=height,
                                           width=width,
                                           depth=depth, 
                                           align_tips=align_tips,
                                           branch_lengths=branch_lengths,
                                           appearance=appearance)
            y2 = cym
            if c is tree.children[0]:
                y1 = cym
        # midpoint of node on y axis
        ym = (y1 + y2)/2
        if appearance['show_support']:
            ax.text(x+0.1, -ym, "%.2f" % tree.support,
                    va='center', fontsize=8)
        ax.plot([x, x], [-y1, -y2], color='black')
        td = tree.dist
        if branch_lengths:
            totbl = depth[1]
            xint = width / totbl
            ax.plot([x, x-(td*xint)], [-ym, -ym], color='black')
        else:
            totbl = depth[0]
            if align_tips:
                xint = width / totbl
            else:
                xint = (width - 2) / totbl
            ax.plot([x, x-xint], [-ym, -ym], color='black')
        return (ax, y, ym, ps)