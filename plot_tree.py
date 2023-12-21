#!/usr/bin/env python3
import ete3

def plot_tree(tree, ax, xpos=0, ypos=0,
              height=10, width=10,
              support=False, align=False, bl=True):
    T = ete3.Tree(tree)
    maxdist = ((T.get_farthest_leaf(topology_only=True)[1],
                T.get_farthest_leaf(topology_only=False)[1],
                len(T)))
    ax, _, _ = draw_tree(T, ax,
                         x=xpos,
                         y=-(ypos+len(T)),
                         x0=xpos,
                         height=height,
                         width=width,
                         depth=maxdist,
                         support=support,
                         align=align,
                         bl=bl)
    # ax.set_axis_off()
    return (ax)

def draw_tree(tree, ax,
              x=0,
              y=0,
              x0=0,
              height=10,
              width=10,
              depth=None,
              support=False,
              align=False,
              bl=True):
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
        if not align:
            if bl:
                totbl = depth[1]
                xint = width / totbl
                ax.text(x+(depth[1] * 0.01), -y, tree.name, va='center')
                ax.plot([x, x-(xint*td)], [-y, -y], color='black')
            else:
                totbl = depth[0]
                xint = width / totbl
                ax.text(x+0.1, -y, tree.name, va='center')
                ax.plot([x, x-xint], [-y, -y], color='black')
        else:
            if bl:
                totbl = depth[1]
                xint = width / totbl
                ax.text(depth[1]+0.1, -y, tree.name, va='center')
                ax.plot([x, x-(xint * td)], [-y, -y], color='black')
                ax.plot([x, depth[1]+0.1], [-y, -y], color='lightgrey',
                        ls="-")
            else:
                totbl = depth[0]
                xint = width / totbl
                ax.text(depth[0]+xint+0.1, -y, tree.name, va='center')
                ax.plot([x-xint, depth[0]+1], [-y, -y], color='black')

        return (ax, y+yint, y)
    else:
        y1 = y
        y2 = y
        for c in tree.children:
            td = c.dist
            if bl:
                totbl = depth[1]
                xint = width / totbl
                ax, y, cym = draw_tree(c, ax, x+(td*xint), y,
                                       x0=x0, height=height, width=width,
                                       support=support,
                                       align=align, depth=depth, bl=bl)
            else:
                totbl = depth[0]
                xint = width / totbl
                ax, y, cym = draw_tree(c, ax, x+xint, y,
                                       x0=x0, height=height, width=width,
                                       support=support,
                                       align=align, depth=depth, bl=bl)             
            y2 = cym
            if c is tree.children[0]:
                y1 = cym
        # midpoint of node on y axis
        ym = (y1 + y2)/2
        if support:
            ax.text(x+0.1, -ym, "%.2f" % tree.support,
                    va='center', fontsize=8)
        ax.plot([x, x], [-y1, -y2], color='black')
        td = tree.dist
        if bl:
            totbl = depth[1]
            xint = width / totbl
            ax.plot([x, x-(td*xint)], [-ym, -ym], color='black')
        else:
            totbl = depth[0]
            xint = width / totbl
            ax.plot([x, x-xint], [-ym, -ym], color='black')
            
        return (ax, y, ym)